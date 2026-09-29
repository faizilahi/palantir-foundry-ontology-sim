import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from objects import load_object_defs, load_objects
from links import validate_links
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    defs = load_object_defs(ROOT / "ontology" / "objects.json")
    objs = load_objects(DATA)
    links = pd.read_csv(DATA / "encounter_bed_link.csv")
    v = validate_links(objs["Encounter"], objs["Bed"], links)
    sql_total = int(objs["Encounter"]["length_of_stay_hours"].sum())
    screen = links.merge(objs["Encounter"], on="encounter_id")
    screen_total = int(screen["length_of_stay_hours"].sum())
    summary = {
        "simulation_only": True,
        "not_a_foundry_tenant": True,
        "objects": defs["objects"],
        **v,
        "screen_total_los_hours": screen_total,
        "sql_total_los_hours": sql_total,
        "delta": screen_total - sql_total,
    }
    pd.DataFrame([summary]).to_csv(OUT / "screen_vs_sql.csv", index=False)
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
