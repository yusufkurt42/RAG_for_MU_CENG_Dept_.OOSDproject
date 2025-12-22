import argparse
import json
from collections import defaultdict
from typing import Dict, List, Any


def build_keyword_index(chunks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Output format:
      term -> list of {docId, chunkId, tf}
    """
    # term -> chunkId -> (docId, tf)
    postings: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)

    for c in chunks:
        cid = c.get("id")
        doc_id = c.get("docId")
        text = (c.get("text") or "").strip()

        if not cid or not text:
            continue

        terms = text.lower().split()

        tf_map: Dict[str, int] = defaultdict(int)
        for t in terms:
            if t:
                tf_map[t] += 1

        for term, tf in tf_map.items():
            postings[term][cid] = {"docId": doc_id, "chunkId": cid, "tf": tf}

    # convert to required dict-of-lists format
    out: Dict[str, List[Dict[str, Any]]] = {}
    for term, chunk_map in postings.items():
        out[term] = list(chunk_map.values())

    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", required=True, help="Path to chunks.json")
    parser.add_argument("--out", required=True, help="Path to keyword_index.json output")
    args = parser.parse_args()

    with open(args.chunks, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    idx = build_keyword_index(chunks)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)

    print(f"Wrote keyword index: {args.out} (terms={len(idx)})")


if __name__ == "__main__":
    main()
