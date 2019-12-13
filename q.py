from aisynphys.database import SynphysDatabase
from aisynphys.cell_class import CellClass
db = SynphysDatabase.load_version('synphys_r1.0_2019-08-29_small.sqlite')

inhibitory_class = CellClass(cre_type=('pvalb', 'sst', 'vip'))
query = db.pair_query(project_name=db.mouse_projects, synapse=True)
print(query)