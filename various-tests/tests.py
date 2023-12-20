from pyrelalg.Operators import *

sch = DBSchema(("A", "B",), (INTEGER, INTEGER,))
rel = DBRelation(sch)

print(rel)