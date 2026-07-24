@dataclass
class Divergence:
    type: str
    track: int
    clip_a: str
    clip_b: str
    position_a: int
    position_b: int
    detail: str
    severity: str  # "ERROR", "WARNING", "INFO"

def detect_divergences(reports: List[ClipColorReport]) -> List[Divergence]:
    divergences = []

    by_track: dict[int, List[ClipColorReport]] = {}
    for r in reports:
        by_track.setdefault(r.track, []).append(r)

    for track, clips in by_track.items():
        ordered = sorted(clips, key=lambda c: c.position)

        for i in range(len(ordered) - 1):
            a = ordered[i]
            b = ordered[i + 1]

            if a.state == ColorState.COLOR_GROUP or b.state == ColorState.COLOR_GROUP:
                continue

            if (a.state == ColorState.UNCOLORED) != (b.state == ColorState.UNCOLORED):
                divergences.append(Divergence(
                    type="state_mismatch", track=track,
                    clip_a=a.name, clip_b=b.name,
                    position_a=a.position, position_b=b.position,
                    detail=f"'{a.name}' ({a.state.value}) vs '{b.name}' ({b.state.value})",
                    severity="ERROR",
                ))

            elif (a.state == ColorState.GRADED and b.state == ColorState.GRADED
                  and a.lut_node1 != b.lut_node1):
                divergences.append(Divergence(
                    type="lut_mismatch", track=track,
                    clip_a=a.name, clip_b=b.name,
                    position_a=a.position, position_b=b.position,
                    detail=f"LUT nodo 1: '{a.lut_node1 or '(ninguna)'}' vs '{b.lut_node1 or '(ninguna)'}'",
                    severity="WARNING",
                ))

            if (a.state == ColorState.MULTIPLE_VERSIONS
                    or b.state == ColorState.MULTIPLE_VERSIONS):
                divergences.append(Divergence(
                    type="unresolved_versions", track=track,
                    clip_a=a.name, clip_b=b.name,
                    position_a=a.position, position_b=b.position,
                    detail="Al menos un clip tiene versiones locales sin consolidar",
                    severity="INFO",
                ))

    return divergences
