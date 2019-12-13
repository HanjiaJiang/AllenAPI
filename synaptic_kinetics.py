import numpy as np
from aisynphys.database import SynphysDatabase
from aisynphys.cell_class import CellClass

# Download and cache the sqlite file for the requested database
#   (for available versions, see SynphysDatabase.list_versions)
db = SynphysDatabase.load_version('synphys_r1.0_2019-08-29_small.sqlite')

cell_classes = {
    'exc': CellClass(pyramidal=True),
    'pvalb': CellClass(cre_type='pvalb'),
    'sst': CellClass(cre_type='sst'),
    'vip': CellClass(cre_type='vip'),
}


def qry(pre_class, post_class, pre_name, post_name, attribute):
    pairs = db.pair_query(
        project_name=["mouse V1 coarse matrix", "mouse V1 pre-production"],    # db.mouse_projects
        pre_class=pre_class,
        post_class=post_class,
        synapse=True
    )
    pairs = pairs.add_columns(
        db.Dynamics.paired_pulse_ratio_50hz,
        db.Dynamics.stp_induction_50hz,
        db.Synapse.psc_rise_time,
        db.Synapse.psc_decay_tau,
        db.Synapse.psp_amplitude,
    )
    df = pairs.dataframe()
    print('pre={}, post={}'.format(pre_name, post_name))
    print('{} = {}\n'.format(attribute, df[attribute].mean()))


# qry(CellClass(cre_type='pvalb'), CellClass(), 'psc_rise_time')

for pre_name, pre_class in cell_classes.items():
    for post_name, post_class in cell_classes.items():
        qry(pre_class, post_class, pre_name, post_name, 'stp_induction_50hz')