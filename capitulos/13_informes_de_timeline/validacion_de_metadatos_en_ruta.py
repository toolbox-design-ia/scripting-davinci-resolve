def validate_clip(media_item, timeline_dur_frames, fps, allowed_codecs=None):
    result = {
        "status": "OK",
        "notes": "",
        "file_path": "",
        "codec": "",
        "resolution": "",
        "clip_type": "",
    }
    issues = []

    if not media_item:
        result["status"] = "WARNING"
        result["notes"] = "clip interno sin archivo fuente"
        result["clip_type"] = "PLACEHOLDER"
        return result

    path   = media_item.GetClipProperty("File Path")
    codec  = media_item.GetClipProperty("Codec")
    res    = media_item.GetClipProperty("Resolution")
    name   = media_item.GetName()
    result.update({
        "file_path": path,
        "codec": codec,
        "resolution": res,
        "clip_type": classify_clip(name, path),
    })

    if not file_is_accessible(path):
        issues.append(f"archivo no accesible: {path}")

    if allowed_codecs and codec not in allowed_codecs:
        issues.append(f"codec no esperado: {codec}")

    try:
        clip_fps = float(media_item.GetClipProperty("FPS"))
        if abs(clip_fps - fps) > 0.01:
            issues.append(f"FPS del clip ({clip_fps:.3f}) difiere del proyecto ({fps:.3f})")
    except (ValueError, TypeError):
        pass

    if issues:
        result["status"] = "ERROR" if any("no accesible" in i for i in issues) else "WARNING"
        result["notes"] = "; ".join(issues)

    return result
