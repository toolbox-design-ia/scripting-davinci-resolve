import yaml

def cargar_catalogo(ruta_yaml: str) -> list[dict]:
    with open(ruta_yaml, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["presets"]

def aplicar_preset_a_resolve(project, preset_def: dict, target_dir: str) -> bool:
    settings = {
        "SelectAllFrames": True,
        "TargetDir": target_dir,
        "FormatWidth": preset_def["width"],
        "FormatHeight": preset_def["height"],
        "FrameRate": preset_def["fps"],
        "ExportVideo": preset_def["export_video"],
        "ExportAudio": preset_def["export_audio"],
        "AudioCodec": preset_def["audio_codec"],
        "AudioSampleRate": preset_def["audio_sample_rate"],
        "AudioBitDepth": preset_def["audio_bit_depth"],
    }
    ok_format = project.SetCurrentRenderFormatAndCodec(
        preset_def["format"], preset_def["codec"]
    )
    ok_settings = project.SetRenderSettings(settings)
    return ok_format and ok_settings
