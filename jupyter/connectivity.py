import numpy as np
from aisynphys.database import SynphysDatabase
from aisynphys.cell_class import CellClass, classify_cells, classify_pairs
from aisynphys.connectivity import measure_connectivity, pair_was_probed

# Download and cache the sqlite file for the requested database
#   (for available versions, see SynphysDatabase.list_versions)
db = SynphysDatabase.load_version('synphys_r1.0_2019-08-29_small.sqlite')

# Load all cell pairs associated with mouse V1 projects
mouse_pairs = db.pair_query(project_name=["mouse V1 coarse matrix", "mouse V1 pre-production"]).all()

print("loaded %d cell pairs" % len(mouse_pairs))

# print some information about the last cell pair returned
pair = mouse_pairs[-1]
print("Cell pair:", pair)
print("  presynaptic subclass:", pair.pre_cell.cre_type)
print("  postsynaptic subclass:", pair.post_cell.cre_type)
print("  synaptic connection:", "yes" if pair.has_synapse else "no")

cell_class_criteria = {
    'l23pyr': {'dendrite_type': 'spiny',       'cortical_layer': '2/3'},
    'l23pv':  {'cre_type': 'pvalb',            'cortical_layer': '2/3'},
    'l23sst': {'cre_type': 'sst',              'cortical_layer': '2/3'},
    'l23vip': {'cre_type': 'vip',              'cortical_layer': '2/3'},
    'l4pyr':  {'cre_type': ('nr5a1', 'rorb'),  'cortical_layer': '4'},
    'l4pv':   {'cre_type': 'pvalb',            'cortical_layer': '4'},
    'l4sst':  {'cre_type': 'sst',              'cortical_layer': '4'},
    'l4vip':  {'cre_type': 'vip',              'cortical_layer': '4'},
    'l5et':   {'cre_type': ('sim1', 'fam84b'), 'cortical_layer': '5'},
    'l5it':   {'cre_type': 'tlx3',             'cortical_layer': '5'}, 
    'l5pv':   {'cre_type': 'pvalb',            'cortical_layer': '5'},
    'l5sst':  {'cre_type': 'sst',              'cortical_layer': '5'},
    'l5vip':  {'cre_type': 'vip',              'cortical_layer': '5'},
    'l6pyr':  {'cre_type': 'ntsr1',            'cortical_layer': ('6a','6b')},
    'l6pv':   {'cre_type': 'pvalb',            'cortical_layer': ('6a','6b')},
    'l6sst':  {'cre_type': 'sst',              'cortical_layer': ('6a','6b')},
    'l6vip':  {'cre_type': 'vip',              'cortical_layer': ('6a','6b')},
}

cell_classes = {name:CellClass(name=name, **criteria) for name,criteria in cell_class_criteria.items()}

# Group all cells by selected classes
cell_groups = classify_cells(cell_classes.values(), pairs=mouse_pairs)

# Group pairs into (pre_class, post_class) groups
pair_groups = classify_pairs(mouse_pairs, cell_groups)

# analyze matrix elements
results = measure_connectivity(pair_groups)

# pick two arbitrary cell classes to display results from
pre_class = cell_classes['l23sst']
post_class = cell_classes['l23vip']

print("Connectivity results for %s => %s" % (pre_class, post_class))
print("  %d synapses found out of %d probed" % (
    results[pre_class, post_class]['n_connected'],
    results[pre_class, post_class]['n_probed'],
))
print("  %0.2f%% connection probability" % (
    results[pre_class, post_class]['connection_probability'][0] * 100,
))
print("  95%% confidence interval: %0.2f%%-%0.2f%%" % (
    results[pre_class, post_class]['connection_probability'][1] * 100,
    results[pre_class, post_class]['connection_probability'][2] * 100,
))
    

import matplotlib.colors, matplotlib.cm
import matplotlib.pyplot as plt
from aisynphys.ui.notebook import show_connectivity_matrix
%matplotlib inline

# define a colormap and log normalization used to color the heatmap
norm = matplotlib.colors.LogNorm(vmin=0.01, vmax=1.0, clip=True)
cmap = matplotlib.cm.get_cmap('plasma')

# define the display labels to use for each cell subclass:
class_labels = {
    'l23pyr': 'L2/3 Pyr\nspiny',
    'l23pv':  'L2/3 Pv',
    'l23sst': 'L2/3 Sst',
    'l23vip': 'L2/3 Vip',
    'l4pyr':  'L4 Pyr\n nr5a1',
    'l4pv':   'L4 Pv',
    'l4sst':  'L4 Sst',
    'l4vip':  'L4 Vip',
    'l5et':   'L5 Pyr ET\nsim1, fam84b',
    'l5it':   'L5 Pyr IT\ntlx3',
    'l5pv':   'L5 Pv',
    'l5sst':  'L5 Sst',
    'l5vip':  'L5 Vip',
    'l6pyr':  'L6 Pyr\nntsr1',
    'l6pv':   'L6 Pv',
    'l6sst':  'L6 Sst',
    'l6vip':  'L6 Vip',
}

