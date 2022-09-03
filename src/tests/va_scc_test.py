from pathlib import Path
from typing import Callable

import pytest
from classes.va_scc import VaScc

CsvGenerator = Callable[[], Path]


def test_parse(tmp_path: Path):
    """Parse a valid file, expecting no errors"""

    file_contents = """Entity ID,Entity Name,Name Type,Entity Type,Principal Office Address,RA Name,Status
111,,Fictitious Name,Nonstock Corporation,"5555 Whatever Dr, Nowhere, VA, 88888 - 7777, USA",Doctor Who,Active,"""

    tmp_file = tmp_path / "file.csv"
    tmp_file.write_text(file_contents)

    VaScc.from_csv(tmp_file)


class TestHeaderCheck:
    headers: list[str]
    lines: list[str]

    @pytest.fixture(autouse=True)
    def _init(self):
        # Default to real headers
        self.headers = [
            "Entity ID",
            "Entity Name",
            "Name Type",
            "Entity Type",
            "Principal Office Address",
            "RA Name",
            "Status",
        ].copy()

        # Default body
        self.lines = [",".join(self.headers)]

    @pytest.fixture()
    def create_csv(self, tmp_path: Path) -> CsvGenerator:
        """Create temporary .csv file with fake data"""

        def create():
            header_line = ",".join(self.headers)
            file_contents = [header_line] + self.lines
            file_contents = "\n".join(file_contents) + "\n"

            tmp_file = tmp_path / "file.csv"
            tmp_file.write_text(file_contents)

            return tmp_file

        return create

    def test_header_change(self, create_csv: CsvGenerator):
        """Rename a header, expecting AssertionError"""

        self.headers[1] = "zzz"
        tmp_file = create_csv()

        with pytest.raises(AssertionError):
            VaScc.from_csv(tmp_file)

    def test_header_order(self, create_csv: CsvGenerator):
        """Swap two headers, expecting no errors"""

        [self.headers[1], self.headers[0]] = self.headers[:2]
        tmp_file = create_csv()

        VaScc.from_csv(tmp_file)

    def test_header_extra(self, create_csv: CsvGenerator):
        """Add extra header, expecting AssertionError"""

        self.headers.append("lmao")
        tmp_file = create_csv()

        with pytest.raises(AssertionError):
            VaScc.from_csv(tmp_file)

    def test_header_missing(self, create_csv: CsvGenerator):
        """Remove header, expecting AssertionError"""

        self.headers.pop(1)
        tmp_file = create_csv()

        with pytest.raises(AssertionError):
            VaScc.from_csv(tmp_file)
