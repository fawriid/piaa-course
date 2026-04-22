# TSP Solver - Variant 8
# Exact method: Iterative Dynamic Programming
# Approximation: ALSh-2 (Nearest Insertion)

import random

INF = 10**18

# generate symmetric matrix (graph[i][j] = graph[j][i])
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

# generate asymmetric matrix
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

# print matrix
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

# print cost table (same as matrix but after we clean it up)
def print_cost_table(n, cost):
    print("\nCost table (INF = no road, 0 = same city):")
    header = "      " + "".join(f"  c{j}  " for j in range(n))
    print(header)
    for i in range(n):
        row = f"  c{i}  "
        for j in range(n):
            if cost[i][j] >= INF:
                row += f"{'INF':>5} "
            else:
                row += f"{int(cost[i][j]):>5} "
        print(row)

# print dp table - only rows that have at least one non-INF value
def print_dp_table(n, dp):
    print("\nDP table (only updated states):")
    print(f"  {'mask (bin)':<12} {'mask':>5}  " + "".join(f"  city{j}" for j in range(n)))
    for mask in range(1 << n):
        row_has_value = any(dp[mask][j] < INF for j in range(n))
        if not row_has_value:
            continue
        bin_mask = format(mask, f'0{n}b')
        row = f"  {bin_mask:<12} {mask:>5}  "
        for j in range(n):
            if dp[mask][j] >= INF:
                row += f"  {'INF':>5}"
            else:
                row += f"  {int(dp[mask][j]):>5}"
        print(row)


def exact_dp_iterative(n, graph):

    # build cost table from graph
    cost = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                cost[i][j] = 0
            elif graph[i][j] > -0.5:
                cost[i][j] = graph[i][j]

    # show the cost table so we can see what roads exist
    print_cost_table(n, cost)

    # full_mask = all cities visited
    full_mask = (1 << n) - 1
    # show full_mask so we know what we are aiming for
    print(f"\nfull_mask = {full_mask} = {format(full_mask, f'0{n}b')} in binary (all cities visited)")

    # dp table and parent table
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    # show the starting point before we begin
    dp[1 << 0][0] = 0
    print(f"\nStarting point: dp[{1<<0}][0] = 0  (only city0 visited, at city0, cost=0)")

    # show every update that happens to dp table
    print("\n--- Filling DP table step by step ---")

    for mask in range(1 << n):
        # city 0 must always be in the mask
        if not (mask & 1):
            continue

        for last in range(n):
            # skip if we never reached this state
            if dp[mask][last] >= INF:
                continue

            for nxt in range(n):
                # skip if already visited
                if mask & (1 << nxt):
                    continue
                # skip if no road
                if cost[last][nxt] >= INF:
                    continue

                new_mask = mask | (1 << nxt)
                new_cost = dp[mask][last] + cost[last][nxt]

                if new_cost < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = new_cost
                    parent[new_mask][nxt] = last

                    # show which state we updated and what the new cost is
                    bin_old = format(mask, f'0{n}b')
                    bin_new = format(new_mask, f'0{n}b')
                    print(f"  mask={bin_old}({mask}) at city{last}  ->  go to city{nxt}  ->  new_mask={bin_new}({new_mask})  cost={int(new_cost)}")

    # show full dp table after everything is filled
    print("\n--- DP table after all updates ---")
    print_dp_table(n, dp)

    # show all options for returning home and which one is cheapest
    print("\n--- Finding best return to city 0 ---")
    best_cost = INF
    best_last = -1
    for last in range(n):
        if dp[full_mask][last] < INF and cost[last][0] < INF:
            total = dp[full_mask][last] + cost[last][0]
            print(f"  End at city{last}: dp[{full_mask}][{last}]={int(dp[full_mask][last])} + cost[{last}][0]={int(cost[last][0])} = {int(total)}")
            if total < best_cost:
                best_cost = total
                best_last = last

    if best_cost >= INF:
        return None, None

    print(f"\nBest: end at city{best_last}, total cost = {int(best_cost)}")

    # show the path we are going to reconstruct backwards
    print("\n--- Reconstructing path ---")
    path = []
    mask = full_mask
    last = best_last
    path.append(last)

    while mask != (1 << 0):
        # show where we came from at each step
        prev = parent[mask][last]
        print(f"  parent[{format(mask, f'0{n}b')}({mask})][city{last}] = city{prev}")
        path.append(prev)
        mask = mask ^ (1 << last)
        last = prev

    path.reverse()
    path.append(0)
    print(f"  Path (reversed + home): {' -> '.join(map(str, path))}")

    return best_cost, path


