import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum

# Carregar els datasets
task_deadlines = pd.read_csv("task_deadlines.csv")
processor_capacities = pd.read_csv("processor_capacities.csv")
process_dataset = pd.read_csv("process_dataset.csv")

# Crear el problema d'optimització
problem = LpProblem("Minimitzar_Energia", LpMinimize)

# Variables de decisió: xij = 1 si la tasca i s'assigna al processador j, 0 altrament
x_vars = {}
for _, row in process_dataset.iterrows():
    x_vars[(row['Task_ID'], row['Processor_ID'])] = LpVariable(
        f"x_{row['Task_ID']}_{row['Processor_ID']}", cat="Binary"
    )

# Funció objectiu: Minimitzar l'energia
total_energy = lpSum(
    x_vars[(row['Task_ID'], row['Processor_ID'])] * row['Power'] * row['MI'] / row['Speed']
    for _, row in process_dataset.iterrows()
)
problem += total_energy

# Restricció 1: Limitació del temps d'execució
for task_id in task_deadlines['Task_ID']:
    deadline = task_deadlines.loc[task_deadlines['Task_ID'] == task_id, 'Deadline'].values[0]
    problem += lpSum(
        x_vars[(task_id, row['Processor_ID'])] * row['MI'] / row['Speed']
        for _, row in process_dataset[process_dataset['Task_ID'] == task_id].iterrows()
    ) <= deadline

# Restricció 2: Capacitat del processador
for processor_id in processor_capacities['Processor_ID']:
    capacity = processor_capacities.loc[processor_capacities['Processor_ID'] == processor_id, 'Capacity'].values[0]
    problem += lpSum(
        x_vars[(row['Task_ID'], processor_id)] * row['MI']
        for _, row in process_dataset[process_dataset['Processor_ID'] == processor_id].iterrows()
    ) <= capacity

# Restricció 3: Assignació de tasques única
for task_id in task_deadlines['Task_ID']:
    problem += lpSum(
        x_vars[(task_id, row['Processor_ID'])]
        for _, row in process_dataset[process_dataset['Task_ID'] == task_id].iterrows()
    ) == 1

# Resoldre el problema
problem.solve()

# Mostrar els resultats
print("Estat de la solució:", problem.status)
for v in problem.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

print("Energia mínima:", problem.objective.value())
