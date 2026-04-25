import time
import random
import string
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def get_distance_matrix(s1, s2, replace_cost, insert_cost, delete_cost):
    m, n = len(s1), len(s2)
    d = [[0] * (n + 1) for _ in range(m + 1)]

    for j in range(1, n + 1):
        d[0][j] = d[0][j - 1] + insert_cost

    for i in range(1, m + 1):
        d[i][0] = d[i - 1][0] + delete_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
                continue
            d[i][j] = min(
                d[i - 1][j - 1] + replace_cost,
                d[i][j - 1]     + insert_cost,
                d[i - 1][j]     + delete_cost
            )
    return d


def random_string(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def measure_time(n, m):
    s1 = random_string(n)
    s2 = random_string(m)
    start = time.perf_counter()
    get_distance_matrix(s1, s2, 1, 1, 1)
    return time.perf_counter() - start


tests = [
    (10,        10),
    (10,      1000),
    (1000,      10),
    (100,    10000),
    (10000,    100),
    (1000,    1000),
    (1000000,   10),
]

print(f"{'s1':>10} {'s2':>10} {'product':>12} {'time (s)':>12}")
print("-" * 48)

products = []
times    = []

for n, m in tests:
    print(f"Running ({n} x {m})...", end=' ', flush=True)
    t = measure_time(n, m)
    products.append(n * m)
    times.append(t)
    print(f"{t:.5f}s")
    print(f"{n:>10} {m:>10} {n*m:>12} {t:>12.5f}")

# plot — same style as friend's graph
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(products, times, marker='o', color='steelblue', label='Затраченное время')

ax.set_xscale('log')
ax.set_xticks([100, 10000, 1000000, 10000000])
ax.get_xaxis().set_major_formatter(
    ticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))
)

ax.set_xlabel('Произведение размеров строк')
ax.set_ylabel('Затраченное время')
ax.legend()
ax.grid(True, axis='y', alpha=0.4)

plt.tight_layout()
plt.savefig("graph.png", dpi=150)
plt.show()
print("Graph saved as graph.png")