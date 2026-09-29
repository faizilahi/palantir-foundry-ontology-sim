"""Foundry-style transform pipeline over ontology (local pandas transforms)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from ontology_store import OntologyStore

ROOT = Path(__file__).resolve().parents[1]


def run_transforms(store: OntologyStore, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    enc = store.links["PatientHasEncounter"]
    patient_summary = (
        enc.groupby(["patient_id", "risk_tier", "primary_site"], as_index=False)
        .agg(encounter_count=("encounter_id", "count"), total_cost_usd=("cost_usd", "sum"))
    )
    high_risk = patient_summary[patient_summary["risk_tier"] == "HIGH"].sort_values(
        "total_cost_usd", ascending=False
    )
    patient_summary.to_csv(out_dir / "patient_cost_summary.csv", index=False)
    high_risk.head(25).to_csv(out_dir / "high_risk_top_spenders.csv", index=False)
    dept = enc.groupby("department", as_index=False).agg(total_cost=("cost_usd", "sum"))
    dept.to_csv(out_dir / "department_spend.csv", index=False)


def main() -> None:
    raw = ROOT / "data" / "raw"
    schema = ROOT / "ontology" / "schema.yaml"
    store = OntologyStore.from_schema(schema, raw)
    out = ROOT / "data" / "derived"
    run_transforms(store, out)
    print("Ontology sim pipeline complete. Object counts:", store.object_count())
    print(f"Derived CSVs in {out}")


if __name__ == "__main__":
    main()