# create a figure/axes to draw on
fig, ax = plt.subplots(figsize=(15, 15))

# finally, draw the colormap using the provided function:
im, cbar, labels = show_connectivity_matrix(
    ax=ax, 
    results=results, 
    pre_cell_classes=cell_classes.values(), 
    post_cell_classes=cell_classes.values(), 
    class_labels=class_labels, 
    cmap=cmap, 
    norm=norm
)

# optionally we can save the figure at this point
fig.savefig('mouse_connectivity_matrix.svg', format='svg')

l23sst = cell_classes['l23sst']
cp, ci_low, ci_high = results[l23sst, l23sst]['connection_probability']
print(ci_low, ci_high)

# Load all cell pairs associated with mouse V1 projects
human_pairs = db.pair_query(project_name=["human coarse matrix"]).all()

print("loaded %d cell pairs" % len(human_pairs))

# Load all cell pairs associated with mouse V1 projects
human_pairs = db.pair_query(project_name=["human coarse matrix"]).all()

print("loaded %d cell pairs" % len(human_pairs))

cell_class_criteria = {
    'l2pyr':  {'dendrite_type': 'spiny', 'cortical_layer': '2'},
    'l3pyr':  {'dendrite_type': 'spiny', 'cortical_layer': '3'},
    'l4pyr':  {'dendrite_type': 'spiny', 'cortical_layer': '4'},
    'l5pyr':  {'dendrite_type': 'spiny', 'cortical_layer': '5'},
}

cell_classes = {name:CellClass(name=name, **criteria) for name,criteria in cell_class_criteria.items()}

# Group all cells by selected classes
cell_groups = classify_cells(cell_classes.values(), pairs=human_pairs)

# Group pairs into (pre_class, post_class) groups
pair_groups = classify_pairs(human_pairs, cell_groups)

# analyze matrix elements
results = measure_connectivity(pair_groups)

class_labels = {
    'l2pyr':  'L2 Pyr',
    'l2int':  'L2 Inh',
    'l3pyr':  'L3 Pyr',
    'l3int':  'L3 Inh',
    'l4pyr':  'L4 Pyr',
    'l4int':  'L4 Inh',
    'l5pyr':  'L5 Pyr',
    'l5int':  'L5 Inh',
}

# create a figure/axes to draw on
fig, ax = plt.subplots(figsize=(7, 7))

# finally, draw the colormap using the provided function:
im, cbar, labels = show_connectivity_matrix(
    ax=ax, 
    results=results, 
    pre_cell_classes=cell_classes.values(), 
    post_cell_classes=cell_classes.values(), 
    class_labels=class_labels, 
    cmap=cmap, 
    norm=norm
)
cbar.set_label("Connection probability", size=16)

# sort all inhibitory cells into pv, sst,and vip subclasses
cell_classes = {
    'pv': CellClass(cre_type='pvalb'),
    'sst': CellClass(cre_type='sst'),
    'vip': CellClass(cre_type='vip'),
}
cell_groups = classify_cells(cell_classes.values(), pairs=mouse_pairs)
pair_groups = classify_pairs(mouse_pairs, cell_groups)

from aisynphys.connectivity import connectivity_profile

# 20 um bins
bin_edges = np.arange(0, 500e-6, 20e-6)

profiles = {}
distances = {}
connected = {}

# loop over all 3 cell classes 
for name, cell_class in cell_classes.items():
    # get all like->like pairs for this cell class
    pairs = pair_groups[cell_class, cell_class]
    
    # filter for pairs that were probed for inhibitory connections
    pairs = [pair for pair in pairs if pair_was_probed(pair, 'in')]
    
    # build an array describing whether each pair is connected
    connected[name] = np.array([pair.has_synapse for pair in pairs]).astype(bool)
    
    # and another list of distances
    distances[name] = np.array([pair.distance for pair in pairs]).astype(float)
    
    # generate a profile of connection probability vs distance 
    # with confidence intervals
    profiles[name] = connectivity_profile(connected[name], distances[name], bin_edges)
    
    
fig,axes = plt.subplots(2, 3, figsize=(10, 5), sharex=True, gridspec_kw={'height_ratios': [1, 4]})

for i,name in enumerate(profiles):
    bin_edges, prop, lower_ci, upper_ci = profiles[name]
    
    ax = axes[0, i]
    dist = distances[name]*1e6
    ax.hist(dist, bins=bin_edges*1e6, color=(0.6, 0.7, 0.9))
    ax.hist(dist[connected[name]], bins=bin_edges*1e6, color='red')
    
    xvals = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax = axes[1, i]
    ax.fill_between(xvals*1e6, lower_ci, upper_ci, color=(0.8, 0.8, 0.8))
    ax.plot(xvals*1e6, prop, color=(0, 0, 0))
    ax.set_ylim(0.001, 0.5)
    ax.set_xlim(0, 250)
    ax.set_title(name + "->" + name, size=18)
    

axes[0,0].set_ylabel('pairs\nprobed', size=12)
axes[1,0].set_ylabel('proportion connected', size=16)
axes[1,1].set_xlabel('intersomatic distance (µm)', size=16);


