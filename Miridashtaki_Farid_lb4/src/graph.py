import time
import random
import string
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def compute_prefix(p):
    m = len(p)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and p[k] != p[i]:
            k = pi[k - 1]
        if p[k] == p[i]:
            k += 1
        pi[i] = k
    return pi

def kmp_search(p, t):
    m, n = len(p), len(t)
    pi = compute_prefix(p)
    results = []
    k = 0
    for i in range(n):
        while k > 0 and p[k] != t[i]:
            k = pi[k - 1]
        if p[k] == t[i]:
            k += 1
        if k == m:
            results.append(i - m + 1)
            k = pi[k - 1]
    return results

text_sizes = [1000, 100000, 1000000, 5000000]
pattern_size = 100
chars = string.ascii_lowercase[:4]

print("Running benchmarks...")
times = []
for tsize in text_sizes:
    t = "".join(random.choices(chars, k=tsize))
    p = "".join(random.choices(chars, k=min(pattern_size, tsize)))
    start = time.time()
    kmp_search(p, t)
    elapsed = time.time() - start
    times.append(elapsed)
    print("Text size: " + str(tsize) + " | Time: " + str(round(elapsed, 6)) + "s")

fig, ax = plt.subplots(figsize=(9, 4))

ax.plot(text_sizes, times, marker="o", color="steelblue",
        linewidth=1.5, markersize=5, label="Размер текста")

ax.set_xscale("log")
ax.set_xticks(text_sizes)
ax.get_xaxis().set_major_formatter(
    ticker.FuncFormatter(lambda x, _: "{:,}".format(int(x)).replace(",", "."))
)

ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
ax.yaxis.grid(True, color="lightgrey", linewidth=0.8)
ax.set_axisbelow(True)

ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), frameon=False)

for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color("black")
    spine.set_linewidth(0.8)

ax.tick_params(axis="both", labelsize=9)

plt.tight_layout()
plt.savefig("graph.png", dpi=150, bbox_inches="tight")
plt.show()
print("Graph saved as graph.png")