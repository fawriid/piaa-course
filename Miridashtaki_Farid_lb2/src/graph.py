import matplotlib.pyplot as plt
import time
import random

INF = 10**18


def exact_dp_iterative(n, graph):
    cost = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                cost[i][j] = 0
            elif graph[i][j] > -0.5:
                cost[i][j] = graph[i][j]
    
    full_mask = (1 << n) - 1
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1 << 0][0] = 0
    
    for mask in range(1 << n):
        if not (mask & 1):
            continue
        for last in range(n):
            if dp[mask][last] >= INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                if cost[last][nxt] >= INF:
                    continue
                new_mask = mask | (1 << nxt)
                new_cost = dp[mask][last] + cost[last][nxt]
                if new_cost < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = new_cost
                    parent[new_mask][nxt] = last
    
    best_cost = INF
    best_last = -1
    for last in range(n):
        if dp[full_mask][last] < INF and cost[last][0] < INF:
            total = dp[full_mask][last] + cost[last][0]
            if total < best_cost:
                best_cost = total
                best_last = last
    
    if best_cost >= INF:
        return None, None
    
    path = []
    mask = full_mask
    last = best_last
    path.append(last)
    while mask != (1 << 0):
        prev = parent[mask][last]
        path.append(prev)
        mask = mask ^ (1 << last)
        last = prev
    path.reverse()
    path.append(0)
    
    return best_cost, path

def approx_alsh2(n, graph):
    cost = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                cost[i][j] = 0
            elif graph[i][j] > -0.5:
                cost[i][j] = graph[i][j]
    
    visited = [False] * n
    tour = [0]
    visited[0] = True
    
    while len(tour) < n:
        best_vertex = -1
        best_pos = -1
        best_increase = INF
        
        for v in range(n):
            if visited[v]:
                continue
            
            min_to_tour = INF
            for u in tour:
                if cost[u][v] < min_to_tour:
                    min_to_tour = cost[u][v]
            
            if min_to_tour >= INF:
                continue
            
            for pos in range(len(tour)):
                prev = tour[pos]
                nxt = tour[(pos + 1) % len(tour)]
                if cost[prev][v] < INF and cost[v][nxt] < INF:
                    increase = cost[prev][v] + cost[v][nxt] - cost[prev][nxt]
                    if increase < best_increase:
                        best_increase = increase
                        best_vertex = v
                        best_pos = pos + 1
        
        if best_vertex == -1:
            return None, None
        
        tour.insert(best_pos, best_vertex)
        visited[best_vertex] = True
    
    total_cost = 0
    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        if cost[u][v] >= INF:
            return None, None
        total_cost += cost[u][v]
    
    return total_cost, tour + [tour[0]]

# ============ MATRIX GENERATION ============

def generate_symmetric_matrix(n, max_weight=100):
    graph = [[-1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                graph[i][j] = -1
            else:
                w = random.randint(1, max_weight)
                graph[i][j] = float(w)
                graph[j][i] = float(w)
    return graph

# ============ TIME MEASUREMENT ============

def measure_time(algorithm, n, repeats=2):
    times = []
    for _ in range(repeats):
        graph = generate_symmetric_matrix(n, 100)
        start = time.perf_counter()
        algorithm(n, graph)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / repeats

# ============ GENERATE CHARTS ============

def generate_dp_chart():
    print("\n[1] Measuring DP Algorithm (Exact Method)...")
    print("This may take a minute...")
    
    # For DP: only up to n=14 because it becomes slow
    sizes = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    times = []
    
    for n in sizes:
        t = measure_time(exact_dp_iterative, n, repeats=2)
        times.append(t)
        print(f"n = {n:2d} | Time: {t:.6f} seconds")
    
    # Create chart
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8, color='blue')
    plt.xlabel('Размер матрицы (n)', fontsize=12)
    plt.ylabel('Время (секунды)', fontsize=12)
    plt.title('График зависимости затраченного времени от размера матрицы для алгоритма DP', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(sizes)
    
    for x, y in zip(sizes, times):
        plt.annotate(f'{y:.4f}s', (x, y), textcoords="offset points", 
                    xytext=(0, 10), ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('dp_time_chart.png', dpi=150)
    plt.show()
    print("Chart saved as 'dp_time_chart.png'")
    
    return sizes, times

def generate_approx_chart():
    print("\n[2] Measuring ALSh-2 Algorithm (Approximation)...")
    
    # For ALSh-2: can go up to larger n
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    times = []
    
    for n in sizes:
        t = measure_time(approx_alsh2, n, repeats=2)
        times.append(t)
        print(f"n = {n:4d} | Time: {t:.6f} seconds")
    
    # Create chart
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'ro-', linewidth=2, markersize=8, color='red')
    plt.xlabel('Размер матрицы (n)', fontsize=12)
    plt.ylabel('Время (секунды)', fontsize=12)
    plt.title('График зависимости затраченного времени от размера матрицы для алгоритма ALSh-2', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    for x, y in zip(sizes, times):
        plt.annotate(f'{y:.3f}s', (x, y), textcoords="offset points", 
                    xytext=(0, 10), ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('approx_time_chart.png', dpi=150)
    plt.show()
    print("Chart saved as 'approx_time_chart.png'")
    
    return sizes, times

# ============ MAIN ============

def main():
    print("="*60)
    print("GENERATING CHARTS FOR VARIANT 8 REPORT")
    print("="*60)
    
    # Generate DP chart
    dp_sizes, dp_times = generate_dp_chart()
    
    # Generate ALSh-2 chart
    approx_sizes, approx_times = generate_approx_chart()
    
    # Print summary table
    print("\n" + "="*60)
    print("SUMMARY DATA FOR REPORT")
    print("="*60)
    
    print("\nТаблица 1. Время работы DP алгоритма")
    print("-"*40)
    for n, t in zip(dp_sizes, dp_times):
        print(f"{n}\t{t:.6f}")
    
    print("\nТаблица 2. Время работы ALSh-2 алгоритма")
    print("-"*40)
    for n, t in zip(approx_sizes, approx_times):
        print(f"{n}\t{t:.6f}")

if __name__ == "__main__":
    main()