DEFAULT_VERSION_NAMES = {"Version 1", "version 1", "Version_1"}

def classify_clip(track_idx: int, item) -> ClipColorReport:
    name = item.GetName()
    position = item.GetStart()
    duration = item.GetDuration()
    warnings = []

    num_local = len(item.GetVersionNameList(0))
    num_remote = len(item.GetVersionNameList(1))
    version_names = item.GetVersionNameList(0) or []
    current = item.GetCurrentVersion(0) or ""
    lut_node1 = item.GetLUT(1) or ""

    if is_in_color_group(item):
        return ClipColorReport(
            name=name, track=track_idx, position=position, duration=duration,
            state=ColorState.COLOR_GROUP,
            num_local_versions=num_local,
            num_remote_versions=num_remote,
            version_names=version_names,
            current_version=current,
            lut_node1=lut_node1,
            warnings=["El grade proviene de un grupo de color"],
        )

    if num_local == 0 and num_remote == 0:
        state = ColorState.UNCOLORED
    elif num_local == 0 and num_remote > 0:
        state = ColorState.GRADED
        warnings.append("El grade proviene de versiones remotas, no locales")
    elif num_local > 1:
        state = ColorState.MULTIPLE_VERSIONS
        warnings.append(f"{num_local} versiones locales sin consolidar")
    elif current in DEFAULT_VERSION_NAMES and not lut_node1:
        state = ColorState.DEFAULT
    else:
        state = ColorState.GRADED

    return ClipColorReport(
        name=name, track=track_idx, position=position, duration=duration,
        state=state,
        num_local_versions=num_local,
        num_remote_versions=num_remote,
        version_names=version_names,
        current_version=current,
        lut_node1=lut_node1,
        warnings=warnings,
    )
