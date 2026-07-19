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
    # Google Drive 데스크톱 앱 동기 폴더의 로컬 경로 (옐로필드/아웃풋섹터/PIMMplayer_JSON).
    # 여기에 쓰면 Drive 앱이 자동 업로드 → 별도 API 불필요.
    drive_export_dir: str = os.getenv("PIMM_DRIVE_EXPORT_DIR", "")

    # 서버
    host: str = os.getenv("PIMM_HOST", "127.0.0.1")
    port: int = int(os.getenv("PIMM_PORT", "8787"))

    @property
    def has_claude(self) -> bool:
        return bool(self.anthropic_api_key)


settings = Settings()
