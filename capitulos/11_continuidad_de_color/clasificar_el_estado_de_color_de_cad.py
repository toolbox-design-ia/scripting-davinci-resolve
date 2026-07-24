class ColorState(Enum):
    UNCOLORED         = "sin_grade"
    DEFAULT           = "version_defecto"
    GRADED            = "coloreado"
    MULTIPLE_VERSIONS = "versiones_multiples"
    COLOR_GROUP       = "grupo_de_color"

@dataclass
class ClipColorReport:
    name: str
    track: int
    position: int
    duration: int
    state: ColorState
    num_local_versions: int
    num_remote_versions: int
    version_names: List[str]
    current_version: str
    lut_node1: str
    warnings: List[str] = field(default_factory=list)
