import re
import os

def check_resolution(props: dict, spec: Spec) -> list[Incident]:
    res = props['resolution']
    if not res:
        return [Incident('warning', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'resolution_missing', 'Propiedad Resolution vacía')]
    parts = res.split('x')
    if len(parts) != 2:
        return [Incident('warning', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'resolution_format', f'Formato inesperado: "{res}"')]
    try:
        w, h = int(parts[0]), int(parts[1])
    except ValueError:
        return [Incident('warning', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'resolution_parse', f'No se pudo convertir: "{res}"')]
    if w != spec.width or h != spec.height:
        return [Incident('error', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'resolution',
                         f'Resolución {res}; esperada {spec.width}x{spec.height}')]
    return []


def check_fps(props: dict, spec: Spec) -> list[Incident]:
    fps_str = props['fps']
    if not fps_str:
        return [Incident('warning', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'fps_missing', 'Propiedad FPS vacía')]
    try:
        fps_val = float(fps_str)
    except ValueError:
        return [Incident('warning', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'fps_parse', f'No se pudo interpretar FPS: "{fps_str}"')]
    if abs(fps_val - spec.fps) > spec.fps_tolerance:
        return [Incident('error', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'fps', f'FPS {fps_val}; esperado {spec.fps}')]
    return []


def check_codec(props: dict, spec: Spec) -> list[Incident]:
    if not spec.codecs:
        return []
    codec = props['video_codec'].lower()
    if not any(c.lower() in codec for c in spec.codecs):
        return [Incident('error', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'codec',
                         f'Codec "{props["video_codec"]}"; '
                         f'permitidos: {spec.codecs}')]
    return []


def check_nomenclature(props: dict, spec: Spec) -> list[Incident]:
    if not spec.name_pattern:
        return []
    fname = os.path.basename(props['file_name'] or props['clip_name'])
    if not re.match(spec.name_pattern, fname):
        return [Incident('warning', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'nomenclature',
                         f'Nombre "{fname}" no cumple patrón')]
    return []


def check_audio(props: dict, spec: Spec) -> list[Incident]:
    try:
        ch = int(props['audio_channels'])
    except ValueError:
        return []
    if ch == 0:
        return [Incident('error', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'audio_absent', 'Sin canales de audio')]
    if ch < spec.min_audio_channels:
        return [Incident('warning', props['clip_name'], props['file_name'],
                         props['track'], props['frame_in'],
                         'audio_channels',
                         f'{ch} canales; mínimo {spec.min_audio_channels}')]
    return []
