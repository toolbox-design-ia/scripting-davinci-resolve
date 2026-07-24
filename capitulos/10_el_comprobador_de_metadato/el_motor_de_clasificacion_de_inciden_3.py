CHECKERS = [check_resolution, check_fps, check_codec,
            check_nomenclature, check_audio]

def validate_timeline(spec: Spec) -> list[Incident]:
    _, timeline = get_context()
    incidents = []

    for track_idx, item in iter_video_items(timeline):
        props = get_clip_properties(track_idx, item)
        if props is None:
            incidents.append(Incident(
                severity='info',
                clip_name=f'[pista {track_idx}, frame {item.GetStart()}]',
                file_name='',
                track=track_idx,
                frame_in=item.GetStart(),
                rule='no_media_pool_item',
                detail='Sin MediaPoolItem (título, ajuste o clip offline)'
            ))
            continue
        for checker in CHECKERS:
            incidents.extend(checker(props, spec))

    return incidents
