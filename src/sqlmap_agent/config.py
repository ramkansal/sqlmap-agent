from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    
    model: str = os.getenv("LLM_MODEL")
    
    sqlmap_timeout_s: int = int(os.getenv("SQLMAP_TIMEOUT_S", "900"))  

settings = Settings()
