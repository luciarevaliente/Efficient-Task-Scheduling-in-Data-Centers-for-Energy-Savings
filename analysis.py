import matplotlib.pyplot as plt
import numpy as np

# INICIALITZAR
tasks = np.array([25, 50, 500])
processors = np.array([10, 20, 200])
energy_min = np.array([20.763579848141486, 31.524447557252667, 109.28440365801482])

# Gráfica combinada: Energía mínima vs todas las variables
plt.figure(figsize=(12, 8))

# Energía mínima vs Tareas
plt.plot(tasks, energy_min, marker='o', label='Energía mínima vs Tareas', linestyle='-', color='blue')

# Energía mínima vs Procesadores
plt.plot(processors, energy_min, marker='s', label='Energía mínima vs Procesadores', linestyle='--', color='orange')

# Configuración de la gráfica
plt.title('Energía Mínima en Función de las Variables', fontsize=16)
plt.xlabel('Cantidad (Log)', fontsize=14)
plt.ylabel('Energía Mínima', fontsize=14)
plt.xscale('log')  # Escala logarítmica para tareas y procesadores
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend(fontsize=12)
plt.tight_layout()

# Mostrar la gráfica
plt.show()
