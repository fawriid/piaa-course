import time
import random
import matplotlib.pyplot as plt
from collections import deque

ALPHABET = ['A', 'C', 'G', 'T', 'N']

def random_string(length):
    return ''.join(random.choices(ALPHABET, k=length))

def build_trie(patterns):
    son = [{}]
    pats = [[]]
    for pi, p in enumerate(patterns):
        cur = 0
        for c in p:
            if c not in son[cur]:
                son[cur][c] = len(son)
                son.append({})
                pats.append([])
            cur = son[cur][c]
        pats[cur].append(pi + 1)
    return son, pats

def build_automaton(son, pats):
    total = len(son)
    go = [{} for _ in range(total)]
    fail = [0] * total
    term = [-1] * total
    all_chars = set()
    for node in son:
        all_chars |= set(node.keys())
    q = deque()
    for c, s in son[0].items():
        fail[s] = 0
        go[0][c] = s
        q.append(s)
    for c in all_chars:
        if c not in go[0]:
            go[0][c] = 0
    while q:
        v = q.popleft()
        f = fail[v]
        if pats[f]:
            term[v] = f
        elif term[f] != -1:
            term[v] = term[f]
        else:
            term[v] = -1
        for c, s in son[v].items():
            fail[s] = go[fail[v]].get(c, 0)
            go[v][c] = s
            q.append(s)
        for c in all_chars:
            if c not in go[v]:
                go[v][c] = go[fail[v]].get(c, 0)
    return go, fail, term

def search_text(T, go, pats, term):
    cur = 0
    results = []
    for i, c in enumerate(T):
        cur = go[cur].get(c, 0)
        tmp = cur
        while tmp != 0:
            if pats[tmp]:
                for pi in pats[tmp]:
                    results.append((i, pi))
            tmp = term[tmp]
            if tmp == -1:
                break
    return results

# ── TRIE BUILD TIME ──
print("Суммарный размер паттернов | Время создания бора")
pattern_sizes = [10, 100, 1000, 10000, 100000]
trie_times = []
for total_size in pattern_sizes:
    pat_len = max(1, total_size // 20)
    patterns = [random_string(pat_len) for _ in range(20)]
    times = []
    for _ in range(50):
        t0 = time.perf_counter()
        build_trie(patterns)
        times.append(time.perf_counter() - t0)
    avg = sum(times) / len(times)
    trie_times.append(avg)
    print(f"{total_size:<26} {avg:.6f}")

# ── SEARCH TIME ──
print("\nРазмер текста | Время поиска вхождений")
text_sizes = [100, 1000, 10000, 100000, 1000000]
search_times = []
patterns_fixed = [random_string(10) for _ in range(10)]
son, pats = build_trie(patterns_fixed)
go, fail, term = build_automaton(son, pats)
for text_size in text_sizes:
    T = random_string(text_size)
    times = []
    for _ in range(20):
        t0 = time.perf_counter()
        search_text(T, go, pats, term)
        times.append(time.perf_counter() - t0)
    avg = sum(times) / len(times)
    search_times.append(avg)
    print(f"{text_size:<14} {avg:.6f}")

# ── GRAPH 1 ──
plt.figure(figsize=(8, 5))
plt.plot(range(len(pattern_sizes)), trie_times, marker='o', color='steelblue', linewidth=2, label='Время создания бора')
plt.xticks(range(len(pattern_sizes)), labels=[str(x) for x in pattern_sizes])
plt.xlabel('Суммарный размер паттернов')
plt.ylabel('Время (сек)')
plt.title('Зависимость времени создания бора от суммарного размера паттернов')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('graph1_trie.png', dpi=150)
plt.close()
print("\nGraph 1 saved: graph1_trie.png")

# ── GRAPH 2 ──
plt.figure(figsize=(8, 5))
plt.plot(range(len(text_sizes)), search_times, marker='o', color='darkorange', linewidth=2, label='Время поиска вхождений')
plt.xticks(range(len(text_sizes)), labels=[str(x) for x in text_sizes])
plt.xlabel('Размер текста')
plt.ylabel('Время (сек)')
plt.title('Зависимость времени поиска от размера текста')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('graph2_search.png', dpi=150)
plt.close()
print("Graph 2 saved: graph2_search.png")