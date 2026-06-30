# from scheduler.scheduler import Scheduler

# scheduler = Scheduler(
#     "data/employees.csv",
#     "data/tasks.csv"
# )

# schedule = scheduler.generate_schedule()

# print("\nToday's Schedule\n")

# for employee, tasks in schedule.items():

#     print(employee)

#     for task in tasks:

#         print("   -", task)

#     print()

# from scheduler.scheduler import Scheduler

# scheduler = Scheduler(
#     "data/employees.csv",
#     "data/tasks.csv"
# )

# schedule = scheduler.generate_schedule()

# for shift, employees in schedule.items():

#     print(f"\n{shift.upper()} SHIFT\n")

#     for employee, tasks in employees.items():

#         print(employee)

#         for task in tasks:
#             print("  -", task)

#         print()


## ADDING ABSENT TO THE SYSTEM
from scheduler.scheduler import Scheduler

# 👇 Ask manager for absent employees
absent_input = input("Enter absent employees IDs (comma separated or N/A): ")

if absent_input.strip().upper() in ["N/A", "NO", "NONE", ""]:
    absent_today = []
else:
    absent_today = [name.strip() for name in absent_input.split(",")]

# 👇 Pass absent list into scheduler
scheduler = Scheduler(
    "data/employees.csv",
    "data/general_tasks.csv",
    absent_today
)

schedule = scheduler.generate_schedule()

# 👇 Print output
for shift, employees in schedule.items():

    print(f"\n{shift.upper()} SHIFT\n")

    for employee, tasks in employees.items():

        print(employee)

        for task in tasks:
            print("  -", task)

        print()