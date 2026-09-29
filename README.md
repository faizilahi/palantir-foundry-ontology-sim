# Hospital Ops Ontology (Local Simulation)

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

Local simulation of Foundry-style ontology objects for a hospital operations
review. **Not a Foundry tenant** — no Palantir cloud, no AIP service calls.

## Objects

`Encounter`, `Bed`, `Department`, `StaffShift` defined in `ontology/objects.json`.

## Links

Encounter→Bed, Encounter→Department, StaffShift→Department. Link integrity
checked in `src/links.py`.

## The screen total vs the SQL total

The ops screen summed `encounter.length_of_stay_hours` across open encounters
and showed **13,168**. SQL at grain `encounter_id` (deduped links) shows
**11,760** — the screen double-counted encounters with bed transfers (**48**
transfers × avg 15h fanout artifact).

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_ontology.py
```
