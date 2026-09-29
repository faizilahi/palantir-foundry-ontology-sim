"""In-memory ontology object store — LOCAL SIMULATION, not Foundry."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


@dataclass
class OntologyStore:
    objects: dict[str, pd.DataFrame] = field(default_factory=dict)
    links: dict[str, pd.DataFrame] = field(default_factory=dict)
    schema: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_schema(cls, schema_path: Path, raw_dir: Path) -> "OntologyStore":
        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        store = cls(schema=schema)
        for name, spec in schema.get("objects", {}).items():
            pk = spec["primary_key"]
            path = raw_dir / f"{name.lower()}s.csv" if name != "Patient" else raw_dir / "patients.csv"
            if name == "Encounter":
                path = raw_dir / "encounters.csv"
            elif name == "Asset":
                path = raw_dir / "assets.csv"
            df = pd.read_csv(path)
            df.attrs["primary_key"] = pk
            store.objects[name] = df
        store._materialize_links()
        return store

    def _materialize_links(self) -> None:
        patients = self.objects["Patient"]
        encounters = self.objects["Encounter"]
        link_pe = encounters.merge(
            patients[["patient_id", "primary_site", "risk_tier"]], on="patient_id", how="left"
        )
        self.links["PatientHasEncounter"] = link_pe
        assets = self.objects["Asset"]
        site_link = patients.merge(assets, left_on="primary_site", right_on="site", how="inner")
        self.links["SiteAlignsAsset"] = site_link

    def object_count(self) -> dict[str, int]:
        return {k: len(v) for k, v in self.objects.items()}
