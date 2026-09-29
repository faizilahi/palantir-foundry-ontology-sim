import json
from pathlib import Path
import pandas as pd

def load_object_defs(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def load_objects(data: Path) -> dict:
    return {
        "Encounter": pd.read_csv(data / "encounter.csv"),
        "Bed": pd.read_csv(data / "bed.csv"),
        "Department": pd.read_csv(data / "department.csv"),
    }
