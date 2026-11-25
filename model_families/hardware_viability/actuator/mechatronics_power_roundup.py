"""Deterministic mechatronics-power formula primitives for network keep/cut/merge review."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/mechatronics_power_roundup')


from itertools import combinations
from math import exp
from typing import Sequence


@_policy.record(frozen=True)
class GateResult:
    pass


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def pbr001_min_hold_up_time_closure(
    c_eff_f: float,
    v_start_v: float,
    v_bor_v: float,
    p_crit_w: float,
    t_inhibit_s: float,
    t_log_s: float,
    t_reset_s: float,
) -> GateResult:
    if p_crit_w <= 0:
        raise ValueError('p_crit_w must be > 0')
    if v_start_v < v_bor_v:
        raise ValueError('v_start_v must be >= v_bor_v')
    t_hold = (c_eff_f * (v_start_v**2 - v_bor_v**2)) / (2.0 * p_crit_w)
    required = t_inhibit_s + t_log_s + t_reset_s
    return GateResult(value=t_hold - required, passed=t_hold >= required)


def pbr002_brownout_entry_guard(
    v_bus_v: float,
    v_fall_v: float,
    dt_below_s: float,
    tau_confirm_s: float,
    dv_bus_dt_v_per_s: float,
    gamma_drop_v_per_s: float,
) -> bool:
    return ((v_bus_v <= v_fall_v) and (dt_below_s >= tau_confirm_s)) or (
        dv_bus_dt_v_per_s <= -abs(gamma_drop_v_per_s)
    )


def pbr003_stable_restart_gate(
    v_bus_v: float,
    v_rise_v: float,
    sigma_v: float,
    sigma_max: float,
    dv_bus_dt_v_per_s: float,
    gamma_settle_v_per_s: float,
    dt_above_s: float,
    tau_stable_s: float,
) -> bool:
    return (
        (v_bus_v >= v_rise_v)
        and (sigma_v <= sigma_max)
        and (abs(dv_bus_dt_v_per_s) <= abs(gamma_settle_v_per_s))
        and (dt_above_s >= tau_stable_s)
    )


def pbr004_rail_coherence_index(voltages_v: Sequence[float], v_nom_v: float, rho_max: float) -> GateResult:
    if len(voltages_v) < 2:
        raise ValueError('Need at least two rail voltages')
    if v_nom_v <= 0:
        raise ValueError('v_nom_v must be > 0')
    rho = max(abs(a - b) / v_nom_v for a, b in combinations(voltages_v, 2))
    return GateResult(value=rho, passed=rho <= rho_max)


def ptt001_tau_valid(dv_bus_dt_abs_v_per_s: float, tau_base_s: float, k_dv_s2_per_v: float, state_factor: float) -> float:
    if tau_base_s <= 0 or state_factor <= 0:
        raise ValueError('tau_base_s and state_factor must be > 0')
    return tau_base_s * state_factor / (1.0 + k_dv_s2_per_v * max(0.0, dv_bus_dt_abs_v_per_s))


def ptt001_power_telemetry_freshness_at_use_gate(
    t_use_s: float,
    t_stamp_s: float,
    dv_bus_dt_abs_v_per_s: float,
    tau_base_s: float,
    k_dv_s2_per_v: float,
    state_factor: float,
) -> GateResult:
    age = t_use_s - t_stamp_s
    tau_valid = ptt001_tau_valid(dv_bus_dt_abs_v_per_s, tau_base_s, k_dv_s2_per_v, state_factor)
    return GateResult(value=age - tau_valid, passed=age <= tau_valid)


def paa001_actuation_enable_authority_gate(
    power_valid: bool,
    actuator_bus_valid: bool,
    thermal_valid: bool,
    state_valid: bool,
    fault_latched: bool,
    valid_for_use: bool,
) -> bool:
    return all([power_valid, actuator_bus_valid, thermal_valid, state_valid, valid_for_use]) and (not fault_latched)


def paa002_actuator_induced_bus_sag_closure(
    i_step_a: float,
    r_eq_ohm: float,
    l_eq_h: float,
    di_dt_a_per_s: float,
    v_pre_v: float,
    v_hold_v: float,
) -> GateResult:
    delta_v = i_step_a * r_eq_ohm + l_eq_h * di_dt_a_per_s
    v_post = v_pre_v - delta_v
    return GateResult(value=v_post - v_hold_v, passed=v_post >= v_hold_v)


def paa003_thermal_voltage_derated_actuator_envelope(
    u_nom: float,
    t_core_c: float,
    t_warn_c: float,
    t_crit_c: float,
    v_bus_v: float,
    v_min_v: float,
    v_nom_v: float,
) -> float:
    if t_crit_c <= t_warn_c:
        raise ValueError('t_crit_c must exceed t_warn_c')
    if v_nom_v <= v_min_v:
        raise ValueError('v_nom_v must exceed v_min_v')
    thermal_factor = (t_crit_c - t_core_c) / (t_crit_c - t_warn_c)
    voltage_factor = (v_bus_v - v_min_v) / (v_nom_v - v_min_v)
    factor = clamp(min(thermal_factor, voltage_factor), 0.0, 1.0)
    return u_nom * factor


def paa004_safe_reenable_delay(
    t_sensor_settle_s: float,
    t_estimator_lock_s: float,
    t_bus_stable_s: float,
    t_clock_sync_s: float,
    t_fault_clear_s: float,
) -> float:
    return max(t_sensor_settle_s, t_estimator_lock_s, t_bus_stable_s, t_clock_sync_s, t_fault_clear_s)


def tpd001_two_node_thermal_rc_step(
    t_core_c: float,
    t_sink_c: float,
    t_amb_c: float,
    p_loss_w: float,
    c_core_j_per_c: float,
    c_sink_j_per_c: float,
    r_cs_c_per_w: float,
    r_sa_c_per_w: float,
    dt_s: float,
) -> tuple[float, float]:
    dcore_dt = (p_loss_w - (t_core_c - t_sink_c) / r_cs_c_per_w) / c_core_j_per_c
    dsink_dt = (((t_core_c - t_sink_c) / r_cs_c_per_w) - ((t_sink_c - t_amb_c) / r_sa_c_per_w)) / c_sink_j_per_c
    return (t_core_c + dcore_dt * dt_s, t_sink_c + dsink_dt * dt_s)


def tpd002_thermal_timing_derate(
    wcet_nom_s: float,
    t_core_c: float,
    t_ref_c: float,
    k_t_per_c: float,
    t_budget_s: float,
) -> GateResult:
    wcet_eff = wcet_nom_s * (1.0 + k_t_per_c * max(0.0, t_core_c - t_ref_c))
    return GateResult(value=t_budget_s - wcet_eff, passed=wcet_eff <= t_budget_s)


def tpd003_thermal_distortion_confidence_ceiling(
    conf_nom: float,
    k_conf_per_c: float,
    t_core_c: float,
    t_cal_c: float,
) -> float:
    return conf_nom * exp(-k_conf_per_c * max(0.0, t_core_c - t_cal_c))


def ecl001_energy_continuity_margin(
    e_avail: float,
    eta_gen: float,
    p_gen_profile_w: Sequence[float],
    p_load_profile_w: Sequence[float],
    dt_s: float,
    e_reserve: float,
    e_req: float,
) -> float:
    if e_req <= 0 or dt_s <= 0:
        raise ValueError('e_req and dt_s must be > 0')
    if len(p_gen_profile_w) != len(p_load_profile_w):
        raise ValueError('profiles must be same length')
    e_gen = sum(eta_gen * p for p in p_gen_profile_w) * dt_s
    e_load = sum(p_load_profile_w) * dt_s
    return (e_avail + e_gen - e_load - e_reserve) / e_req


def ecl002_regulation_chain_delivery_margin(
    p_src_w: float,
    eta_stages: Sequence[float],
    p_parasitic_w: float,
    p_demand_w: float,
) -> GateResult:
    if p_demand_w <= 0:
        raise ValueError('p_demand_w must be > 0')
    p_delivered = p_src_w
    for eta in eta_stages:
        p_delivered *= eta
    margin = (p_delivered - p_parasitic_w - p_demand_w) / p_demand_w
    return GateResult(value=margin, passed=margin >= 0.0)


def ecl003_priority_load_shed_optimization(
    utilities: Sequence[float],
    powers_w: Sequence[float],
    p_avail_w: float,
    p_reserve_w: float,
    critical_indices: Sequence[int] = _policy.default,
    prohibited_indices: Sequence[int] = _policy.default,
) -> tuple[list[int], float]:
    if not (len(utilities) == len(powers_w)):
        raise ValueError('utilities and powers_w must match')
    n = len(utilities)
    keep = set(critical_indices)
    prohibited = set(prohibited_indices)
    remaining = [i for i in range(n) if i not in keep and i not in prohibited]
    capacity = p_avail_w - p_reserve_w - sum(powers_w[i] for i in keep)
    if capacity < 0:
        return (sorted(keep), sum(utilities[i] for i in keep))
    best_set = set(keep)
    best_utility = sum(utilities[i] for i in keep)
    from itertools import combinations
    for r in range(len(remaining)+1):
        for subset in combinations(remaining, r):
            p = sum(powers_w[i] for i in subset)
            if p <= capacity:
                u = sum(utilities[i] for i in subset) + sum(utilities[i] for i in keep)
                if u > best_utility:
                    best_utility = u
                    best_set = set(keep).union(subset)
    return (sorted(best_set), best_utility)

_policy.bind(globals())
