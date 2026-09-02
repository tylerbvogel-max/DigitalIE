# CSV adapter

CSV is the first adoption bridge. It validates headers, preserves the original file hash, and maps data into canonical evidence/events. It does not infer a root cause from columns or discard source rows during import.

The torque fixture illustrates a minimal quality-event extract: timestamp, unit, station, shift, torque result, defect code, and tool battery voltage.
