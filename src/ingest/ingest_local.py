from pathlib import Path
import json

RAW = Path("data/raw")
src = RAW / "transactions.json"
assert src.exists(), "Missing data/raw/transactions.json"
events = json.loads(src.read_text(encoding="utf-8"))
print(f"[ingest] read {len(events)} transactions from {src}")
