# Architecture — Palantir Foundry Ontology Simulation

**NOT a Foundry tenant.** Local YAML ontology + pandas transforms only.

```mermaid
flowchart LR
  RAW[CSV sources] --> OS[OntologyStore objects]
  OS --> LINKS[Link materialization]
  LINKS --> TX[Transforms pipeline]
  TX --> DER[data/derived KPIs]
```

Objects: Patient, Encounter, Asset. Links: PatientHasEncounter, SiteAlignsAsset.
