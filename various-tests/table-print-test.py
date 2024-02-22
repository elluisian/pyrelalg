from pyrelalg.Operators import *

sch = DBSchema(("A", "B",), (INTEGER, INTEGER,))
rel = DBRelation(sch)

rel.insert((1, 2,))

print(rel)