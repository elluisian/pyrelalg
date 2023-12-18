from pyrelalg.Operators import *


employeesSchema = DBSchema(
    { "Matr": INTEGER, "Nome": STRING, "Età": INTEGER, "Stipendio": INTEGER },
    ("Matr", "Nome", "Età", "Stipendio",)
)

"""
employeesSchema = DBSchema(
    (("Matr", INTEGER), ("Nome", STRING), ("Età", INTEGER), ("Stipendio", INTEGER),)
)
"""


chiefEmployeesSchema = DBSchema(
    { "Capo": INTEGER, "Impiegato": INTEGER },
    ("Capo", "Impiegato",)
)

"""
chiefEmployeesSchema = DBSchema(
    (("Capo", INTEGER), ("Impiegato", INTEGER),)
)
"""


employeesInst = DBInstance(employeesSchema)
employeesInst.insert((101,   "Mario Rossi", 34, 40,))
employeesInst.insert((103, "Mario Bianchi", 23, 35,))
employeesInst.insert((104,    "Luigi Neri", 38, 61,))
employeesInst.insert((105,     "Nico Bini", 44, 38,))
employeesInst.insert((210,   "Marco Celli", 49, 60,))
employeesInst.insert((231,     "Siro Bisi", 50, 60,))
employeesInst.insert((252,     "Nico Bini", 44, 70,))
employeesInst.insert((301,  "Sergio Rossi", 34, 70,))
employeesInst.insert((375,   "Mario Rossi", 50, 65,))

print("Relazione A")
print(employeesInst)
impiegati = employeesInst


chiefEmployeesInst = DBInstance(chiefEmployeesSchema)
chiefEmployeesInst.insert((210, 101,))
chiefEmployeesInst.insert((210, 103,))
chiefEmployeesInst.insert((210, 104,))
chiefEmployeesInst.insert((231, 105,))
chiefEmployeesInst.insert((301, 210,))
chiefEmployeesInst.insert((301, 231,))
chiefEmployeesInst.insert((375, 252,))

supervisione = chiefEmployeesInst


print("Relazione B")
print(chiefEmployeesInst)



"""
ERRATISSIMO!!
"""
r1 = theta_join(supervisione, impiegati, lambda x : x.getValue("Matr") == x.getValue("Impiegato"))
r2 = rename(impiegati, ("MatrC", "NomeC", "EtàC", "StipendioC",), ("Matr", "Nome", "Età", "Stipendio",))
r3 = theta_join(r1, r2, lambda x : x.getValue("MatrC") == x.getValue("Capo"))
r4 = rename(select(r3, lambda x : x.getValue("Stipendio") > 40), ("MatrC2", "NomeC2", "EtàC2", "StipendioC2", "CapoC2", "ImpiegatoC2", "OldMatr", "OldNome", "OldEtà", "OldStipendio",), ("MatrC", "NomeC", "EtàC", "StipendioC", "Capo", "Impiegato", "Matr", "Nome", "Età", "Stipendio",))
r5 = theta_join(r3, r4, lambda x : x.getValue("MatrC") != x.getValue("MatrC2"))
r = project(r5, ("MatrC", "NomeC",))

print(r)


r1_ = theta_join(supervisione, select(impiegati, lambda x : x.getValue("Stipendio") <= 40), lambda x : x.getValue("Impiegato") == x.getValue("Matr"))
r2_ = difference(project(supervisione, ("Capo",)), project(r1_, ("Capo",)))
r3_ = theta_join(impiegati, r2_, lambda x : x.getValue("Capo") == x.getValue("Matr"))
rcc = project(r3_, ("Matr", "Nome",))

print(rcc)




r21_ = theta_join(supervisione, impiegati, lambda x : x.getValue("Matr") == x.getValue("Impiegato"))
r22_ = rename(impiegati, ("MatrC", "NomeC", "EtàC", "StipendioC",), ("Matr", "Nome", "Età", "Stipendio",))
r23_ = theta_join(r21_, r22_, lambda x : x.getValue("MatrC") == x.getValue("Capo"))
r24_ = project(select(r23_, lambda x : x.getValue("Stipendio") <= 40), ("Capo",))
r25_ = difference(project(r23_, ("Capo",)), r24_)
rcc1 = project(theta_join(r25_, impiegati, lambda x : x.getValue("Matr") == x.getValue("Capo")), ("Matr", "Nome",))

print(rcc1)
