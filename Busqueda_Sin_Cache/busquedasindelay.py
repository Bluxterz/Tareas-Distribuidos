import json
import random
import matplotlib.pyplot as plt
import collections
import time

def load_data(file_path="./cars.json"):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def simulate_normal_distribution_searches(data, total_searches):
    id_counts_normal = collections.defaultdict(int)
    total_time = 0
    total_matches = 0

    for i in range(total_searches):
        # Genera un ID de búsqueda que sigue una distribución normal
        target_id = int(random.normalvariate(50, 15))  # Medio y Desviacion estandar
        target_id = max(1, min(99, target_id))  

        # Simula la búsqueda en caché
        start_time = time.time()

        value = None
        for item in data:
            if item["id"] == target_id:
                value = item
                break
        
        elapsed_time = time.time() - start_time

        if value:
            id_counts_normal[target_id] += 1
            total_time += elapsed_time
            total_matches += 1

        # Muestra información de búsqueda
        print(f"Searching {i + 1}/{total_searches}")
        print(f"Tiempo transcurrido: {elapsed_time:.2f} seconds")
        print()

    # Calcular métricas
    total_time_saved = total_searches * (3 + 0.001) - total_time
    average_time_per_query = total_time / total_searches

    # Ordena el diccionario por ID
    sorted_id_counts_normal = dict(sorted(id_counts_normal.items()))

    # Extrae ID y frecuencia
    ids_normal = list(sorted_id_counts_normal.keys())
    frequencies_normal = list(sorted_id_counts_normal.values())

    # Genera el gráfico de frecuencia vs. ID
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.bar(ids_normal, frequencies_normal)
    plt.xlabel("ID")
    plt.ylabel("Frecuencia")
    plt.title("Frecuencia de Consulta vs. ID (Distribución Normal)")

    # Métricas
    plt.subplot(1, 2, 2)
    plt.text(0.5, 0.8, f"Tiempo total: {total_time:.2f} seconds\n"
                        f"Tiempo promedio por consulta: {average_time_per_query:.5f} seconds\n"
                        f"Total de coincidencias encontradas: {total_matches}",
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.axis('off')
    plt.title("Métricas")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Cargar datos desde el archivo JSON
    data = load_data()

    # Solicitar al usuario la cantidad de consultas a realizar
    total_searches = int(input("Ingrese la cantidad de consultas que desea realizar: "))

    # Simular distribución normal
    simulate_normal_distribution_searches(data, total_searches)
