import os

def main():
    spec = SPEC_UHD_25  # o: spec = load_spec('specs/uhd_25_prores.json')

    resolve = dvr_script.scriptapp("Resolve")
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    timeline = project.GetCurrentTimeline()

    project_name  = project.GetName()
    timeline_name = timeline.GetName()

    incidents = validate_timeline(spec)

    output_dir = os.path.expanduser("~/Desktop/qc_reports")
    os.makedirs(output_dir, exist_ok=True)

    xml_path = os.path.join(output_dir, f"{timeline_name}_qc.xml")
    csv_path = os.path.join(output_dir, f"{timeline_name}_qc.csv")

    root = build_xml_report(incidents, project_name, timeline_name, spec)
    save_xml(root, xml_path)
    save_csv(incidents, csv_path)

    errors   = sum(1 for i in incidents if i.severity == 'error')
    warnings = sum(1 for i in incidents if i.severity == 'warning')
    infos    = sum(1 for i in incidents if i.severity == 'info')

    print(f"\nQC completado - {project_name} / {timeline_name}")
    print(f"  Errores:      {errors}")
    print(f"  Advertencias: {warnings}")
    print(f"  Info:         {infos}")
    print(f"\nInformes en {output_dir}")

if __name__ == '__main__':
    main()
