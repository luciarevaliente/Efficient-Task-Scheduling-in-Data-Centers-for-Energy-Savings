import random
import numpy as np
import pandas as pd

# Configuración inicial
num_tasks = 25  # Número de tareas
num_processors = 10  # Número de procesadores
num_processes_per_task = (1, 5)  # Rango de procesos por tarea
random.seed(42)
np.random.seed(42)

# Rango ajustado de datos
mi_range = (500, 3000)  # MI entre 500 y 3000
speed_range = (1000, 3000)  # Velocidades de procesadores en MIPS
power_range = (0.5, 2.0)  # Potencias de procesadores en kW
capacity_factor = 20  # Multiplicador para calcular la capacidad basada en velocidad

# Configuración de procesadores
processors = [f"P{i+1}" for i in range(num_processors)]
processor_speeds = {p: random.randint(*speed_range) for p in processors}
processor_powers = {p: round(random.uniform(*power_range), 2) for p in processors}
processor_capacities = {p: processor_speeds[p] * capacity_factor for p in processors}

# Generación de procesos por tarea
processes = []
for task_id in range(1, num_tasks + 1):
    task_name = f"T{task_id}"
    num_processes = random.randint(*num_processes_per_task)

    for process_id in range(1, num_processes + 1):
        process_name = f"T{task_id}_P{process_id}"
        processor = random.choice(processors)  # Procesador asignado
        mi = random.randint(*mi_range)
        speed = processor_speeds[processor]
        power = processor_powers[processor]

        processes.append({
            "Task_ID": task_name,
            "Process_ID": process_name,
            "Processor_ID": processor,
            "MI": mi,
            "Speed": speed,
            "Power": power
        })

# Crear DataFrame de procesos
process_df = pd.DataFrame(processes)
process_df.to_csv("process_dataset.csv", index=False)

# Generación de deadlines ajustados
deadlines = []
for task_id in range(1, num_tasks + 1):
    task_name = f"T{task_id}"
    avg_mi = process_df[process_df["Task_ID"] == task_name]["MI"].mean()
    avg_speed = np.mean(list(processor_speeds.values()))
    deadline = int(avg_mi / avg_speed * random.uniform(1.5, 3))  # Deadline ajustado al tamaño de la tarea
    deadlines.append({"Task_ID": task_name, "Deadline": deadline})

limits_df = pd.DataFrame(deadlines)
limits_df.to_csv("task_deadlines.csv", index=False)

# Generación de capacidades de procesadores
capacities = []
for processor_id in processors:
    capacities.append({
        "Processor_ID": processor_id,
        "Capacity": processor_capacities[processor_id]
    })

capacities_df = pd.DataFrame(capacities)
capacities_df.to_csv("processor_capacities.csv", index=False)

# Generación de demandas horarias realistas
# demand_schedule = []
# hours = list(range(24))

# for hour in hours:
#     peak_factor = 1.5 if 9 <= hour <= 18 else 0.5  # Pico en horas laborales
#     num_tasks_in_hour = int(random.randint(10, 50) * peak_factor)
#     tasks_in_hour = random.sample(range(1, num_tasks + 1), min(num_tasks_in_hour, num_tasks))

#     for task in tasks_in_hour:
#         demand_schedule.append({"Hour": hour, "Task_ID": f"T{task}"})

# schedule_df = pd.DataFrame(demand_schedule)
# schedule_df.to_csv("task_demand_schedule.csv", index=False)

# print("Archivos generados:")
print("- process_dataset.csv")
print("- task_deadlines.csv")
print("- processor_capacities.csv")
# print("- task_demand_schedule.csv")
