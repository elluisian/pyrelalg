from Operators import *


instA = DBInstance(DBSchema(("Matr", "Nome", "Età", "Stipendio",), (INTEGER, STRING, INTEGER, INTEGER,)))
instA.insert((101,   "Mario Rossi", 34, 40,))
instA.insert((103, "Mario Bianchi", 23, 35,))
instA.insert((104,    "Luigi Neri", 38, 61,))
instA.insert((105,     "Nico Bini", 44, 38,))
instA.insert((210,   "Marco Celli", 49, 60,))
instA.insert((231,     "Siro Bisi", 50, 60,))
instA.insert((252,     "Nico Bini", 44, 70,))
instA.insert((301,  "Sergio Rossi", 34, 70,))
instA.insert((375,   "Mario Rossi", 50, 65,))

print("Relazione A")
print(instA)


"""
instB = DBInstance(DBSchema(("Matr", "Nome", "Età", "Stipendio",), (INTEGER, STRING, INTEGER, INTEGER,)))
instB.insert((101,   "Mario Rossi", 34, 40,))

print("Relazione B")
print(instB)

print("Difference")
instDiff = difference(instA, instB)
print(instDiff)

exit(0)
"""



instB = DBInstance(DBSchema(("Capo", "Impiegato",), (INTEGER, INTEGER,)))
instB.insert((210, 101,))
instB.insert((210, 103,))
instB.insert((210, 104,))
instB.insert((231, 105,))
instB.insert((301, 210,))
instB.insert((301, 231,))
instB.insert((375, 252,))
instB.insert((375, 277,)) # DA RIMUOVERE

print("Relazione B")
print(instB)


print("Rinomino di B (B')")
instB1 = rename(instB, ("Matr",), ("Impiegato",))
print(instB1)

print("Natural join")
njoin = natural_join(instA, instB1)
print(njoin)


print("Left semi-join")
lsjoin = left_semijoin(instA, instB1)
print(lsjoin)

print("Right semi-join")
rsjoin = right_semijoin(instA, instB1)
print(rsjoin)


print("Left anti-join")
lajoin = left_antijoin(instA, instB1)
print(lajoin)


print("Right anti-join")
rajoin = right_antijoin(instA, instB1)
print(rajoin)


print("Left outer-join")
lojoin = left_outerjoin(instA, instB1)
print(lojoin)


print("Right outer-join")
rojoin = right_outerjoin(instA, instB1)
print(rojoin)


print("Full outer-join")
fojoin = full_outerjoin(instA, instB1)
print(fojoin)


print("Self join of Relation A")
print(self_join(instA))

