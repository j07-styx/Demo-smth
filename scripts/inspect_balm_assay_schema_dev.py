import json,pyarrow as pa
from pathlib import Path
p=Path(r'C:\Users\J0124\dynacpi_v4\data\reference\balm_bindingdb_202611\data-00000-of-00001.arrow')
with pa.memory_map(str(p),'r') as h:
    schema=pa.ipc.open_stream(h).schema
fields=schema.names
out={'evidence':'SCHEMA_ONLY_NO_LABEL_VALUES_READ','fields':fields,'assay_like_fields':[x for x in fields if any(k in x.lower() for k in ['assay','doi','publication','construct','endpoint','unit'])],'meaning':'Column names alone cannot authenticate comparability. No automatic same-assay assumption.'}
Path('research/pose_free_interaction_20261113/assay_schema.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
