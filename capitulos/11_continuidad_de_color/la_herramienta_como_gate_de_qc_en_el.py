def run_color_continuity_check(output_path: str = "color_qc.json") -> bool:
    timeline = get_active_timeline()
    fps = timeline.GetSetting("timelineFrameRate")
    fps = float(fps) if fps else 24.0
    timeline_name = timeline.GetName()

    raw_items = collect_timeline_items(timeline)
    clip_reports = [classify_clip(track_idx, item) for track_idx, item in raw_items]
    divergences = detect_divergences(clip_reports)

    report = build_report(timeline_name, fps, clip_reports, divergences)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print_summary(report)
    print(f"\nReporte completo guardado en: {output_path}")

    return report["summary"]["qc_pass"]

if __name__ == "__main__":
    passed = run_color_continuity_check()
    raise SystemExit(0 if passed else 1)
