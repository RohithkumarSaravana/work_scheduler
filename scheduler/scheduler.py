# import pandas as pd

# class Scheduler:

#     def __init__(self, employee_file, task_file):

#         self.employees = pd.read_csv(employee_file)

#         self.tasks = pd.read_csv(task_file)

#     def generate_schedule(self):

#         schedule = {}

#         employees = self.employees["Name"].tolist()

#         tasks = self.tasks["Task"].tolist()

#         for i, task in enumerate(tasks):

#             employee = employees[i % len(employees)]

#             if employee not in schedule:
#                 schedule[employee] = []

#             schedule[employee].append(task)

#         return schedule


#before model based system
# import pandas as pd

# class Scheduler:

#     def __init__(self, employee_file, task_file):
#         self.employees = pd.read_csv(employee_file)
#         self.tasks = pd.read_csv(task_file)

#     def generate_schedule(self):

#         schedule = {}

#         # Group by shift
#         for shift in self.tasks["Shift"].unique():

#             shift_tasks = self.tasks[self.tasks["Shift"] == shift]["Task"].tolist()
#             shift_employees = self.employees[self.employees["Shift"] == shift]["Name"].tolist()

#             if not shift_employees:
#                 continue

#             schedule[shift] = {}

#             for i, task in enumerate(shift_tasks):

#                 employee = shift_employees[i % len(shift_employees)]

#                 if employee not in schedule[shift]:
#                     schedule[shift][employee] = []

#                 schedule[shift][employee].append(task)

#         return schedule

#model based system
# from models.employee import Employee
# from models.task import Task
# import pandas as pd
# from collections import defaultdict


# class Scheduler:

#     def __init__(self, employee_file, task_file):

#         df_employees = pd.read_csv(employee_file)
#         df_tasks = pd.read_csv(task_file)

#         # Convert CSV → Employee objects
#         self.employees = [
#             Employee(
#                 name=row["Name"],
#                 shift=row["Shift"],
#                 employment_type=row["Type"]
#             )
#             for _, row in df_employees.iterrows()
#         ]

#         # Convert CSV → Task objects
#         self.tasks = [
#             Task(
#                 name=row["Task"],
#                 shift=row["Shift"]
#             )
#             for _, row in df_tasks.iterrows()
#         ]


#     def generate_schedule(self):

#         schedule = {}

#         # process shift by shift
#         for shift in set(t.shift for t in self.tasks):

#             # filter tasks by shift
#             shift_tasks = [t for t in self.tasks if t.shift == shift]

#             # filter employees by shift
#             shift_employees = [e for e in self.employees if e.shift == shift]

#             if not shift_employees:
#                 continue

#             schedule[shift] = defaultdict(list)

#             for i, task in enumerate(shift_tasks):

#                 employee = shift_employees[i % len(shift_employees)]

#                 schedule[shift][employee.name].append(task.name)

#         return schedule
##ADDING ABSENT TO THE SYSTEM
from models.employee import Employee
from models.task import Task
import pandas as pd
from collections import defaultdict


class Scheduler:

    def __init__(self, employee_file, task_file, absent_today=None):

        self.absent_today = absent_today or []

        df_employees = pd.read_csv(employee_file)
        df_tasks = pd.read_csv(task_file)

        # Convert CSV → Employee objects
        self.employees = [
            Employee(
                name=row["Name"],
                shift=row["Shift"],
                employment_type=row["Type"]
            )
            for _, row in df_employees.iterrows()
        ]

        # Convert CSV → Task objects
        self.tasks = [
            Task(
                name=row["Task"],
                shift=row["Shift"]
            )
            for _, row in df_tasks.iterrows()
        ]


    def generate_schedule(self):

        schedule = {}

        # process shift by shift
        for shift in set(t.shift for t in self.tasks):

            # filter tasks by shift
            shift_tasks = [t for t in self.tasks if t.shift == shift]

            # 👇 UPDATED: filter employees by shift + absence
            shift_employees = [
                e for e in self.employees
                if e.shift == shift and e.name not in self.absent_today
            ]

            if not shift_employees:
                continue

            schedule[shift] = defaultdict(list)

            for i, task in enumerate(shift_tasks):

                employee = shift_employees[i % len(shift_employees)]

                schedule[shift][employee.name].append(task.name)

        return schedule