"""M3.2a — Coupled rigid-body 6-DOF propagation"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('plant_fidelity/Coupled rigid-body 6-DOF propagation')


from typing import Sequence, Dict, Any, Optional
import math


def _flatten(values):
    try:
        items = iter(values) if not isinstance(values, (bytes, str)) else None
    except TypeError:
        items = None
    if items is None:
        yield float(values)
    else:
        for item in items:
            yield from _flatten(item)


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _identity(size):
    return [[float(i == j) for j in range(size)] for i in range(size)]


def _inverse(matrix):
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square")
    rows = [list(map(float, row)) + unit for row, unit in zip(matrix, _identity(size))]
    for col in range(size):
        pivot = max(range(col, size), key=lambda i: abs(rows[i][col]))
        if rows[pivot][col] == 0:
            raise ValueError("matrix is singular")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x / scale for x in rows[col]]
        for i in range(size):
            if i != col:
                factor = rows[i][col]
                rows[i] = [x - factor*y for x, y in zip(rows[i], rows[col])]
    return [row[size:] for row in rows]


def _as_vec(x: Sequence[float], n: int, name: str) -> list[float]:
    arr = list(_flatten(x))
    if len(arr) != n:
        raise ValueError(f"{name} must have shape ({n},), got {len(arr)}")
    return arr


def _normalize_quaternion(q: list[float]) -> list[float]:
    norm = math.hypot(*q)
    if norm <= 0.0:
        raise ValueError("quaternion norm must be positive")
    return [v / norm for v in q]


def _quat_to_rotation(q: list[float]) -> list[list[float]]:
    q0, q1, q2, q3 = q
    return [
        [1.0 - 2.0 * (q2**2 + q3**2), 2.0 * (q1*q2 - q0*q3), 2.0 * (q1*q3 + q0*q2)],
        [2.0 * (q1*q2 + q0*q3), 1.0 - 2.0 * (q1**2 + q3**2), 2.0 * (q2*q3 - q0*q1)],
        [2.0 * (q1*q3 - q0*q2), 2.0 * (q2*q3 + q0*q1), 1.0 - 2.0 * (q1**2 + q2**2)],
    ]


def _omega_matrix(omega: list[float]) -> list[list[float]]:
    wx, wy, wz = omega
    return [
        [0.0, -wx, -wy, -wz],
        [wx, 0.0, wz, -wy],
        [wy, -wz, 0.0, wx],
        [wz, wy, -wx, 0.0],
    ]


def compute_rigid_body_6dof_step(
    position: Sequence[float],
    velocity: Sequence[float],
    quaternion: Sequence[float],
    omega: Sequence[float],
    mass: float,
    inertia: Sequence[Sequence[float]],
    body_force: Sequence[float],
    body_torque: Sequence[float],
    dt: float,
    env_force: Optional[Sequence[float]] = _policy.default,
    env_torque: Optional[Sequence[float]] = _policy.default,
    gravity: Optional[Sequence[float]] = _policy.default,
) -> Dict[str, Any]:
    """Advance a rigid-body state by one explicit integration step."""
    if mass <= 0.0:
        raise ValueError("mass must be positive")
    if dt <= 0.0:
        raise ValueError("dt must be positive")

    r = _as_vec(position, 3, "position")
    v = _as_vec(velocity, 3, "velocity")
    q = _normalize_quaternion(_as_vec(quaternion, 4, "quaternion"))
    w = _as_vec(omega, 3, "omega")
    f_b = _as_vec(body_force, 3, "body_force")
    tau_b = _as_vec(body_torque, 3, "body_torque")
    f_env = [0.0]*3 if env_force is None else _as_vec(env_force, 3, "env_force")
    tau_env = [0.0]*3 if env_torque is None else _as_vec(env_torque, 3, "env_torque")
    g = [0.0]*3 if gravity is None else _as_vec(gravity, 3, "gravity")

    J = [list(row) for row in inertia]
    if len(J) != 3 or any(len(row) != 3 for row in J):
        raise ValueError("inertia must have shape (3, 3)")
    force = _matvec(_quat_to_rotation(q), f_b)
    accel = [(f + env)/mass + gravity_i for f, env, gravity_i in zip(force, f_env, g)]
    lx, ly, lz = _matvec(J, w)
    wx, wy, wz = w
    gyroscopic = [wy*lz - wz*ly, wz*lx - wx*lz, wx*ly - wy*lx]
    torque = [a + b - c for a, b, c in zip(tau_b, tau_env, gyroscopic)]
    omega_dot = _matvec(_inverse(J), torque)
    quaternion_rate = _matvec(_omega_matrix(w), q)

    r_next = [x + dt*y for x,y in zip(r, v)]
    v_next = [x + dt*y for x,y in zip(v, accel)]
    w_next = [x + dt*y for x,y in zip(w, omega_dot)]
    q_next = _normalize_quaternion([x + 0.5*dt*y for x,y in zip(q, quaternion_rate)])

    return {
        "position": r_next,
        "velocity": v_next,
        "quaternion": q_next,
        "omega": w_next,
        "linear_acceleration": accel,
        "angular_acceleration": omega_dot,
    }


__all__ = ['compute_rigid_body_6dof_step']

_policy.bind(globals())
