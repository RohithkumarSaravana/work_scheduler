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
# from models.employee import Employee
# from models.task import Task
# import pandas as pd
# from collections import defaultdict


# class Scheduler:

#     def __init__(self, employee_file, task_file, absent_today=None):

#         self.absent_today = absent_today or []

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

#             # 👇 UPDATED: filter employees by shift + absence
#             shift_employees = [
#                 e for e in self.employees
#                 if e.shift == shift and e.name not in self.absent_today
#             ]

#             if not shift_employees:
#                 continue

#             schedule[shift] = defaultdict(list)

#             for i, task in enumerate(shift_tasks):

#                 employee = shift_employees[i % len(shift_employees)]

#                 schedule[shift][employee.name].append(task.name)

#         return schedule


##RULE BASED SCHEDULER
from models.employee import Employee
from models.task import Task
import pandas as pd
from collections import defaultdict


class Scheduler:

    def __init__(self, employee_file, task_file, absent_today=None):

        self.absent_today = {
            emp_id.strip().upper()
            for emp_id in (absent_today or [])
        }

        # Load employees
        df_employees = pd.read_csv(employee_file)
        self.employees = [
            Employee(
                employee_id=row["EmployeeID"],
                name=row["Name"],
                shift=row["Shift"],
                employment_type=row["Type"],
                start_time=row["StartTime"],
                end_time=row["EndTime"]
            )
            for _, row in df_employees.iterrows()
        ]

        # Load tasks
        df_tasks = pd.read_csv(task_file)
        self.tasks = [
            Task(
                name=row["Task"],
                shift=row["Shift"],
                duration=row["Duration"]
            )
            for _, row in df_tasks.iterrows()
        ]


    def generate_schedule(self):

        schedule = {}

        # Process shift by shift
        for shift in set(t.shift for t in self.tasks):

            # Filter tasks for shift
            shift_tasks = [t for t in self.tasks if t.shift == shift]

            # Filter available employees
            shift_employees = [
                e for e in self.employees
                if e.shift == shift and e.employee_id not in self.absent_today
            ]

            if not shift_employees:
                continue

            schedule[shift] = defaultdict(list)

            # =========================
            # MORNING / EVENING LOGIC
            # =========================
            if shift in ["Morning", "Evening"]:

                self._assign_round_robin(
                    shift_tasks,
                    shift_employees,
                    schedule,
                    shift
                )

            # =========================
            # NIGHT SHIFT LOGIC
            # =========================
            elif shift == "Night":

                part_time = [e for e in shift_employees if e.employment_type == "Part Time"]
                full_time = [e for e in shift_employees if e.employment_type == "Full Time"]

                # Step 1: assign 2 tasks to each part-time employee
                task_index = 0

                for emp in part_time:
                    for _ in range(2):
                        if task_index >= len(shift_tasks):
                            break

                        task = shift_tasks[task_index]
                        schedule[shift][emp.name].append(task.name)
                        task_index += 1

                # Step 2: assign remaining tasks to full-time employees
                full_time_all = full_time if full_time else shift_employees

                for i in range(task_index, len(shift_tasks)):

                    emp = full_time_all[(i - task_index) % len(full_time_all)]
                    task = shift_tasks[i]

                    schedule[shift][emp.name].append(task.name)

        return schedule


    def _assign_round_robin(self, tasks, employees, schedule, shift):

        for i, task in enumerate(tasks):

            employee = employees[i % len(employees)]
            schedule[shift][employee.name].append(task.name)