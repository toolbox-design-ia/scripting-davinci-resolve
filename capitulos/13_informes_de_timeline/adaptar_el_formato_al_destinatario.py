import json

def write_json_timeline(events, reel_map, project_name, output_path, **kwargs):
    payload = {
        "project": project_name,
        "reel_map": reel_map,
        "events": [
            {k: v for k, v in ev.items() if k != "media"}
            for ev in events
        ],
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
