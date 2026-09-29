from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)
derived = ROOT / "data" / "derived" / "department_spend.csv"
if derived.exists():
    df = pd.read_csv(derived)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df["department"], df["total_cost"], color="#2D72D2")
    ax.set_title("Department spend (ontology transform output)")
    ax.set_ylabel("USD")
    fig.tight_layout()
    fig.savefig(OUT / "department_spend.png", dpi=120)
    plt.close(fig)
    print(f"Wrote {OUT / 'department_spend.png'}")
