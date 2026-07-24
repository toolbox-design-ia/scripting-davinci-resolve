def write_edl(events, reel_map, project_name, drop_frame, output_path):
    fcm = "DROP FRAME" if drop_frame else "NON-DROP FRAME"
    lines = [f"TITLE: {project_name}", f"FCM: {fcm}", ""]

    for ev in events:
        lines.append(
            f"{ev['event_num']:03d}  "
            f"{ev['reel']:<8} "
            f"V     C        "
            f"{ev['src_in']} {ev['src_out']} "
            f"{ev['rec_in']} {ev['rec_out']}"
        )
        lines.append(f"* FROM CLIP NAME: {ev['source_name']}")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
