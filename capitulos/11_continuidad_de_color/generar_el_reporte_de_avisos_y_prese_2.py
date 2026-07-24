def print_summary(report: dict) -> None:
    s = report["summary"]
    print(f"\n=== Continuidad de color: {report['timeline']} ===")
    print(f"Total de clips analizados : {s['total_clips']}")
    print(f"Sin grade                 : {s['uncolored']}")
    print(f"En versión por defecto    : {s['default_grade']}")
    print(f"Versiones sin consolidar  : {s['multiple_versions']}")
    print(f"Divergencias ERROR        : {s['divergence_errors']}")
    print(f"Divergencias WARNING      : {s['divergence_warnings']}")
    print(f"Resultado QC              : {'APROBADO' if s['qc_pass'] else 'RECHAZADO'}")
    print()

    if s["uncolored"] > 0:
        print("CLIPS SIN GRADE:")
        for c in report["clips"]:
            if c["state"] == "sin_grade":
                print(f"  [{c['timecode']}] Pista {c['track']} - {c['name']}")

    if s["divergence_errors"] > 0:
        print("\nDIVERGENCIAS CRITICAS:")
        for d in report["divergences"]:
            if d["severity"] == "ERROR":
                print(f"  [{d['timecode_a']}] Pista {d['track']} - "
                      f"{d['clip_a']} / {d['clip_b']}: {d['detail']}")
