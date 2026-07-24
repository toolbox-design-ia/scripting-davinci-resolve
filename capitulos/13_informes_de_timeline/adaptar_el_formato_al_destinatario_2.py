def export_timeline_report(timeline, fps, drop_frame, destination, output_path, **kwargs):
    events, reel_map = extract_edl_events(timeline, fps, drop_frame)
    validation = [
        validate_clip(
            ev["media"], ev["duration_frames"], fps,
            kwargs.get("allowed_codecs")
        )
        for ev in events
    ]

    project_name = kwargs.get("project_name", "Resolve Project")

    if destination == "edl":
        return write_edl(events, reel_map, project_name, drop_frame, output_path)
    if destination == "csv":
        return write_csv_report(events, validation, output_path)
    if destination == "json":
        return write_json_timeline(events, reel_map, project_name, output_path)

    raise ValueError(f"Destino no soportado: {destination}")
