from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/recovery_time_inflation')


from typing import Any
from types import MappingProxyType
import math

PHASE_LABELS = MappingProxyType({
    0: 'NOMINAL_RECOVERY',
    1: 'GRACEFUL_DEGRADATION',
    2: 'LAWFUL_RECOVERY_PRESSURE',
    3: 'ESCROW_OR_TERMINAL_REQUIRED',
})


@_policy.record(frozen=True, kw_only=True)
class RecoveryTimeInflationConfig:

    def __post_init__(self):
        for name in vars(self):
            object.__setattr__(self, name, float(getattr(self, name)))
        


@_policy.record(frozen=True, kw_only=True)
class RecoveryTraceConfig:

    def __post_init__(self):
        for name in ("amplitude", "threshold_abs", "dt_s", "horizon_s"):
            object.__setattr__(self, name, float(getattr(self, name)))
        raw = float(self.dwell_samples)
        if not raw.is_integer():
            raise ValueError("dwell_samples must be an integer")
        object.__setattr__(self, "dwell_samples", int(raw))
        


@_policy.record(frozen=True)
class RecoveryTimeInflationSymbolicContract:
    pass


@_policy.record(frozen=True)
class RecoveryTimeInflationResult:

    def as_dict(self) -> dict[str, Any]:
        return {
            'recovery_time_s': self.recovery_time_s,
            'baseline_recovery_time_s': self.baseline_recovery_time_s,
            'ttv_s': self.ttv_s,
            'rti': self.rti,
            'recovery_margin_s': self.recovery_margin_s,
            'recovery_ratio': self.recovery_ratio,
            'rti_growth_per_s': self.rti_growth_per_s,
            'divergence_pressure': self.divergence_pressure,
            'phase_code': self.phase_code,
            'phase_label': self.phase_label,
            'terminal_required': self.terminal_required,
        }


def _metrics(recovery, baseline, ttv, previous, dt, epsilon, eta, warning, growth_warning, ratio_pressure):
    rti = recovery / max(epsilon, baseline)
    ratio = recovery / max(epsilon, ttv)
    growth = (rti - previous) / max(epsilon, dt)
    terminal = recovery >= ttv
    if terminal:
        phase = 3
    elif ratio >= ratio_pressure:
        phase = 2
    elif rti >= warning or growth > growth_warning:
        phase = 1
    else:
        phase = 0
    return {
        "rti": rti, "recovery_margin": ttv - recovery, "recovery_ratio": ratio,
        "rti_growth": growth, "phase_code": phase, "terminal_flag": int(terminal),
        "divergence_pressure": max(0, recovery-baseline) / max(epsilon, ttv) + eta*max(0, growth),
    }


def build_symbolic_contract() -> RecoveryTimeInflationSymbolicContract:
    """Return expression text, symbol names, and ordered scalar evaluators."""
    names = ("T_rec", "T_rec_0", "TTV_s", "RTI_prev", "dt", "eps", "eta", "RTI_warn", "growth_warn", "ratio_press")
    symbols = {name: name for name in names}
    expressions = {
        "rti": "T_rec / max(eps, T_rec_0)", "recovery_margin": "TTV_s - T_rec",
        "recovery_ratio": "T_rec / max(eps, TTV_s)",
        "rti_growth": "(rti - RTI_prev) / max(eps, dt)",
        "divergence_pressure": "max(0, T_rec - T_rec_0)/max(eps, TTV_s) + eta*max(0, rti_growth)",
        "phase_code": "3 if T_rec >= TTV_s else 2 if recovery_ratio >= ratio_press else 1 if rti >= RTI_warn or rti_growth > growth_warn else 0",
        "terminal_flag": "int(T_rec >= TTV_s)",
    }
    def evaluator(key):
        @_policy.evaluator("build_symbolic_contract.evaluate")
        def evaluate(T_rec, T_rec_0, TTV_s, RTI_prev, dt, eps, eta, RTI_warn, growth_warn, ratio_press):
            return _metrics(T_rec, T_rec_0, TTV_s, RTI_prev, dt, eps, eta, RTI_warn, growth_warn, ratio_press)[key]
        return evaluate
    functions = {key: evaluator(key) for key in expressions}
    latex = {
        'RTI-001': r'RTI = \frac{T_{rec}}{\max(\epsilon, T_{rec,0})}',
        'RTI-002': r'M_{rec} = TTV_s - T_{rec}',
        'RTI-003': r'\dot{RTI}_k = \frac{RTI_k - RTI_{k-1}}{\max(\epsilon, \Delta t)}',
        'RTI-004': r'\mathscr{D}_{\Omega,RTI} = \frac{\max(0,T_{rec}-T_{rec,0})}{\max(\epsilon,TTV_s)} + \eta\max(0,\dot{RTI})',
        'RTI-005': r'T_{rec} \geq TTV_s \Rightarrow V_{term}',
    }

    return RecoveryTimeInflationSymbolicContract(latex=latex, symbols=symbols, expressions=expressions, functions=functions)


