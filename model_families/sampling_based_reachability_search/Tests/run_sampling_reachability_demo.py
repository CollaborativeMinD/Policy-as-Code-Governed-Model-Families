#!/usr/bin/env python3
"""Run the executable reachability model.

Usage:
    python run_reachability_demo.py
"""
from __future__ import annotations

import json

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sampling_based_reachability import (
    SamplingReachabilitySearch,
    demo_blocked_path_config,
    demo_clear_path_config,
    run_campaign,
)


def main() -> None:
    clear = SamplingReachabilitySearch(demo_clear_path_config(seed=7)).run()
    blocked = SamplingReachabilitySearch(demo_blocked_path_config(seed=7)).run()
    campaign = run_campaign(demo_clear_path_config(seed=i) for i in range(12))

    print("CLEAR_PATH_STATUS:", clear.status)
    print("CLEAR_PATH_SUCCESS:", clear.success)
    print("CLEAR_PATH_ACCEPTED_NODES:", clear.telemetry["accepted_nodes"])
    print("CLEAR_PATH_REJECTED_NODES:", clear.telemetry["rejected_nodes"])
    print("CLEAR_PATH_LENGTH:", clear.telemetry["path_length"])

    print("BLOCKED_PATH_STATUS:", blocked.status)
    print("BLOCKED_PATH_SUCCESS:", blocked.success)
    print("BLOCKED_PATH_ACCEPTED_NODES:", blocked.telemetry["accepted_nodes"])
    print("BLOCKED_PATH_REJECTED_NODES:", blocked.telemetry["rejected_nodes"])
    print("BLOCKED_COLLAPSE_PRESSURE:", blocked.telemetry["collapse_pressure"])

    print("CAMPAIGN_SUMMARY:")
    print(json.dumps(
        {
            "campaign_count": campaign["campaign_count"],
            "success_count": campaign["success_count"],
            "success_probability": campaign["success_probability"],
            "collapse_dominant_count": campaign["collapse_dominant_count"],
            "collapse_dominant_probability": campaign["collapse_dominant_probability"],
        },
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
