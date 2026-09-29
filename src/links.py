import pandas as pd

def validate_links(encounters, beds, links) -> dict:
    orphan = links[~links["bed_id"].isin(beds["bed_id"])]
    multi = links.groupby("encounter_id").size().reset_index(name="n")
    transfers = multi[multi["n"] > 1]
    return {
        "orphan_bed_links": int(len(orphan)),
        "encounters_with_transfer_links": int(len(transfers)),
        "link_rows": int(len(links)),
    }
