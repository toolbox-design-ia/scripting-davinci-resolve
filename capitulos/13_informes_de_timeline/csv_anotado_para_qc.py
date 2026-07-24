import csv

def write_csv_report(events, validation_results, output_path):
    fieldnames = [
        "event_num", "source_name", "reel_code",
        "rec_in", "rec_out", "duration_frames",
        "file_path", "codec", "resolution", "clip_type",
        "status", "notes",
    ]

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ev, val in zip(events, validation_results):
            writer.writerow({
                "event_num":       ev["event_num"],
                "source_name":     ev["source_name"],
                "reel_code":       ev["reel"],
                "rec_in":          ev["rec_in"],
                "rec_out":         ev["rec_out"],
                "duration_frames": ev["duration_frames"],
                "file_path":       val.get("file_path", ""),
                "codec":           val.get("codec", ""),
                "resolution":      val.get("resolution", ""),
                "clip_type":       val.get("clip_type", ""),
                "status":          val.get("status", "OK"),
                "notes":           val.get("notes", ""),
            })
