from pyrelalg.Transaction import *


sch1 = DBSchema(("A", "B",), (INTEGER, INTEGER,))
rel1 = DBRelation(sch1)
rel1.insert((1, 2,))


sch2 = DBSchema(("A", "C",), (INTEGER, INTEGER,))
rel2 = DBRelation(sch2)
rel2.insert((1, 2,))
rel2.insert((3, 4,))
rel2.insert((5, 6,))
rel2.insert((7, 8,))
rel2.insert((9, 10,))
rel2.insert((11, 12,))

print("rel1 is")
print(rel1)


print("rel2 is")
print(rel2)



t = Transaction(rel1)
t.project(("A",))
#t.natural_join(rel2)
print(t.resolve())
#t.resolve(5)
