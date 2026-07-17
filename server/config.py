"""환경 설정 로딩 — 키/경로는 전부 서버측에서만 다룬다."""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # dotenv 미설치여도 동작
    pass


class Settings:
    # Claude
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = os.getenv("PIMM_MODEL", "claude-opus-4-8")

    # 저장소
    storage_backend: str = os.getenv("STORAGE_BACKEND", "local")  # local | gdrive
    storage_root: Path = Path(os.getenv("STORAGE_ROOT", "./storage")).resolve()
    gdrive_service_account: str = os.getenv("GDRIVE_SERVICE_ACCOUNT", "")
    gdrive_root_folder_id: str = os.getenv("GDRIVE_ROOT_FOLDER_ID", "")

    # 서버
    host: str = os.getenv("PIMM_HOST", "127.0.0.1")
    port: int = int(os.getenv("PIMM_PORT", "8787"))

    @property
    def has_claude(self) -> bool:
        return bool(self.anthropic_api_key)


settings = Settings()
