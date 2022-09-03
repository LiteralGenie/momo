import dataclasses
import gzip
import json
from classes.va_scc import VaScc
from config import paths

data = VaScc.from_csv(paths.DATA_DIR / "va_scc.csv")
data = [dataclasses.asdict(x) for x in data]

with gzip.open(paths.DATA_DIR / "va_scc.json.gz", "wt") as file:
    file.write(json.dumps(data))
