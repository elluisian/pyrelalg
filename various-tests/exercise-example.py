from pyrelalg.Operators import *


employeesSchema = DBSchema(
    ("Serial", "Name", "Age", "Salary",),
    {
        "Serial": INTEGER,
        "Name": STRING,
        "Age": INTEGER,
        "Salary": INTEGER,
    },
)
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




supervisionSchema = DBSchema(
    ("Chief", "Employee",),
    {
        "Chief": INTEGER,
        "Employee": INTEGER,
    },
)
supervisionInst = DBInstance(supervisionSchema)
supervisionInst.insert((210, 101,))
supervisionInst.insert((210, 103,))
supervisionInst.insert((210, 104,))
supervisionInst.insert((231, 105,))
supervisionInst.insert((301, 210,))
supervisionInst.insert((301, 231,))
supervisionInst.insert((375, 252,))



print("Employees table")
print(employeesInst)



print("\n\nSupervision table")
print(supervisionInst)



print("\n\n\n\nShow name and age of all the employees whose salary is greater than 40")
r = project(
    select(
        employeesInst,
        lambda x : x["Salary"] > 40
    ),
    ("Name", "Age",)
)
print(r)



print("\n\n\n\nGiven the chiefs of the employees whose salary is greater than 40, show their serial number")
# Natural join + rename can be used, but theta join is recommended
r = project(
    natural_join(
        rename(
            select(
                employeesInst,
                lambda x : x["Salary"] > 40
            ),
            ("Employee",),
            ("Serial",)
        ),
        supervisionInst
    ),
    ("Chief",)
)


r = project(
    theta_join(
        select(
            employeesInst,
            lambda x : x["Salary"] > 40
        ),
        supervisionInst,
        lambda x : x["Employee"] == x["Serial"]
    ),
    ("Chief",)
)


print(r)



print("\n\n\n\nShow serial, name and salary of both, the employees whose salary is greater than the chief's and the chief itself.")
r_1 = rename(
    employeesInst,
    ("SerialC", "NameC", "AgeC", "SalaryC",),
    ("Serial", "Name", "Age", "Salary",)
)


r_2 = theta_join(
    employeesInst,
    theta_join(
        r_1,
        supervisionInst,
        lambda x : x["Chief"] == x["SerialC"]
    ),
    lambda x : x["Employee"] == x["Serial"]
)

r = project(
    select(
        r_2,
        lambda x : x["Salary"] > x["SalaryC"]
    ),
    ("Serial", "Name", "Salary", "SerialC", "NameC", "SalaryC",)
)

print(r)



print("\n\n\n\nShow serial and name of chiefs who supervise ONLY employees with a salary greater than 40")


r_1 = select(
    employeesInst,
    lambda x : x["Salary"] <= 40
)

r_2 = project(
    theta_join(
        supervisionInst,
        r_1,
        lambda x : x["Employee"] == x["Serial"]
    ),
    ("Chief",)
)


r_3 = difference(
    project(
        supervisionInst,
        ("Chief",)
    ),
    r_2
)

r = project(
    theta_join(
        r_3,
        employeesInst,
        lambda x : x["Chief"] == x["Serial"]
    ),
    ("Serial", "Name",)
)

print(r)