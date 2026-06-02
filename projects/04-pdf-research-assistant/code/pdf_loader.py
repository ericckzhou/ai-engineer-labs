"""pdf_loader.py — [provided] Parse a PDF to text. NOT the learning target.

PDF parsing is plumbing, not RAG. This wraps `pypdf` so the rest of the pipeline gets plain text, and
ships a small in-memory SAMPLE_DOC so you (and the offline tests) can build the whole pipeline without a
real PDF on disk. The learning targets are chunking, grounded generation, citation, and faithfulness —
not text extraction.

Run:  python pdf_loader.py path/to/file.pdf      (or no arg → prints the sample doc)
"""
from __future__ import annotations

import sys

# A tiny, self-contained "document" so the pipeline + tests run with zero files and zero network.
SAMPLE_DOC = (
    "Acme Corp Q3 Report. "
    "Q3 revenue was 4.2 million dollars, up 8 percent year over year. "
    "Operating margin held steady at 21 percent. "
    "The company opened a new engineering office in Berlin in July. "
    "Headcount grew from 180 to 215 employees during the quarter. "
    "Management reaffirmed full-year guidance of 17 million dollars in revenue."
)


def load_pdf(path: str) -> str:
    """Extract text from a PDF file as one string (pages joined by newlines).

    Example:
        load_pdf("report.pdf")  ->  "Q3 revenue was ...\\n..."   # all page text, concatenated
    """
    from pypdf import PdfReader  # lazy: importing this module shouldn't require pypdf installed

    reader = PdfReader(path)
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def main() -> None:
    if len(sys.argv) > 1:
        text = load_pdf(sys.argv[1])
        print(f"Project 04 — PDF Loader. Extracted {len(text)} chars from {sys.argv[1]}")
    else:
        print("Project 04 — PDF Loader (no file given; showing SAMPLE_DOC)")
        print(SAMPLE_DOC)


if __name__ == "__main__":
    main()
