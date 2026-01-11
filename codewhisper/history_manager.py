"""
History Manager - 转录结果本地历史持久化（轻量级）
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .utils import get_project_root


@dataclass(frozen=True)
class HistoryRecord:
    text: str
    created_at: str


class HistoryManager:
    """本地历史记录管理器（JSON 持久化、容量限制、线程安全）"""

    def __init__(self, path: Optional[Path] = None, max_records: int = 10):
        self.path = Path(path) if path is not None else (get_project_root() / "history.json")
        self.max_records = int(max_records)
        self._lock = threading.Lock()
        self._records: List[HistoryRecord] = []
        self._load()

    def _load(self) -> None:
        with self._lock:
            if not self.path.exists():
                self._records = []
                return

            try:
                data = json.loads(self.path.read_text(encoding="utf-8"))
                records = []
                for item in data.get("records", []):
                    text = (item.get("text") or "").strip()
                    created_at = (item.get("created_at") or "").strip()
                    if not text:
                        continue
                    records.append(HistoryRecord(text=text, created_at=created_at or ""))
                self._records = records[-self.max_records :]
            except Exception:
                self._records = []

    def _save(self) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "version": 1,
                "records": [
                    {"text": record.text, "created_at": record.created_at}
                    for record in self._records[-self.max_records :]
                ],
            }
            self.path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def add(self, text: str) -> None:
        cleaned = (text or "").strip()
        if not cleaned:
            return

        created_at = datetime.now(timezone.utc).astimezone().isoformat()
        with self._lock:
            self._records.append(HistoryRecord(text=cleaned, created_at=created_at))
            if len(self._records) > self.max_records:
                self._records = self._records[-self.max_records :]
        self._save()

    def list(self) -> List[HistoryRecord]:
        with self._lock:
            return list(self._records)

