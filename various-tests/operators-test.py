from pyrelalg.Operators import *


# Tables data
employeesInst = DBInstance(DBSchema(("Serial", "Name", "Age", "Salary",), (INTEGER, STRING, INTEGER, INTEGER,)))
employeesInst.insert((101,   "Mario Rossi", 34, 40,))
employeesInst.insert((103, "Mario Bianchi", 23, 35,))
employeesInst.insert((104,    "Luigi Neri", 38, 61,))
employeesInst.insert((105,     "Nico Bini", 44, 38,))
employeesInst.insert((210,   "Marco Celli", 49, 60,))
employeesInst.insert((231,     "Siro Bisi", 50, 60,))
employeesInst.insert((252,     "Nico Bini", 44, 70,))
employeesInst.insert((301,  "Sergio Rossi", 34, 70,))
employeesInst.insert((375,   "Mario Rossi", 50, 65,))

print("Employees table:")
print(employeesInst)


supervisionInst = DBInstance(DBSchema(("Chief", "Employee",), (INTEGER, INTEGER,)))
supervisionInst.insert((210, 101,))
supervisionInst.insert((210, 103,))
supervisionInst.insert((210, 104,))
supervisionInst.insert((231, 105,))
supervisionInst.insert((301, 210,))
supervisionInst.insert((301, 231,))
supervisionInst.insert((375, 252,))
supervisionInst.insert((375, 277,)) # TO BE REMOVED





# Showing tables
print("\n\n\n\nSupervision table:")
print(supervisionInst)



print("\n\n\n\nRename of Supervision:")
v = rename(
    supervisionInst,
    ("EmployeeID",),
    ("Employee",)
)
print(v)


print("\n\n\n\nProjection of Supervision:")
v = project(
    supervisionInst,
    ("Employee",),
)
print(v)


# Operations
print("\n\n\n\nNatural join of Employees and Supervision")
v = natural_join(employeesInst, supervisionInst)
print(v)


print("\n\n\n\nLeft semi-join of Employees and Supervision")
v = left_semijoin(employeesInst, supervisionInst)
print(v)

print("\n\n\n\nRight semi-join of Employees and Supervision")
v = right_semijoin(employeesInst, supervisionInst)
print(v)


print("\n\n\n\nLeft anti-join of Employees and Supervision")
v = left_antijoin(employeesInst, supervisionInst)
print(v)


print("\n\n\n\nRight anti-join of Employees and Supervision")
v = right_antijoin(employeesInst, supervisionInst)
print(v)


print("\n\n\n\nLeft outer-join of Employees and Supervision")
v = left_outerjoin(employeesInst, supervisionInst)
print(v)


print("\n\n\n\nRight outer-join of Employees and Supervision")
v = right_outerjoin(employeesInst, supervisionInst)
print(v)


print("\n\n\n\nFull outer-join of Employees and Supervision")
v = full_outerjoin(employeesInst, supervisionInst)
print(v)


print("\n\n\n\nSelf join of Employees and Supervision")
print(self_join(employeesInst))