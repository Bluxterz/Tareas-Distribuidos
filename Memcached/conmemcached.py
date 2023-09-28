import json
import random
import time
import matplotlib.pyplot as plt
import memcache

# Configura el cliente Memcached
mc = memcache.Client(['localhost:11211'], debug=0)

# Initialize variables to track metrics
total_time_in_cache = 0
total_time_saved = 0
average_time_with_cache = 0
total_cache_hits = 0

def load_data(file_path="./cars.json"):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def find_car_by_id(data, target_id):
    # Intenta obtener el resultado de Memcached
    result = mc.get(str(target_id))
    if result:
        return json.loads(result)

    # Si no está en caché, busca en los datos con un delay entre 1 y 3 segundos
    delay = random.uniform(1, 3)
    time.sleep(delay)  # Add a random delay between 1 and 3 seconds
    start_time = time.time()
    for car in data:
        if car["id"] == target_id:
            # Agrega el resultado a la caché
            mc.set(str(target_id), json.dumps(car))
            end_time = time.time()
            search_time = end_time - start_time + delay  # Include delay in search time
            return car
    return None

def simulate_normal_distribution_searches(data, total_searches):
    found_count = 0
    search_times = []
    query_id_vs_frequency = {}  # For Query ID vs. Frequency

    for i in range(total_searches):
        start_time = time.time()

        # Genera un ID de búsqueda que sigue una distribución normal
        mean = len(data) // 2  # Media para la distribución normal
        std_deviation = len(data) // 6  # Desviación estándar para la distribución normal
        target_id = int(random.normalvariate(mean, std_deviation))
        target_id = max(1, min(len(data), target_id))  # Asegura que el ID esté dentro del rango

        result = find_car_by_id(data, target_id)

        end_time = time.time()
        search_time = end_time - start_time
        search_times.append(search_time)

        if result:
            found_count += 1

        # Track query ID vs. Frequency
        if target_id in query_id_vs_frequency:
            query_id_vs_frequency[target_id] += 1
        else:
            query_id_vs_frequency[target_id] = 1

        # Print query time in real-time
        print(f"Query {i + 1} - Time: {search_time:.5f} seconds")

    print(f"Simulación de distribución normal: Se encontraron {found_count} autos en {total_searches} búsquedas.")

    global total_time_in_cache, total_time_saved, average_time_with_cache, total_cache_hits

    # Calculate metrics
    total_time_in_cache += sum(search_times)
    total_time_saved += max(0, (3 + 0.001) * total_searches - total_time_in_cache)
    average_time_with_cache = total_time_in_cache / total_searches
    total_cache_hits += len([time for time in search_times if time < 1])

    # Display metrics in the terminal
    print(f"Total time in cache: {total_time_in_cache:.2f} seconds")
    print(f"Total time saved thanks to cache: {total_time_saved:.2f} seconds")
    print(f"Average time per query with cache: {average_time_with_cache:.5f} seconds")
    print(f"Total cache hits: {total_cache_hits}")

    # Generate Query ID vs. Frequency graph for distribution normal
    query_ids = list(query_id_vs_frequency.keys())
    frequencies = [query_id_vs_frequency[qid] for qid in query_ids]
    plt.bar(query_ids, frequencies)
    plt.xlabel("Query ID")
    plt.ylabel("Frequency")
    plt.title("Query ID vs. Frequency (Distribution Normal)")
    plt.show()

def simulate_constant_frequency_searches(data, total_searches):
    found_count = 0
    search_times = []
    query_id_vs_frequency = {}  # For Query ID vs. Frequency

    for i in range(total_searches):
        start_time = time.time()

        # Usa una frecuencia constante de 1 para el ID de búsqueda
        target_id = i + 1

        result = find_car_by_id(data, target_id)

        end_time = time.time()
        search_time = end_time - start_time
        search_times.append(search_time)

        if result:
            found_count += 1

        # Track query ID vs. Frequency
        if target_id in query_id_vs_frequency:
            query_id_vs_frequency[target_id] += 1
        else:
            query_id_vs_frequency[target_id] = 1

        # Print query time in real-time
        print(f"Query {i + 1} - Time: {search_time:.5f} seconds")

    print(f"Simulación de frecuencia constante: Se encontraron {found_count} autos en {total_searches} búsquedas.")

    global total_time_in_cache, total_time_saved, average_time_with_cache, total_cache_hits

    # Calculate metrics
    total_time_in_cache += sum(search_times)
    total_time_saved += max(0, (3 + 0.001) * total_searches - total_time_in_cache)
    average_time_with_cache = total_time_in_cache / total_searches
    total_cache_hits += len([time for time in search_times if time < 1])

    # Display metrics in the terminal
    print(f"Total time in cache: {total_time_in_cache:.2f} seconds")
    print(f"Total time saved thanks to cache: {total_time_saved:.2f} seconds")
    print(f"Average time per query with cache: {average_time_with_cache:.5f} seconds")
    print(f"Total cache hits: {total_cache_hits}")

    # Generate Query ID vs. Frequency graph for constant frequency
    query_ids = list(query_id_vs_frequency.keys())
    frequencies = [query_id_vs_frequency[qid] for qid in query_ids]
    plt.bar(query_ids, frequencies)
    plt.xlabel("Query ID")
    plt.ylabel("Frequency")
    plt.title("Query ID vs. Frequency (Constant Frequency)")
    plt.show()

def user_menu(data):
    while True:
        print("\nChoose an operation:")
        print("1. Simulate Normal Distribution Searches")
        print("2. Simulate Constant Frequency Searches")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            total_searches = int(input("Enter the total number of searches to simulate: "))
            simulate_normal_distribution_searches(data, total_searches)
        elif choice == "2":
            total_searches = int(input("Enter the total number of searches to simulate: "))
            simulate_constant_frequency_searches(data, total_searches)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    # Cargar datos desde el archivo JSON
    data = load_data()
    user_menu(data)

