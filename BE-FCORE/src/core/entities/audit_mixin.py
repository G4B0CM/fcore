# core/entities/audit.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AuditMixin:
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None