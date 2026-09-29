"""Synthetic healthcare / ops data for Foundry-style ontology lab (NOT a real tenant)."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(7)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    n_patients = 400
    patients = pd.DataFrame(
        {
            "patient_id": [f"P{i:05d}" for i in range(1, n_patients + 1)],
            "full_name": [f"Patient {i}" for i in range(1, n_patients + 1)],
            "risk_tier": RNG.choice(["LOW", "MEDIUM", "HIGH"], n_patients),
            "primary_site": RNG.choice(["North Clinic", "South Clinic", "Telehealth"], n_patients),
        }
    )
    encounters = []
    for pid in patients["patient_id"]:
        for _ in range(int(RNG.integers(1, 5))):
            encounters.append(
                {
                    "encounter_id": f"E{RNG.integers(100000, 999999)}",
                    "patient_id": pid,
                    "encounter_date": (
                        pd.Timestamp("2024-03-01") + pd.Timedelta(days=int(RNG.integers(0, 180)))
                    ).date().isoformat(),
                    "department": RNG.choice(["ED", "IP", "OP", "LAB"]),
                    "cost_usd": round(float(RNG.uniform(120, 8500)), 2),
                }
            )
    enc = pd.DataFrame(encounters).drop_duplicates(subset=["encounter_id"])

    assets = pd.DataFrame(
        {
            "asset_id": [f"A{i:04d}" for i in range(1, 51)],
            "asset_type": RNG.choice(["MRI", "CT", "INFUSION_PUMP", "VENTILATOR"], 50),
            "site": RNG.choice(["North Clinic", "South Clinic"], 50),
            "status": RNG.choice(["ACTIVE", "MAINTENANCE", "RETIRED"], 50, p=[0.8, 0.15, 0.05]),
        }
    )

    patients.to_csv(args.out_dir / "patients.csv", index=False)
    enc.to_csv(args.out_dir / "encounters.csv", index=False)
    assets.to_csv(args.out_dir / "assets.csv", index=False)
    print(f"Wrote patients, encounters, assets to {args.out_dir}")


if __name__ == "__main__":
    main()
