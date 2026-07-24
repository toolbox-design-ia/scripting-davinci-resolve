import csv

def save_csv(incidents: list[Incident], path: str):
    fieldnames = ['severity', 'rule', 'track', 'frame_in',
                  'clip_name', 'file_name', 'detail']
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for inc in incidents:
            writer.writerow({
                'severity':  inc.severity,
                'rule':      inc.rule,
                'track':     inc.track,
                'frame_in':  inc.frame_in,
                'clip_name': inc.clip_name,
                'file_name': inc.file_name,
                'detail':    inc.detail,
            })
