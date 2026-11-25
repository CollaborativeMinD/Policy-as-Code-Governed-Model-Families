# actuator_power_authority

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.actuator_power_authority.md`

## Why this family exists
Whether actuation remains safe and supportable given current power, thermal, and bus conditions.

## Cross-domain use cases
servo bus sag; thruster enable gating; wheel motor derate; fin actuation under thermal/power stress.

## Optimal use
Use when commands can themselves collapse the substrate or when derate shrinks the actuator envelope.

## Do not use when
Do not use without the matching electrical and thermal truths that define the envelope.

## Canonical formulas in this family

- **ACT-PWR-001** `act_pwr_001__actuator_power_authority__actuation_enable_authority_gate.py`: Actuation Enable Authority Gate
  - Symbolic form: `actuate_ok = power_valid ∧ actuator_bus_valid ∧ thermal_valid ∧ state_valid ∧ valid_for_use ∧ ¬fault_latched`
  - Why kept: Hard actuation enable gate tied to power truth is broadly reusable and fail-closed.
- **ACT-PWR-002** `act_pwr_002__actuator_power_authority__actuator_induced_bus_sag_closure.py`: Actuator-Induced Bus Sag Closure
  - Symbolic form: `ΔV = I_step R_eq + L_eq dI/dt; m_sag = (V_pre - ΔV) - V_hold`
  - Why kept: Portable sag-closure margin for any actuator that can collapse the bus it depends on.
- **ACT-PWR-003** `act_pwr_003__actuator_power_authority__thermal_voltage_derated_actuator_envelope.py`: Thermal Voltage Derated Actuator Envelope
  - Symbolic form: `u_derated = u_nom · min(f_thermal(T), f_voltage(V_bus))`
  - Why kept: Cross-domain derated actuator envelope useful for any electromechanical actuator under substrate stress.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
