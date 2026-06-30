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

import pandas as pd

class Scheduler:

    def __init__(self, employee_file, task_file):
        self.employees = pd.read_csv(employee_file)
        self.tasks = pd.read_csv(task_file)

    def generate_schedule(self):

        schedule = {}

        # Group by shift
        for shift in self.tasks["Shift"].unique():

            shift_tasks = self.tasks[self.tasks["Shift"] == shift]["Task"].tolist()
            shift_employees = self.employees[self.employees["Shift"] == shift]["Name"].tolist()

            if not shift_employees:
                continue

            schedule[shift] = {}

            for i, task in enumerate(shift_tasks):

                employee = shift_employees[i % len(shift_employees)]

                if employee not in schedule[shift]:
                    schedule[shift][employee] = []

                schedule[shift][employee].append(task)

        return schedule