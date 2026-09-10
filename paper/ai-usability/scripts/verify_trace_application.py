#!/usr/bin/env python3
"""Validate public trace integrity, references and coverage; not source truth."""
from pathlib import Path
import collections, hashlib, json
P=Path(__file__).resolve().parents[1]
D=P/'data/trace-v0.3'
def read(name): return json.loads((D/name).read_text())
def main():
    manifest=read('manifest.json')
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((D/name).read_bytes()).hexdigest()==digest, name
    frozen=json.loads((P/'data/manifest.json').read_text())
    for name,digest in frozen['frozen_files'].items():
        assert hashlib.sha256((P/'data'/name).read_bytes()).hexdigest()==digest,name
    events=read('events.json'); E={e['event_id']:e for e in events}
    attempts=read('attempts.json'); units=read('applications.json')
    assert len(E)==len(events)==350
    assert all(e['return_present'] for e in events)
    assert sum(e['attempt_id']=='MAIN' for e in events)==49
    assert len(attempts)==31
    assert len({a['task_id'] for a in attempts if a['structured_report']})==18
    assert len({u['unit_id'] for u in units})==len(units)==52
    assert sum(bool(u['selected_event_id']) for u in units)==48
    for u in units:
        assert all('M'+str(i) in u for i in range(1,12))
        if u['selected_event_id']:
            assert u['selected_event_id'] in E
            assert E[u['selected_event_id']]['tool']=='WebFetch'
        for eid in u['additional_event_ids']: assert eid in E
        assert u['M10']['execution_tested'] is False
    assert E['O-A01-E005']['timestamp_utc'] < E['O-A01-E009']['timestamp_utc']
    counts={s:dict(collections.Counter(u['M2']['code'] for u in units if u['side']==s and u['comparison_included'])) for s in ['cann','cuda']}
    assert counts==read('application-summary.json')['primary_M2_by_side']
    for p in D.iterdir():
        if p.is_file():
            text=p.read_text()
            assert ('/'+'Users'+'/') not in text and '.claude/projects' not in text,p.name
    print('PASS: frozen/public hashes; 350 paired events; 31 attempts; 52 units; 48 selected reads; cross-references and O chronology.')
    print('These checks establish integrity and consistency, not independent coding validity or execution success.')
if __name__=='__main__':main()
