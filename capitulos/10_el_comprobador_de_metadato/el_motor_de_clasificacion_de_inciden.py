from dataclasses import dataclass

@dataclass
class Incident:
    severity: str   # 'error' | 'warning' | 'info'
    clip_name: str
    file_name: str
    track: int
    frame_in: int
    rule: str
    detail: str
