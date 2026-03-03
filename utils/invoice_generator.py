"""Utility for creating PDF invoices with tables and a logo.

This module uses ReportLab (https://www.reportlab.com/) to generate a PDF
file containing invoice details, line items, totals and an optional logo.

Install the dependency with ``pip install reportlab`` and add it to
``requirements.txt`` if you want it available in production.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Dict, List, Optional, Union

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generate_invoice(
    invoice_data: Dict,
    output_file: Union[str, Path],
    logo_path: Optional[Union[str, Path]] = None,
    page_size=A4,
) -> None:
    """Generate a PDF invoice.

    ``invoice_data`` should be a dictionary containing at least the keys
    ``"from"``, ``"to"``, ``"number"`` and ``"date"`` with string values
    and ``"items"`` with a list of line-item dictionaries.  Each line item
    should have ``"description"``, ``"quantity"`` and ``"unit_price"``.

    Additional optional fields like ``"terms"`` or ``"notes"`` may be
    supplied and will be appended to the bottom of the invoice.

    ``output_file`` is the filename or ``Path`` where the PDF will be written.
    ``logo_path`` may be ``None`` or a path to an image file to be displayed
    at the top of the document.  ``page_size`` can be changed to ``letter``
    (imported above) if desired.
    """

    doc = SimpleDocTemplate(str(output_file), pagesize=page_size, rightMargin=72,
                            leftMargin=72, topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = styles["Heading1"]

    elements: List = []

    # logo
    if logo_path:
        try:
            img = Image(str(logo_path))
            img.drawHeight = 1 * inch
            img.drawWidth = 1 * inch
            elements.append(img)
            elements.append(Spacer(1, 12))
        except Exception as e:
            # if image loading fails, we just ignore it
            elements.append(Paragraph(f"<b>Logo could not be loaded:</b> {e}", normal))
            elements.append(Spacer(1, 12))

    # heading
    elements.append(Paragraph("Invoice", heading))
    elements.append(Spacer(1, 12))

    # from/to/number/date
    from_text = invoice_data.get("from", "")
    to_text = invoice_data.get("to", "")
    number = invoice_data.get("number", "")
    date = invoice_data.get("date", "")

    header_table_data = [
        [Paragraph(f"<b>From:</b><br/>{from_text}", normal),
         Paragraph(f"<b>To:</b><br/>{to_text}", normal)],
        [Paragraph(f"<b>Invoice #:</b> {number}", normal),
         Paragraph(f"<b>Date:</b> {date}", normal)],
    ]
    header_table = Table(header_table_data, hAlign="LEFT")
    elements.append(header_table)
    elements.append(Spacer(1, 24))

    # items table
    items = invoice_data.get("items", [])
    table_data = [["Description", "Qty", "Unit Price", "Total"]]
    grand_total = 0

    for item in items:
        desc = item.get("description", "")
        qty = item.get("quantity", 0)
        unit = item.get("unit_price", 0)
        total = qty * unit
        grand_total += total
        table_data.append([desc, str(qty), f"${unit:,.2f}", f"${total:,.2f}"])

    # add total row
    table_data.append(["", "", Paragraph("<b>Grand Total</b>", normal),
                       Paragraph(f"<b>${grand_total:,.2f}</b>", normal)])

    invoice_table = Table(table_data, colWidths=[3 * inch, inch, inch, inch])
    invoice_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ]
        )
    )
    elements.append(invoice_table)
    elements.append(Spacer(1, 24))

    # optional notes/terms
    for key in ("terms", "notes"):
        if key in invoice_data:
            elements.append(Paragraph(f"<b>{key.capitalize()}:</b> {invoice_data[key]}", normal))
            elements.append(Spacer(1, 12))

    doc.build(elements)


if __name__ == "__main__":
    # simple CLI usage example
    sample = {
        "from": "Acme Corp, 123 Elm St",
        "to": "John Doe, 456 Oak Ave",
        "number": "1001",
        "date": "2026-03-03",
        "items": [
            {"description": "Widget", "quantity": 2, "unit_price": 9.99},
            {"description": "Gadget", "quantity": 1, "unit_price": 19.99},
        ],
        "terms": "Payment due within 30 days",
    }
    generate_invoice(sample, "invoice.pdf", logo_path=None)
