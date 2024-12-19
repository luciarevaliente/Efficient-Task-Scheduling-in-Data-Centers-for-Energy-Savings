import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum

# Carregar els datasets des de fitxers CSV
# `task_deadlines` conté les dates límit per a cada tasca
# `processor_capacities` conté les capacitats màximes de cada processador
# `process_dataset` conté informació sobre el temps i energia requerida per processar cada tasca en cada processador
task_deadlines = pd.read_csv("task_deadlines.csv")
processor_capacities = pd.read_csv("processor_capacities.csv")
process_dataset = pd.read_csv("process_dataset.csv")

# Crear el problema d'optimització
# Nom del problema: "Minimitzar_Energia"
# Tipus de problema: Minimització
problem = LpProblem("Minimitzar_Energia", LpMinimize)

# Variables de decisió: xij = 1 si la tasca i s'assigna al processador j, 0 altrament
x_vars = {}  # Diccionari per guardar les variables binàries
for _, row in process_dataset.iterrows():
    x_vars[(row['Task_ID'], row['Processor_ID'])] = LpVariable(
        f"x_{row['Task_ID']}_{row['Processor_ID']}", cat="Binary"
    )

# Funció objectiu: Minimitzar l'energia total consumida
# Energia consumida per una tasca: Power * MI / Speed, on:
# - `Power`: Potència consumida pel processador
# - `MI`: Instruccions a executar
# - `Speed`: Velocitat del processador
total_energy = lpSum(
    x_vars[(row['Task_ID'], row['Processor_ID'])] * row['Power'] * row['MI'] / row['Speed']
    for _, row in process_dataset.iterrows()
)
problem += total_energy  # Afegir la funció objectiu al problema

# Restricció 1: Cada tasca ha de complir amb la seva data límit
for task_id in task_deadlines['Task_ID']:
    # Obtenir la data límit per a la tasca
    deadline = task_deadlines.loc[task_deadlines['Task_ID'] == task_id, 'Deadline'].values[0]
    # Afegir la restricció: temps d'execució <= data límit
    problem += lpSum(
        x_vars[(task_id, row['Processor_ID'])] * row['MI'] / row['Speed']
        for _, row in process_dataset[process_dataset['Task_ID'] == task_id].iterrows()
    ) <= deadline

# Restricció 2: No excedir la capacitat màxima de cada processador
for processor_id in processor_capacities['Processor_ID']:
    # Obtenir la capacitat del processador
    capacity = processor_capacities.loc[processor_capacities['Processor_ID'] == processor_id, 'Capacity'].values[0]
    # Afegir la restricció: càrrega total <= capacitat
    problem += lpSum(
        x_vars[(row['Task_ID'], processor_id)] * row['MI']
        for _, row in process_dataset[process_dataset['Processor_ID'] == processor_id].iterrows()
    ) <= capacity

# Restricció 3: Cada tasca s'ha d'assignar exactament a un processador
for task_id in task_deadlines['Task_ID']:
    # Afegir la restricció: sumatori de xij per a tots els processadors = 1
    problem += lpSum(
        x_vars[(task_id, row['Processor_ID'])]
        for _, row in process_dataset[process_dataset['Task_ID'] == task_id].iterrows()
    ) == 1

# Resoldre el problema
problem.solve()

# Mostrar els resultats
print("Estat de la solució:", problem.status)  # Estat del problema (Òptim, No factible, etc.)
for v in problem.variables():
    if v.varValue > 0:  # Només mostrar les variables assignades
        print(v.name, "=", v.varValue)

# Mostrar el valor mínim de l'energia
print("Energia mínima:", problem.objective.value())
