import pandera as pa

# def contains_newline(s):
#     return s.str.contains('\n')

# fxn_map = {
#     'contains_newline': contains_newline
# }


# schema_dict = {
#     num_cols: 9,
#     checks: {
#         StringError: 'contains_newline'
#     }
# }

# def create_schema(config):
#     schema = pa.DataFrameSchema()
#     columns = [str(i) for i in range(0, config.num_cols)]
#     for col in columns:
#         checks = [pa.Check(error=k, check_fn=fxn_map[v]) for (k, v) in config.checks.items()]
#     return schema

# schema = create_schema(schema_dict)

import pandas as pd

from pandera import Check, Column, DataFrameSchema

df = pd.DataFrame({"column": ["a", "b", "c"]})

schema = pa.DataFrameSchema({"column": Column(pa.Int)})
print(schema)

schema1 = pa.DataFrameSchema({
    "column2": pa.Column(pa.String, [
        pa.Check(lambda s: s.str.startswith("value")),
        pa.Check(lambda s: s.str.split("_", expand=True).shape[1] == 2)
    ]),
})

print(schema1)