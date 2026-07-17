"""저장소 추상화 — JSON 보드 + 업로드 에셋을 '실파일'로 남긴다.

핵심(Bible §2 에셋 변수): 업로드/생성 산출물이 드라이브에 **실파일**로 존재해야
Claude(코워크)가 Read로 검수할 수 있다. 그래서 브라우저 localStorage가 아니라
서버가 파일시스템/Drive에 쓴다.

- LocalStore : STORAGE_ROOT 폴더에 저장. 이 폴더가 Google Drive 데스크톱 동기
  폴더면 그대로 Drive에 반영된다. (기본, 즉시 동작)
- DriveStore : Google Drive API 직접 호출. (서비스계정 필요; 골격 제공)
"""
from __future__ import annotations

import json
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .config import settings


class Store(ABC):
    @abstractmethod
    def save_board(self, board_id: str, data: dict[str, Any]) -> None: ...

    @abstractmethod
    def load_board(self, board_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    def list_boards(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def save_asset(self, board_id: str, filename: str, data: bytes) -> str:
        """에셋을 실파일로 저장하고 STORAGE 기준 상대경로를 반환."""

    @abstractmethod
    def read_asset(self, rel_path: str) -> bytes: ...


class LocalStore(Store):
    """로컬 파일시스템(또는 Drive 동기 폴더) 백엔드."""

    def __init__(self, root: Path):
        self.root = root
        (self.root / "boards").mkdir(parents=True, exist_ok=True)
        (self.root / "assets").mkdir(parents=True, exist_ok=True)

    def _board_path(self, board_id: str) -> Path:
        return self.root / "boards" / f"{board_id}.json"

    def save_board(self, board_id: str, data: dict[str, Any]) -> None:
        # 안전 쓰기: 임시파일 → 원자적 교체 (truncate 사고 방지)
        p = self._board_path(board_id)
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(p)

    def load_board(self, board_id: str) -> dict[str, Any] | None:
        p = self._board_path(board_id)
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))

    def list_boards(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for p in sorted((self.root / "boards").glob("*.json")):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                out.append({"id": d.get("id"), "title": d.get("title"),
                            "category": d.get("category")})
            except Exception:
                continue
        return out

    def save_asset(self, board_id: str, filename: str, data: bytes) -> str:
        # 경로 traversal 방지 — basename만 사용
        safe = Path(filename).name or "asset.bin"
        dest_dir = self.root / "assets" / board_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / safe
        # 동명이인 방지
        i = 1
        while dest.exists():
            dest = dest_dir / f"{dest.stem}_{i}{dest.suffix}"
            i += 1
        dest.write_bytes(data)
        return str(dest.relative_to(self.root))

    def read_asset(self, rel_path: str) -> bytes:
        target = (self.root / rel_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise ValueError("경로 이탈")
        return target.read_bytes()


class DriveStore(Store):
    """Google Drive API 백엔드 (골격 — 서비스계정 연결 지점).

    실제 배포 시 google-api-python-client로 파일을 Drive 폴더에 생성/업로드한다.
    현재는 로컬로 폴백하며, TODO 지점에 Drive files.create 호출을 연결한다.
    """

    def __init__(self):
        self._fallback = LocalStore(settings.storage_root)
        self._svc = None
        # TODO: 서비스계정 연결
        # from googleapiclient.discovery import build
        # from google.oauth2 import service_account
        # creds = service_account.Credentials.from_service_account_file(
        #     settings.gdrive_service_account,
        #     scopes=["https://www.googleapis.com/auth/drive"])
        # self._svc = build("drive", "v3", credentials=creds)

    # 초기에는 보드 JSON은 로컬(=Drive 동기 폴더)에, 에셋만 Drive API로 올리는
    # 하이브리드도 가능. 우선 전부 로컬 폴백으로 위임한다.
    def save_board(self, board_id, data):  # noqa: ANN001
        self._fallback.save_board(board_id, data)

    def load_board(self, board_id):  # noqa: ANN001
        return self._fallback.load_board(board_id)

    def list_boards(self):
        return self._fallback.list_boards()

    def save_asset(self, board_id, filename, data):  # noqa: ANN001
        # TODO: self._svc.files().create(media_body=..., body={parents:[folder]})
        return self._fallback.save_asset(board_id, filename, data)

    def read_asset(self, rel_path):  # noqa: ANN001
        return self._fallback.read_asset(rel_path)


def get_store() -> Store:
    if settings.storage_backend == "gdrive":
        return DriveStore()
    return LocalStore(settings.storage_root)
