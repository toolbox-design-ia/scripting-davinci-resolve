from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Spec:
    width: int
    height: int
    fps: float
    fps_tolerance: float = 0.001
    codecs: list = field(default_factory=list)
    name_pattern: Optional[str] = None
    min_audio_channels: int = 2
