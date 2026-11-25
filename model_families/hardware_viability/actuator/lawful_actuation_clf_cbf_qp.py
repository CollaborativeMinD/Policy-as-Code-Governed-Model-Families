"""V.1–V.3 — Bounded single-integrator control with shared CBF and CLF slacks."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/lawful_actuation_clf_cbf_qp')


from math import fsum, hypot, inf, isfinite, sqrt


def require_positive(name, value):
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")


def _as_state_vector(name, value):
    try:
        if isinstance(value, (str, bytes)):
            raise TypeError
        vector = [float(item) for item in value]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a one-dimensional numeric sequence") from exc
    if not all(map(isfinite, vector)):
        raise ValueError(f"{name} must contain only finite values")
    return vector


def _as_hazard_matrix(hazards, state_dim):
    try:
        rows = list(hazards)
    except TypeError as exc:
        raise ValueError("hazards must be a vector or a matrix") from exc
    if not rows:
        return []
    try:
        iter(rows[0])
    except TypeError:
        rows = [rows]
    rows = [_as_state_vector("hazard", row) for row in rows]
    if all(not row for row in rows):
        return []
    if any(len(row) != state_dim for row in rows):
        raise ValueError("each hazard must match the state dimension")
    return rows


def _dot(left, right):
    return fsum(a*b for a, b in zip(left, right, strict=True))


def cbf_margin(x, u, hazard, r_safe: float, dt: float) -> float:
    """Return h_i(x + u dt) = ||(x + u dt) - hazard_i||^2 - r_safe^2.

    A nonnegative value means the discrete next state remains outside the hazard exclusion radius.
    """
    require_positive("r_safe", r_safe)
    require_positive("dt", dt)
    x_vec = _as_state_vector("x", x)
    u_vec = _as_state_vector("u", u)
    hazard_vec = _as_state_vector("hazard", hazard)
    if len(x_vec) != len(u_vec) or len(x_vec) != len(hazard_vec):
        raise ValueError("x, u, and hazard dimensions must match")
    return _barrier(x_vec, u_vec, hazard_vec, r_safe, dt)[0]


def clf_value(x, x_ref) -> float:
    """Quadratic CLF value V(x) = 1/2 ||x - x_ref||^2."""
    x_vec = _as_state_vector("x", x)
    ref_vec = _as_state_vector("x_ref", x_ref)
    if len(x_vec) != len(ref_vec):
        raise ValueError("x and x_ref dimensions must match")
    err = [a - b for a, b in zip(x_vec, ref_vec)]
    return 0.5 * _dot(err, err)


def clf_vdot(x, u, x_ref) -> float:
    """Single-integrator CLF derivative Vdot(x, u) = (x - x_ref)^T u."""
    x_vec = _as_state_vector("x", x)
    u_vec = _as_state_vector("u", u)
    ref_vec = _as_state_vector("x_ref", x_ref)
    if len(x_vec) != len(u_vec) or len(x_vec) != len(ref_vec):
        raise ValueError("x, u, and x_ref dimensions must match")
    return fsum((a-b)*v for a, b, v in zip(x_vec, ref_vec, u_vec))


def clf_margin(x, u, x_ref, alpha: float) -> float:
    """Return the CLF inequality margin: -alpha V(x) - Vdot(x, u).

    Nonnegative margin is equivalent to Vdot(x, u) <= -alpha * V(x).
    """
    require_positive("alpha", alpha)
    return float((-alpha * clf_value(x, x_ref)) - clf_vdot(x, u, x_ref))


def _barrier(x, u, hazard, radius, dt):
    offset = [a + dt*v - h for a, v, h in zip(x, u, hazard)]
    return _dot(offset, offset) - radius**2, [2*dt*v for v in offset]


def _basis(rows, active):
    """Factor active constraint normals using reorthogonalized Gram-Schmidt."""
    axes, triangular = [], []
    for index in active:
        v = rows[index][0].copy()
        coefficients = [0.0] * len(axes)
        for _ in range(2):
            for j, axis in enumerate(axes):
                projection = _dot(v, axis)
                coefficients[j] += projection
                v = [a - projection*b for a, b in zip(v, axis)]
        length = hypot(*v)
        if length < _policy.value("basis_tolerance"):
            raise ArithmeticError("dependent active constraints")
        axes.append([a/length for a in v])
        triangular.append(coefficients + [length])
    return axes, triangular


def _project(target, start, constraints):
    """Project onto a feasible linearized subproblem using a primal active set."""
    rows = []
    for normal, minimum in constraints:
        length = hypot(*normal)
        rows.append(([a/length for a in normal], minimum/length))
    z = start.copy()
    active = []
    for _ in range(max(_policy.value("min_projection_iterations"), _policy.value("projection_iteration_factor") * (len(rows) + len(z)))):
        axes, triangular = _basis(rows, active)
        gradient = [a-b for a, b in zip(z, target)]
        # Multipliers in the active basis and the free descent direction.
        products = [_dot(gradient, axis) for axis in axes]
        direction = [-g + fsum(c*axis[j] for c, axis in zip(products, axes))
                     for j, g in enumerate(gradient)]
        if hypot(*direction) <= _policy.value("projection_tolerance") * (1 + hypot(*gradient)):
            multipliers = products.copy()
            for j in reversed(range(len(active))):
                multipliers[j] /= triangular[j][j]
                for i in range(j):
                    multipliers[i] -= triangular[j][i] * multipliers[j]
            if not multipliers or min(multipliers) >= -_policy.value("projection_tolerance") * (1 + hypot(*gradient)):
                return z
            active.pop(multipliers.index(min(multipliers)))
            continue

        step, blocking = 1.0, None
        for i, (normal, minimum) in enumerate(rows):
            if i in active:
                continue
            rate = _dot(normal, direction)
            if rate >= -_policy.value("basis_tolerance") * hypot(*direction):
                continue
            distance = _dot(normal, z) - minimum
            limit = max(0.0, distance) / -rate
            if limit < step:
                step, blocking = limit, i
        z = [a + step*b for a, b in zip(z, direction)]
        if blocking is not None:
            active.append(blocking)
    raise ArithmeticError("active-set iteration limit")


def _solve(x, nominal, hazards, radius, dt, bounds, reference, alpha, cbf_weight, clf_weight):
    # In scaled coordinates the Hessian of tracking plus both slack costs is identity.
    n = len(x)
    weights = [sqrt(2.0)*sqrt(cbf_weight), sqrt(2.0)*sqrt(clf_weight)]
    error = None if reference is None else [a-b for a, b in zip(x, reference)]
    clf_target = 0.0 if error is None else -0.5*alpha*_dot(error, error)
    initial = [min(max(v, lo), hi) for v, (lo, hi) in zip(nominal, bounds)]

    def constraints_at(u):
        barriers = [_barrier(x, u, hazard, radius, dt) for hazard in hazards]
        stability = 0.0 if error is None else clf_target - _dot(error, u)
        slacks = [max([0.0] + [-h for h, _ in barriers]), max(0.0, -stability)]
        return barriers, stability, slacks

    def cost(u):
        _, _, slacks = constraints_at(u)
        return hypot(*(v-w for v, w in zip(u, nominal)), *(w*s for w, s in zip(weights, slacks)))

    u = initial.copy()
    # At the exact center of a violated ball the first-order CBF normal vanishes.
    # Try bounded axial perturbations in both directions and retain only a descent.
    if any(h < 0 and not any(normal) for h, normal in constraints_at(u)[0]):
        best_cost = cost(u)
        for i, (lo, hi) in enumerate(bounds):
            for sign in (1, -1):
                for fraction in _policy.value("probe_fractions"):
                    candidate = initial.copy()
                    candidate[i] = min(hi, max(lo, initial[i] + sign*fraction*radius/dt))
                    candidate_cost = cost(candidate)
                    if candidate_cost < best_cost:
                        u, best_cost = candidate, candidate_cost

    coordinates = n + 2
    for _ in range(_policy.value("outer_iterations")):
        barriers, stability, slacks = constraints_at(u)
        # Unknowns are the control increment and the two absolute scaled slacks.
        target = [v-w for v, w in zip(nominal, u)] + [0.0, 0.0]
        start = [0.0]*n + [w*s for w, s in zip(weights, slacks)]
        constraints = [(normal + [1/weights[0], 0.0], -h) for h, normal in barriers]
        if error is not None:
            constraints.append(([-v for v in error] + [0.0, 1/weights[1]], -stability))
        for i, (lo, hi) in enumerate(bounds):
            normal = [0.0]*coordinates
            normal[i] = 1.0
            constraints.append((normal, lo-u[i]))
            constraints.append(([-v for v in normal], u[i]-hi))
        constraints += [([0.0]*n + [1.0, 0.0], 0.0), ([0.0]*n + [0.0, 1.0], 0.0)]
        try:
            solution = _project(target, start, constraints)
        except ArithmeticError as exc:
            return initial, inf, inf, False, str(exc)
        next_u = [min(hi, max(lo, v+step)) for v, step, (lo, hi) in zip(u, solution[:n], bounds)]
        movement = hypot(*(a-b for a, b in zip(next_u, u)))
        u = next_u
        if movement <= _policy.value("movement_tolerance") * (1 + hypot(*u)):
            _, _, (cbf_slack, clf_slack) = constraints_at(u)
            return u, cbf_slack, clf_slack, True, "Optimization terminated successfully"
    return initial, inf, inf, False, "Sequential projection iteration limit"


def lawful_control_qp(
    x,
    u_nom,
    hazards,
    r_safe: float,
    dt: float,
    u_bounds,
    Gamma: float = _policy.default,
    *,
    x_ref=_policy.default,
    alpha: float = _policy.default,
    Gamma_cbf: float | None = _policy.default,
    Gamma_clf: float | None = _policy.default,
    clf_required: bool = _policy.default,
):
    """Solve the lawful actuation CLF-CBF QP.

    Args:
        x: Current state vector.
        u_nom: Nominal control vector.
        hazards: Hazard points, one row per hazard. Empty is permitted.
        r_safe: Exclusion radius for each hazard.
        dt: Discrete actuation step in seconds.
        u_bounds: Sequence of ``(lower, upper)`` pairs, one per control dimension.
        Gamma: Backward-compatible default slack penalty used when Gamma_cbf/Gamma_clf are omitted.
        x_ref: CLF reference/goal state. Required by default.
        alpha: Positive CLF convergence rate.
        Gamma_cbf: Optional CBF slack penalty.
        Gamma_clf: Optional CLF slack penalty.
        clf_required: If true, missing x_ref raises ValueError. Set false only for explicit
            legacy CBF + nominal-control tracking runs.

    Returns:
        Dict containing u_star, slacks, CLF/CBF margins, success status, and null-set trigger.
    """
    require_positive("r_safe", r_safe)
    require_positive("dt", dt)
    require_positive("Gamma", Gamma)
    require_positive("alpha", alpha)

    if Gamma_cbf is None:
        Gamma_cbf = Gamma
    if Gamma_clf is None:
        Gamma_clf = Gamma
    require_positive("Gamma_cbf", Gamma_cbf)
    require_positive("Gamma_clf", Gamma_clf)

    x_vec = _as_state_vector("x", x)
    u_nom_vec = _as_state_vector("u_nom", u_nom)
    n = len(u_nom_vec)
    if len(x_vec) != n:
        raise ValueError("x and u_nom dimensions must match")
    if len(u_bounds) != n:
        raise ValueError("u_bounds length must match control dimension")

    bounds = [_as_state_vector("control bound", pair) for pair in u_bounds]
    if any(len(pair) != 2 or pair[0] > pair[1] for pair in bounds):
        raise ValueError("u_bounds must contain finite ordered lower/upper pairs")

    hazard_matrix = _as_hazard_matrix(hazards, state_dim=n)

    if x_ref is None:
        if clf_required:
            raise ValueError("x_ref is required for lawful CLF-CBF QP execution")
        ref_vec = None
    else:
        ref_vec = _as_state_vector("x_ref", x_ref)
        if len(ref_vec) != n:
            raise ValueError("x_ref dimension must match x dimension")

    u, cbf_slack, clf_slack, success, message = _solve(
        x_vec, u_nom_vec, hazard_matrix, r_safe, dt, bounds, ref_vec,
        alpha, Gamma_cbf, Gamma_clf,
    )

    cbf_margins = [cbf_margin(x_vec, u, hz, r_safe, dt) for hz in hazard_matrix]
    cbf_safe_without_slack = success and cbf_slack <= _policy.value("slack_tolerance") and all(margin >= -_policy.value("slack_tolerance") for margin in cbf_margins)

    if ref_vec is None:
        clf_val = None
        clf_derivative = None
        clf_margin_value = None
        clf_stable_without_slack = not clf_required
    else:
        clf_val = clf_value(x_vec, ref_vec)
        clf_derivative = clf_vdot(x_vec, u, ref_vec)
        clf_margin_value = clf_margin(x_vec, u, ref_vec, alpha)
        clf_stable_without_slack = success and clf_slack <= _policy.value("slack_tolerance") and clf_margin_value >= -_policy.value("slack_tolerance")

    feasible_no_slack = bool(cbf_safe_without_slack and clf_stable_without_slack)

    return {
        "u_star": u,
        "cbf_slack": cbf_slack,
        "clf_slack": clf_slack,
        "slack": max(cbf_slack, clf_slack),  # legacy aggregate field
        "success": bool(success),
        "safe_without_slack": feasible_no_slack,
        "cbf_safe_without_slack": bool(cbf_safe_without_slack),
        "clf_stable_without_slack": bool(clf_stable_without_slack),
        "null_set": not feasible_no_slack,
        "cbf_margins": cbf_margins,
        "clf_value": clf_val,
        "clf_vdot": clf_derivative,
        "clf_margin": clf_margin_value,
        "message": message,
    }


def null_set_trigger(safe_without_slack: bool) -> bool:
    return not safe_without_slack


__all__ = [
    "cbf_margin",
    "clf_value",
    "clf_vdot",
    "clf_margin",
    "lawful_control_qp",
    "null_set_trigger",
]

_policy.bind(globals())
