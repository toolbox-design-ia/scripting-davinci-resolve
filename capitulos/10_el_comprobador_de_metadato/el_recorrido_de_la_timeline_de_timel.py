def get_clip_properties(track_idx: int, item) -> dict | None:
    mpi = item.GetMediaPoolItem()
    if mpi is None:
        return None
    return {
        'clip_name':      mpi.GetClipProperty('Clip Name') or mpi.GetName(),
        'file_name':      mpi.GetClipProperty('File Name') or '',
        'resolution':     mpi.GetClipProperty('Resolution') or '',
        'fps':            mpi.GetClipProperty('FPS') or '',
        'video_codec':    mpi.GetClipProperty('Video Codec') or '',
        'audio_channels': mpi.GetClipProperty('Audio Ch') or '0',
        'track':          track_idx,
        'frame_in':       item.GetStart(),
        'duration':       item.GetDuration(),
    }
