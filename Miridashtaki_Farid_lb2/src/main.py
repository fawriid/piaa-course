# TSP Solver - Variant 8
# Exact method: Iterative Dynamic Programming
# Approximation: ALSh-2 (Nearest Insertion)

import random

INF = 10**18

# Generate symmetric matrix automatically (graph[i][j] = graph[j][i])
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
    
    return n, graph

# Generate arbitrary (asymmetric) matrix automatically
def generate_asymmetric_matrix(n, max_weight=100):
    graph = [[-1.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                graph[i][j] = -1
            else:
                graph[i][j] = float(random.randint(1, max_weight))
    
    return n, graph


def read_from_stdin():
    n = int(input())
    graph = []
    for i in range(n):
        row = list(map(float, input().split()))
        graph.append(row)
        print(f"[{', '.join(str(x) for x in graph[i])}]")
    return n, graph

def read_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    graph = []
    for i in range(1, n + 1):
        row = list(map(float, lines[i].strip().split()))
        graph.append(row)
    return n, graph

def save_to_file(n, graph, filename):
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for i in range(n):
            f.write(' '.join(str(graph[i][j]) for j in range(n)) + '\n')
    print(f"Matrix saved to {filename}")

# Print matrix in readable format
def print_matrix(n, graph):
    print("\nMatrix:")
    for i in range(n):
        row = []
        for j in range(n):
            if graph[i][j] > -0.5:
                row.append(f"{int(graph[i][j]) if graph[i][j] == int(graph[i][j]) else graph[i][j]:>6}")
            else:
                row.append(f"{'INF':>6}")
        print(' '.join(row))

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

# Approximation: ALSh-2 (Nearest Insertion)
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

# Print results
def print_results(exact_cost, exact_path, approx_cost, approx_path):
    print("\n" + "-"*20)
    print("EXACT METHOD (Iterative Dynamic Programming):")
    if exact_cost is None:
        print("no path")
    else:
        print(f"Cost: {exact_cost:.2f}")
        print(f"Path: {'-'.join(map(str, exact_path))}")
    
    print("\nAPPROXIMATION METHOD (ALSh-2 - Nearest Insertion):")
    if approx_cost is None:
        print("no path")
    else:
        print(f"Cost: {approx_cost:.2f}")
        print(f"Path: {'-'.join(map(str, approx_path))}")
    print("-"*20)

# Main program with full menu
def main():
    n = 0
    graph = []
    
    while True:
        
        print("1. Generate SYMMETRIC matrix")
        print("2. Generate ARBITRARY matrix")
        print("3. Build matrix (manual input)")
        print("4. Load matrix from file")
        print("5. Save current matrix")
        print("6. Show current matrix")
        print("7. Exit")
        print("-"*50)
        
        choice = input("Choose 1/2/3/4/5/6/7: ").strip()
        
        # Option 1: Generate symmetric matrix automatically
        if choice == '1':
            n = int(input("Enter number of cities (n): "))
            max_w = input("Max weight: ")
            if max_w.strip() == "":
                max_w = 100
            else:
                max_w = int(max_w)
            n, graph = generate_symmetric_matrix(n, max_w)
            print(f"\nGenerated SYMMETRIC matrix ({n}x{n}) with weights 1..{max_w}")
            print_matrix(n, graph)
            
            exact_cost, exact_path = exact_dp_iterative(n, graph)
            approx_cost, approx_path = approx_alsh2(n, graph)
            print_results(exact_cost, exact_path, approx_cost, approx_path)
        
        # Option 2: Generate arbitrary (asymmetric) matrix automatically
        elif choice == '2':
            n = int(input("Enter number of cities (n): "))
            max_w = input("Max weight: ")
            if max_w.strip() == "":
                max_w = 100
            else:
                max_w = int(max_w)
            n, graph = generate_asymmetric_matrix(n, max_w)
            print(f"\nGenerated ARBITRARY matrix ({n}x{n}) with weights 1..{max_w}")
            print_matrix(n, graph)
            
            exact_cost, exact_path = exact_dp_iterative(n, graph)
            approx_cost, approx_path = approx_alsh2(n, graph)
            print_results(exact_cost, exact_path, approx_cost, approx_path)
        
        # Option 3: Read from keyboard (
        elif choice == '3':
            print("\nEnter matrix:")
            # print("First line: number of cities")
            # print("Next n lines: n numbers each (-1 = no edge)")
            n, graph = read_from_stdin()
            print_matrix(n, graph)
            
            exact_cost, exact_path = exact_dp_iterative(n, graph)
            approx_cost, approx_path = approx_alsh2(n, graph)
            print_results(exact_cost, exact_path, approx_cost, approx_path)
        
        # Option 4: Read from file
        elif choice == '4':
            filename = input("Enter filename: ")
            try:
                n, graph = read_from_file(filename)
                print(f"\nLoaded matrix from {filename}")
                print_matrix(n, graph)
                
                exact_cost, exact_path = exact_dp_iterative(n, graph)
                approx_cost, approx_path = approx_alsh2(n, graph)
                print_results(exact_cost, exact_path, approx_cost, approx_path)
            except FileNotFoundError:
                print(f"File '{filename}' not found!")
            except Exception as e:
                print(f"Error: {e}")
        
        # Option 5: Save current matrix to file
        elif choice == '5':
            if n == 0:
                print("No matrix loaded. Please generate or load a matrix first.")
                continue
            filename = input("Enter filename to save: ")
            save_to_file(n, graph, filename)
        
        # Option 6: Show current matrix
        elif choice == '6':
            if n == 0:
                print("No matrix loaded. Please generate or load a matrix first.")
            else:
                print_matrix(n, graph)
        
        # Option 7: Exit
        elif choice == '7':
            print("\n")
            break
        
        else:
            print("Invalid choice. Please choose 1-7.")

if __name__ == "__main__":
    main()