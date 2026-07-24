import json

def build_report(timeline_name: str,
                 fps: float,
                 clip_reports: List[ClipColorReport],
                 divergences: List[Divergence]) -> dict:

    def frames_to_tc(frames: int, fps: float) -> str:
        total_seconds = int(frames / fps)
        f = int(frames % fps)
        s = total_seconds % 60
        m = (total_seconds // 60) % 60
        h = total_seconds // 3600
        return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"

    uncolored = [r for r in clip_reports if r.state == ColorState.UNCOLORED]
    default_grade = [r for r in clip_reports if r.state == ColorState.DEFAULT]
    multiple_v = [r for r in clip_reports if r.state == ColorState.MULTIPLE_VERSIONS]
    errors = [d for d in divergences if d.severity == "ERROR"]
    warnings = [d for d in divergences if d.severity == "WARNING"]

    report = {
        "timeline": timeline_name,
        "fps": fps,
        "summary": {
            "total_clips": len(clip_reports),
            "uncolored": len(uncolored),
            "default_grade": len(default_grade),
            "multiple_versions": len(multiple_v),
            "divergence_errors": len(errors),
            "divergence_warnings": len(warnings),
            "qc_pass": len(uncolored) == 0 and len(errors) == 0,
        },
        "clips": [
            {
                "name": r.name,
                "track": r.track,
                "timecode": frames_to_tc(r.position, fps),
                "state": r.state.value,
                "versions": r.num_local_versions,
                "remote_versions": r.num_remote_versions,
                "current_version": r.current_version,
                "lut_node1": r.lut_node1,
                "warnings": r.warnings,
            }
            for r in clip_reports
        ],
        "divergences": [
            {
                "type": d.type,
                "severity": d.severity,
                "track": d.track,
                "clip_a": d.clip_a,
                "timecode_a": frames_to_tc(d.position_a, fps),
                "clip_b": d.clip_b,
                "timecode_b": frames_to_tc(d.position_b, fps),
                "detail": d.detail,
            }
            for d in divergences
        ],
    }
    return report