# ALSh-2 nearest insertion
def approx_alsh2(n, graph):

    # same cost table
    cost = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                cost[i][j] = 0
            elif graph[i][j] > -0.5:
                cost[i][j] = graph[i][j]

    # start tour with city 0
    visited = [False] * n
    tour = [0]
    visited[0] = True

    # show starting tour before we add anything
    print(f"\nStarting tour: {tour}")

    step = 1
    while len(tour) < n:
        best_vertex = -1
        best_pos = -1
        best_increase = INF

        for v in range(n):
            if visited[v]:
                continue

            # find closest city in tour to v
            min_to_tour = INF
            for u in tour:
                if cost[u][v] < min_to_tour:
                    min_to_tour = cost[u][v]

            if min_to_tour >= INF:
                continue

            # find best position to insert v
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

        # show which city we picked, where we put it, and how much it added to the cost
        print(f"\nStep {step}: insert city{best_vertex} at position {best_pos}  (cost increase = {int(best_increase)})")
        tour.insert(best_pos, best_vertex)
        visited[best_vertex] = True
        # show the tour after each insertion
        print(f"  Tour now: {tour}")
        step += 1

    # show cost of each road in the final tour one by one
    print("\n--- Calculating total cost ---")
    total_cost = 0
    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        if cost[u][v] >= INF:
            return None, None
        print(f"  city{u} -> city{v}: cost = {int(cost[u][v])}")
        total_cost += cost[u][v]

    # show the final sum
    print(f"  Total = {int(total_cost)}")

    return total_cost, tour + [tour[0]]


# print final results
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


# main menu
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

        # option 1: symmetric
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

            print("\n" + "="*50)
            print("RUNNING EXACT DP...")
            print("="*50)
            exact_cost, exact_path = exact_dp_iterative(n, graph)

            print("\n" + "="*50)
            print("RUNNING ALSh-2...")
            print("="*50)
            approx_cost, approx_path = approx_alsh2(n, graph)

            print_results(exact_cost, exact_path, approx_cost, approx_path)

        # option 2: asymmetric
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

            print("\n" + "="*50)
            print("RUNNING EXACT DP...")
            print("="*50)
            exact_cost, exact_path = exact_dp_iterative(n, graph)

            print("\n" + "="*50)
            print("RUNNING ALSh-2...")
            print("="*50)
            approx_cost, approx_path = approx_alsh2(n, graph)

            print_results(exact_cost, exact_path, approx_cost, approx_path)

        # option 3: manual input
        elif choice == '3':
            print("\nEnter matrix:")
            n, graph = read_from_stdin()
            print_matrix(n, graph)

            print("\n" + "="*50)
            print("RUNNING EXACT DP...")
            print("="*50)
            exact_cost, exact_path = exact_dp_iterative(n, graph)

            print("\n" + "="*50)
            print("RUNNING ALSh-2...")
            print("="*50)
            approx_cost, approx_path = approx_alsh2(n, graph)

            print_results(exact_cost, exact_path, approx_cost, approx_path)

        # option 4: from file
        elif choice == '4':
            filename = input("Enter filename: ")
            try:
                n, graph = read_from_file(filename)
                print(f"\nLoaded matrix from {filename}")
                print_matrix(n, graph)

                print("\n" + "="*50)
                print("RUNNING EXACT DP...")
                print("="*50)
                exact_cost, exact_path = exact_dp_iterative(n, graph)

                print("\n" + "="*50)
                print("RUNNING ALSh-2...")
                print("="*50)
                approx_cost, approx_path = approx_alsh2(n, graph)

                print_results(exact_cost, exact_path, approx_cost, approx_path)
            except FileNotFoundError:
                print(f"File '{filename}' not found!")
            except Exception as e:
                print(f"Error: {e}")

        # option 5: save
        elif choice == '5':
            if n == 0:
                print("No matrix loaded. Please generate or load a matrix first.")
                continue
            filename = input("Enter filename to save: ")
            save_to_file(n, graph, filename)

        # option 6: show matrix
        elif choice == '6':
            if n == 0:
                print("No matrix loaded. Please generate or load a matrix first.")
            else:
                print_matrix(n, graph)

        # option 7: exit
        elif choice == '7':
            print("\n")
            break

        else:
            print("Invalid choice. Please choose 1-7.")

if __name__ == "__main__":
    main()
