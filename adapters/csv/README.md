# CSV adapter

CSV is the planned first adoption bridge. A future implementation must validate a declared schema, preserve the original file hash, and map data into canonical evidence/events without inferring a cause or discarding source rows. No CSV adapter is implemented in this repository today.

The synthetic torque fixture illustrates a candidate quality-event source shape: timestamp, unit, station, shift, torque result, defect code, and tool battery voltage. It is test data, not an adapter contract or production schema.
