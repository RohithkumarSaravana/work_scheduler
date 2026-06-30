import pandas as pd

class Scheduler:

    def __init__(self, employee_file, task_file):

        self.employees = pd.read_csv(employee_file)

        self.tasks = pd.read_csv(task_file)

    def generate_schedule(self):

        schedule = {}

        employees = self.employees["Name"].tolist()

        tasks = self.tasks["Task"].tolist()

        for i, task in enumerate(tasks):

            employee = employees[i % len(employees)]

            if employee not in schedule:
                schedule[employee] = []

            schedule[employee].append(task)

        return schedule