_CONTRACT = build_symbolic_contract()


def evaluate_recovery_state(
    *,
    recovery_time_s: float,
    baseline_recovery_time_s: float,
    ttv_s: float,
    previous_rti: float = _policy.default,
    dt_s: float = _policy.default,
    config: RecoveryTimeInflationConfig | None = _policy.default,
) -> RecoveryTimeInflationResult:
    """Evaluate recovery metrics and phase in contract priority order."""

    config = config or RecoveryTimeInflationConfig()
    args = (
        float(recovery_time_s),
        float(baseline_recovery_time_s),
        float(ttv_s),
        float(previous_rti),
        float(dt_s),
        float(config.epsilon_s),
        float(config.divergence_growth_weight),
        float(config.rti_warning_threshold),
        float(config.rti_growth_warning_per_s),
        float(config.recovery_ratio_pressure_threshold),
    )
    metrics = _metrics(*args)
    phase_code = metrics["phase_code"]
    terminal_required = bool(metrics["terminal_flag"])
    return RecoveryTimeInflationResult(
        recovery_time_s=float(recovery_time_s),
        baseline_recovery_time_s=float(baseline_recovery_time_s),
        ttv_s=float(ttv_s),
        rti=metrics["rti"],
        recovery_margin_s=metrics["recovery_margin"],
        recovery_ratio=metrics["recovery_ratio"],
        rti_growth_per_s=metrics["rti_growth"],
        divergence_pressure=metrics["divergence_pressure"],
        phase_code=phase_code,
        phase_label=PHASE_LABELS[phase_code],
        terminal_required=terminal_required,
    )


def deterministic_exponential_recovery_trace(time_s: list[float], *, amplitude: float, tau_s: float) -> list[float]:
    """Deterministic recovery trace y(t)=A exp(-t/tau)."""

    if tau_s <= 0:
        raise ValueError('tau_s must be positive')
    return [amplitude * math.exp(-t / tau_s) for t in time_s]


def theoretical_exponential_recovery_time_s(*, amplitude: float, threshold_abs: float, tau_s: float) -> float:
    """Closed-form settling time for A exp(-t/tau) <= threshold."""

    if not (0 < threshold_abs < amplitude):
        raise ValueError('threshold_abs must be between zero and amplitude')
    if tau_s <= 0:
        raise ValueError('tau_s must be positive')
    return float(tau_s * math.log(amplitude / threshold_abs))


def estimate_recovery_time_s(time_s: list[float], signal: list[float], *, threshold_abs: float, dwell_samples: int = _policy.default) -> float:
    """Return first time where signal remains inside threshold for dwell_samples."""

    if len(time_s) != len(signal):
        raise ValueError('time_s and signal must be same-length 1D arrays')
    if dwell_samples < 1:
        raise ValueError('dwell_samples must be >= 1')
    if len(signal) < dwell_samples:
        raise ValueError("trace shorter than dwell window")
    consecutive = 0
    for i, value in enumerate(signal):
        consecutive = consecutive + 1 if abs(value) <= threshold_abs else 0
        if consecutive == dwell_samples:
            return float(time_s[i - dwell_samples + 1])
    return math.inf


def symbolic_contract() -> RecoveryTimeInflationSymbolicContract:
    return _CONTRACT

_policy.bind(globals())
