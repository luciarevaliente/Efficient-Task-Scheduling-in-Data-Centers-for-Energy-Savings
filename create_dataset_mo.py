import random
import numpy as np
import pandas as pd

# Configuració inicial
num_tasks = 25  # Nombre de tasques
num_processors = 10  # Nombre de processadors
num_processes_per_task = (1, 5)  # Rango de processos per tasca
random.seed(42)  # Fixem la llavor de la randomització
np.random.seed(42)  # Fixem la llavor de la randomització per a numpy

# Rango ajustat de dades
mi_range = (500, 3000)  # MI entre 500 i 3000
speed_range = (1000, 3000)  # Velocitats dels processadors en MIPS
power_range = (0.5, 2.0)  # Potències dels processadors en kW
capacity_factor = 20  # Multiplicador per calcular la capacitat basada en la velocitat

# Configuració dels processadors
processors = [f"P{i+1}" for i in range(num_processors)]  # Creem els identificadors dels processadors
processor_speeds = {p: random.randint(*speed_range) for p in processors}  # Velocitat aleatòria per a cada processador
processor_powers = {p: round(random.uniform(*power_range), 2) for p in processors}  # Potència aleatòria per a cada processador
processor_capacities = {p: processor_speeds[p] * capacity_factor for p in processors}  # Capacitat del processador basada en la seva velocitat

# Generació dels processos per tasca
processes = []
for task_id in range(1, num_tasks + 1):  # Iterem per cada tasca
    task_name = f"T{task_id}"  # Nom de la tasca
    num_processes = random.randint(*num_processes_per_task)  # Nombre aleatori de processos per tasca

    for process_id in range(1, num_processes + 1):  # Iterem per cada procés de la tasca
        process_name = f"T{task_id}_P{process_id}"  # Nom del procés
        processor = random.choice(processors)  # Assignem un processador aleatori
        mi = random.randint(*mi_range)  # Assignem un valor aleatori de MI
        speed = processor_speeds[processor]  # Velocitat del processador assignat
        power = processor_powers[processor]  # Potència del processador assignat

        processes.append({
            "Task_ID": task_name,
            "Process_ID": process_name,
            "Processor_ID": processor,
            "MI": mi,
            "Speed": speed,
            "Power": power
        })

# Crear DataFrame de processos
process_df = pd.DataFrame(processes)  # Creem un DataFrame amb la informació dels processos
process_df.to_csv("process_dataset.csv", index=False)  # Guardem el DataFrame en un arxiu CSV

# Generació de deadlines ajustats
deadlines = []
for task_id in range(1, num_tasks + 1):  # Iterem per cada tasca
    task_name = f"T{task_id}"  # Nom de la tasca
    avg_mi = process_df[process_df["Task_ID"] == task_name]["MI"].mean()  # Mitjana de MI per la tasca
    avg_speed = np.mean(list(processor_speeds.values()))  # Mitjana de les velocitats dels processadors
    deadline = int(avg_mi / avg_speed * random.uniform(1.5, 3))  # Calcul de la deadline ajustada
    deadlines.append({"Task_ID": task_name, "Deadline": deadline})

limits_df = pd.DataFrame(deadlines)  # Creem un DataFrame per les deadlines
limits_df.to_csv("task_deadlines.csv", index=False)  # Guardem el DataFrame en un arxiu CSV

# Generació de capacitats dels processadors
capacities = []
for processor_id in processors:  # Iterem per cada processador
    capacities.append({
        "Processor_ID": processor_id,
        "Capacity": processor_capacities[processor_id]  # Capacitat del processador
    })

capacities_df = pd.DataFrame(capacities)  # Creem un DataFrame per les capacitats dels processadors
capacities_df.to_csv("processor_capacities.csv", index=False)  # Guardem el DataFrame en un arxiu CSV

# Generació de demandes horàries realistes (comentat)
# demand_schedule = []
# hours = list(range(24))  # Llista de les hores del dia

# for hour in hours:  # Iterem per cada hora
#     peak_factor = 1.5 if 9 <= hour <= 18 else 0.5  # Factor de pic en hores laborals
#     num_tasks_in_hour = int(random.randint(10, 50) * peak_factor)  # Nombre de tasques per hora ajustat al factor de pic
#     tasks_in_hour = random.sample(range(1, num_tasks + 1), min(num_tasks_in_hour, num_tasks))  # Seleccionem tasques per hora

#     for task in tasks_in_hour:  # Assignem tasques a l'hora
#         demand_schedule.append({"Hour": hour, "Task_ID": f"T{task}"})

# schedule_df = pd.DataFrame(demand_schedule)  # Creem un DataFrame per les demandes horàries
# schedule_df.to_csv("task_demand_schedule.csv", index=False)  # Guardem el DataFrame en un arxiu CSV

# Imprimim els noms dels arxius generats
print("- process_dataset.csv")
print("- task_deadlines.csv")
print("- processor_capacities.csv")
# print("- task_demand_schedule.csv")
