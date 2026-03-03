import os
import tempfile

from utils.invoice_generator import generate_invoice


def test_generate_invoice_creates_file():
    data = {
        "from": "Foo",
        "to": "Bar",
        "number": "0001",
        "date": "2026-03-03",
        "items": [{"description": "Test", "quantity": 1, "unit_price": 10.0}],
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "out.pdf")
        generate_invoice(data, path)
        assert os.path.isfile(path)
        assert os.path.getsize(path) > 0
