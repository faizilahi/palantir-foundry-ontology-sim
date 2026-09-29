from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(11760)
depts = pd.DataFrame({"department_id": [f"D{i}" for i in range(1, 6)],
                      "department_name": ["ED", "MedSurg", "ICU", "OR", "StepDown"]})
beds = pd.DataFrame({"bed_id": [f"B{i:03d}" for i in range(1, 121)],
                     "department_id": [f"D{(i % 5) + 1}" for i in range(1, 121)]})
# 400 encounters; 48 have 2 bed links (transfers)
enc = []
links = []
for i in range(400):
    eid = f"E{i:04d}"
    los = int(RNG.integers(4, 72))
    enc.append({"encounter_id": eid, "length_of_stay_hours": los, "status": "OPEN",
                "department_id": f"D{(i % 5) + 1}"})
    links.append({"encounter_id": eid, "bed_id": f"B{(i % 120) + 1:03d}", "link": "occupies"})
    if i < 48:
        links.append({"encounter_id": eid, "bed_id": f"B{((i + 3) % 120) + 1:03d}", "link": "occupies"})
# scale LOS so unique sum = 11760 and screen (fanned) = 12480
enc = pd.DataFrame(enc)
factor = 11760 / enc.length_of_stay_hours.sum()
enc["length_of_stay_hours"] = (enc["length_of_stay_hours"] * factor).round().astype(int)
drift = 11760 - int(enc.length_of_stay_hours.sum())
enc.iloc[-1, enc.columns.get_loc("length_of_stay_hours")] += drift
depts.to_csv(DATA / "department.csv", index=False)
beds.to_csv(DATA / "bed.csv", index=False)
enc.to_csv(DATA / "encounter.csv", index=False)
pd.DataFrame(links).to_csv(DATA / "encounter_bed_link.csv", index=False)
print("enc", len(enc), "links", len(links), "sql_total", enc.length_of_stay_hours.sum())
