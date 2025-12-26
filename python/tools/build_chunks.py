# python/tools/build_chunks.py

import argparse
import json
from pathlib import Path
from typing import List, Dict

import re
from pypdf import PdfReader

from rag.chunker.chunker import SlidingWindowChunker
from rag.model.chunk import Chunk


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pypdf."""
    reader = PdfReader(str(pdf_path))
    parts: List[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def normalize_text(text: str) -> str:
    """
    Normalize PDF extracted text for chunking.
    Goals:
      - Fix hyphenation across line breaks: "başvu-\nru" -> "başvuru"
      - Remove page-number lines like "12 / 45"
      - Convert single newlines to spaces, keep paragraph breaks (double newlines)
      - Collapse excessive whitespace
    """
    if not text:
        return ""

    # Fix hyphenation across line breaks
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Remove page number patterns (common in PDFs)
    text = re.sub(r"\n?\s*\d+\s*/\s*\d+\s*\n?", "\n", text)

    # Reduce very long newline runs
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Convert single newlines to spaces (preserve paragraph breaks)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Collapse whitespace (spaces/tabs)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()


def chunk_to_json_record(c: Chunk) -> Dict:
    """Convert internal Chunk object -> canonical chunks.json record."""
    return {
        "id": c.id,
        "docId": c.doc_id,
        "startOffset": c.start_offset,
        "endOffset": c.end_offset,
        "text": c.text,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build chunks.json from PDFs")
    parser.add_argument("--pdf_dir", type=str, default="resources/pdfs", help="Directory containing PDFs")
    parser.add_argument("--out", type=str, default="resources/chunks_generated.json", help="Output chunks json")
    parser.add_argument("--window_size", type=int, default=1200, help="Sliding window size (chars)")
    parser.add_argument("--overlap", type=int, default=200, help="Overlap size (chars)")
    args = parser.parse_args()

    pdf_dir = Path(args.pdf_dir)
    out_path = Path(args.out)

    if not pdf_dir.exists() or not pdf_dir.is_dir():
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir.resolve()}")

    chunker = SlidingWindowChunker(window_size=args.window_size, overlap=args.overlap)

    pdf_files = sorted([p for p in pdf_dir.iterdir() if p.suffix.lower() == ".pdf"])
    if not pdf_files:
        print(f"No PDF files found in: {pdf_dir.resolve()}")
        print("Put PDFs into that folder and run again.")
        return

    all_records: List[Dict] = []

    for pdf_path in pdf_files:
        doc_id = pdf_path.stem  # e.g. "mu_yonetmelik_onlisans_lisans_v21"
        print(f"[+] Reading: {pdf_path.name}")

        full_text = extract_text_from_pdf(pdf_path)
        full_text = normalize_text(full_text)

        print(f"    Extracted chars (normalized): {len(full_text)}")

        chunks = chunker.chunk(doc_id=doc_id, full_text=full_text)
        print(f"    Produced chunks: {len(chunks)}")

        for c in chunks:
            all_records.append(chunk_to_json_record(c))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"[OK] Wrote {len(all_records)} chunk records to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
