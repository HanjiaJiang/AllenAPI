from aisynphys.database import SynphysDatabase
from aisynphys.cell_class import CellClass
from aisynphys.database.schema import Pair

db = SynphysDatabase.load_version('synphys_r1.0_2019-08-29_small.sqlite')
pair_query = db.pair_query(
    project_name=["mouse V1 coarse matrix", "mouse V1 pre production"],
    pre_class= CellClass(cre_type='ex'),
    synapse=True,
    synapse_type='ex'
)
pair_query = pair_query.add_columns(
    db.Pair.has_synapse,
    db.Synapse.psc_decay_tau,
)
df = pair_query.dataframe()
# print(df)
for item in df['has_synapse']:
    print(item)
