"""보드/게이트 도메인 모델 (Bible §3 코어)."""
from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


# --- 상태모델 5단계 (Bible §3) ---
class Status(str, Enum):
    NOT_STARTED = "미착수"
    IN_PROGRESS = "진행"
    REVIEW = "검수대기"
    DONE = "완료"
    HELD = "보류"


Category = Literal["murdermystery", "pimmup", "pimmersive"]


class Asset(BaseModel):
    """업로드→검수 파이프라인의 산출물 (실파일이 드라이브에 저장된다)."""
    id: str
    filename: str
    rel_path: str  # STORAGE_ROOT 기준 상대경로 → Claude가 Read할 실파일 위치
    uploaded_at: str
    reviewed: bool = False
    review_note: str = ""


class Gate(BaseModel):
    """완료 게이트 = 3-Gate (체크리스트 + 산출물링크 + PD승인)."""
    checklist: dict[str, bool] = Field(default_factory=dict)
    asset_ids: list[str] = Field(default_factory=list)
    pd_approved: bool = False

    def is_open(self) -> bool:
        checklist_ok = bool(self.checklist) and all(self.checklist.values())
        return checklist_ok and bool(self.asset_ids) and self.pd_approved


class Step(BaseModel):
    key: str
    title: str
    status: Status = Status.NOT_STARTED
    gate: Gate = Field(default_factory=Gate)
    guide: str = ""  # Partwork 워크로직 + Plogic 판단기준 표시용


class Board(BaseModel):
    """프로젝트보드 = 각 프로젝트의 단일 정본 (JSON)."""
    id: str
    category: Category
    title: str
    brief: dict[str, Any] = Field(default_factory=dict)
    steps: list[Step] = Field(default_factory=list)
    assets: list[Asset] = Field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


# --- 요청 바디 ---
class CreateBoardReq(BaseModel):
    category: Category
    title: str
    brief: dict[str, Any] = Field(default_factory=dict)


class UpdateStepReq(BaseModel):
    status: Status | None = None
    checklist: dict[str, bool] | None = None
    pd_approved: bool | None = None


class ForgeReq(BaseModel):
    """생성형 forge(머더미스터리) 초안 생성 요청."""
    board_id: str
    instruction: str = ""
