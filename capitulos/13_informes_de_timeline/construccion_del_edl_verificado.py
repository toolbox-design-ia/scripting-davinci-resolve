def extract_edl_events(timeline, fps, drop_frame=False):
    reel_map = {}     # nombre_fuente -> codigo_corto
    counter = [0]
    events = []

    def reel_code(name):
        if name not in reel_map:
            counter[0] += 1
            reel_map[name] = f"R{counter[0]:03d}"
        return reel_map[name]

    for item in timeline.GetItemListInTrack("video", 1):
        start_tl = item.GetStart()
        end_tl   = item.GetEnd()
        if end_tl <= start_tl:
            continue

        media = item.GetMediaPoolItem()
        src_name = media.GetName() if media else "BLACK"
        dur = end_tl - start_tl

        events.append({
            "event_num":    len(events) + 1,
            "reel":         reel_code(src_name),
            "track":        "V",
            "transition":   "C",
            "src_in":       frames_to_tc(0, fps, drop_frame),
            "src_out":      frames_to_tc(dur, fps, drop_frame),
            "rec_in":       frames_to_tc(start_tl, fps, drop_frame),
            "rec_out":      frames_to_tc(end_tl, fps, drop_frame),
            "duration_frames": dur,
            "source_name":  src_name,
            "media":        media,
        })

    return events, reel_map
