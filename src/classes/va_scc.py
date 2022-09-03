import csv
from dataclasses import dataclass, fields
from pathlib import Path
from typing import ClassVar

from tqdm import tqdm


@dataclass
class VaScc:
    """Data pulled from https://cis.scc.virginia.gov/"""

    entity_id: str = ""
    entity_name: str = ""
    name_type: str = ""
    entity_type: str = ""
    principal_office_address: str = ""
    ra_name: str = ""
    status: str = ""

    _key_map: ClassVar[dict[str, str]] = {
        "Entity ID": "entity_id",
        "Entity Name": "entity_name",
        "Name Type": "name_type",
        "Entity Type": "entity_type",
        "Principal Office Address": "principal_office_address",
        "RA Name": "ra_name",
        "Status": "status",
    }
    "Maps each CSV header to an attribute"

    def __post_init__(self):
        for f in fields(self):
            # Strip whitespace
            val = getattr(self, f.name)
            if isinstance(val, str):
                val = val.strip()
            setattr(self, f.name, val)

    @classmethod
    def from_csv(cls, fp: Path) -> "list[VaScc]":
        """Convert csv data to list of VaScc instances

        Parameters
        ----------
        fp
            Path to csv

        Returns
        -------
            list of VaScc instances. Unparsable lines trigger a warning and skipped
        """

        ret = []

        raw_lines = fp.read_text().splitlines()
        reader = csv.DictReader(raw_lines)

        # Validate headers
        headers_expected = set(cls._key_map.keys())
        headers_actual = set(reader.fieldnames or [])
        error = f"CSV structure has changed"
        error += f"\nExpected headers {headers_expected}"
        error += f"\nBut got {headers_actual}"
        assert headers_expected == headers_actual, error

        # Parse lines
        # NOTE: CSVReader will silently ignore extraneous values / sprinkle in Nones for missing data,
        #       even with Dialect.strict = True. It would be nice to log warnings / ignore these lines, but whatever.
        for ln in tqdm(reader):
            # Ignore trailing comma
            if None in ln:
                del ln[None]

            # Create instance
            vals = {cls._key_map[k]: v for k, v in ln.items()}
            instance = cls(**vals)
            ret.append(instance)

        return ret
