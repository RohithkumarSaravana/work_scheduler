from scheduler.scheduler import Scheduler

scheduler = Scheduler(
    "data/employees.csv",
    "data/tasks.csv"
)

schedule = scheduler.generate_schedule()

print("\nToday's Schedule\n")

for employee, tasks in schedule.items():

    print(employee)

    for task in tasks:

        print("   -", task)

    print()