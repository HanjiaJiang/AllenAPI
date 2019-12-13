from aisynphys.database import SynphysDatabase
db = SynphysDatabase.load_version('synphys_r1.0_2019-08-29_small.sqlite')

# create an SQLAlchemy session
session = db.session()

# build a query to select all mouse experiments
query = session.query(db.Experiment).join(db.Slice).filter(db.Slice.species=='mouse')

# retrieve the list of experiments
expts = query.all()

# from the first experiment returned, print a list of cells and their transgenic type:
print("Frst experiment returned:", expts[0])
for cell in expts[0].cells:
    print("Cell %s cre type: %s" % (cell.ext_id, cell.cre_type))