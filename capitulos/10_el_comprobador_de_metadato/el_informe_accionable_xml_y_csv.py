import xml.etree.ElementTree as ET
from datetime import datetime

def build_xml_report(incidents: list[Incident], project_name: str,
                     timeline_name: str, spec: Spec) -> ET.Element:
    root = ET.Element('qc_report')
    root.set('project', project_name)
    root.set('timeline', timeline_name)
    root.set('spec_resolution', f'{spec.width}x{spec.height}')
    root.set('spec_fps', str(spec.fps))
    root.set('generated_at', datetime.now().isoformat(timespec='seconds'))
    root.set('total_incidents', str(len(incidents)))

    for inc in incidents:
        el = ET.SubElement(root, 'incident')
        el.set('severity', inc.severity)
        el.set('rule', inc.rule)
        el.set('track', str(inc.track))
        el.set('frame_in', str(inc.frame_in))
        ET.SubElement(el, 'clip').text = inc.clip_name
        ET.SubElement(el, 'file').text = inc.file_name
        ET.SubElement(el, 'detail').text = inc.detail

    return root


def save_xml(root: ET.Element, path: str):
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')   # requiere Python 3.9+
    tree.write(path, encoding='utf-8', xml_declaration=True)
