def classify_clip(source_name, file_path):
    name_upper = source_name.upper()
    path_upper = file_path.upper() if file_path else ""

    if "VFX" in name_upper or "_V" in name_upper:
        return "VFX"
    if "PLHD" in name_upper or source_name == "BLACK":
        return "PLACEHOLDER"
    if "/BROLL/" in path_upper or "\\BROLL\\" in path_upper:
        return "BROLL"
    return "CAM_A"
