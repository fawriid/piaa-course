import sys
from collections import deque


def solve_task1():
    T = input()
    n = int(input())
    patterns = []
    for i in range(n):
        patterns.append(input())

    print("=" * 60)
    print("STEP 1: BUILDING TRIE")
    print("=" * 60)

    son = [{}]
    go = [{}]
    fail = [0]
    term = [-1]
    pats = [[]]

    for pi, p in enumerate(patterns):
        cur = 0
        for c in p:
            if c not in son[cur]:
                son[cur][c] = len(son)
                son.append({})
                go.append({})
                fail.append(0)
                term.append(-1)
                pats.append([])
                print(f"  New node {len(son)-1}: parent={cur}, edge='{c}'")
            cur = son[cur][c]
        pats[cur].append(pi + 1)
        print(f"  Pattern {pi+1} '{p}' terminates at node {cur}")

    total_nodes = len(son)
    print(f"\nTrie built: {total_nodes} nodes")

    max_arcs = max(len(son[i]) for i in range(total_nodes))
    max_arcs_nodes = [i for i in range(total_nodes) if len(son[i]) == max_arcs]
    print(f"\n[VARIANT 5] Max arcs from one trie node: {max_arcs}")
    print(f"            Node(s) with max arcs: {max_arcs_nodes}")

    print("\n" + "=" * 60)
    print("STEP 2: BUILDING AUTOMATON (fail links + terminal links) via BFS")
    print("=" * 60)

    q = deque()

    for c, s in son[0].items():
        fail[s] = 0
        go[0][c] = s
        q.append(s)

    all_chars = set()
    for node in son:
        all_chars |= set(node.keys())

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

        print(f"  Node {v}: fail={fail[v]}, term={term[v]}, "
              f"trie_arcs={list(son[v].keys())}, patterns={pats[v]}")

        for c, s in son[v].items():
            fail[s] = go[fail[v]].get(c, 0)
            go[v][c] = s
            q.append(s)

        for c in all_chars:
            if c not in go[v]:
                go[v][c] = go[fail[v]].get(c, 0)

    print("\n" + "=" * 60)
    print("STEP 3: FULL AUTOMATON DESCRIPTION (every node)")
    print("=" * 60)
    for i in range(total_nodes):
        print(f"  Node {i:3d} | trie_children={son[i]} | "
              f"go={go[i]} | fail={fail[i]} | "
              f"term={term[i]} | patterns={pats[i]}")

    print("\n" + "=" * 60)
    print("STEP 4: SEARCHING TEXT")
    print("=" * 60)
    print(f"  Text = '{T}'")
    print()

    results = []
    covered = [False] * len(T)
    cur = 0

    for i, c in enumerate(T):
        prev = cur
        cur = go[cur].get(c, 0)
        print(f"  i={i+1} char='{c}': state {prev} -> {cur}")

        tmp = cur
        while tmp != 0:
            if pats[tmp]:
                for pi in pats[tmp]:
                    plen = len(patterns[pi - 1])
                    start = i - plen + 2
                    results.append((start, pi))
                    print(f"    [via node {tmp}] Found pattern {pi} "
                          f"'{patterns[pi-1]}' at position {start}")
                    for x in range(i - plen + 1, i + 1):
                        covered[x] = True
            if tmp == cur:
                tmp = term[tmp]
            else:
                tmp = term[tmp]
            if tmp == -1:
                break

    print("\n" + "=" * 60)
    print("FINAL RESULTS (sorted by position then pattern number)")
    print("=" * 60)
    results.sort()
    for pos, pi in results:
        print(f"{pos} {pi}")

    remainder = ''.join(T[i] for i in range(len(T)) if not covered[i])
    print(f"\n[VARIANT 5] Remainder after cutting all found patterns: '{remainder}'")


def solve_task2():
    T = input()
    P = input()
    wildcard = input()

    print("\n" + "=" * 60)
    print("WILDCARD SEARCH")
    print("=" * 60)
    print(f"  Text:     '{T}'")
    print(f"  Pattern:  '{P}'")
    print(f"  Wildcard: '{wildcard}'")

    print("\n--- Step 1: Splitting pattern into chunks ---")
    chunks = []
    i = 0
    while i < len(P):
        if P[i] == wildcard:
            i += 1
        else:
            j = i
            while j < len(P) and P[j] != wildcard:
                j += 1
            chunks.append((i, P[i:j]))
            print(f"  Chunk: '{P[i:j]}' at pattern position {i}")
            i = j

    k = len(chunks)
    if k == 0:
        pat_len = len(P)
        for pos in range(1, len(T) - pat_len + 2):
            print(pos)
        return

    print("\n--- Step 2: Building Aho-Corasick on chunks ---")

    son = [{}]
    go = [{}]
    fail = [0]
    term = [-1]
    pats = [[]]

    for ci, (lpos, chunk) in enumerate(chunks):
        cur = 0
        for c in chunk:
            if c not in son[cur]:
                son[cur][c] = len(son)
                son.append({})
                go.append({})
                fail.append(0)
                term.append(-1)
                pats.append([])
                print(f"  New node {len(son)-1}: parent={cur}, edge='{c}'")
            cur = son[cur][c]
        pats[cur].append((ci, lpos, len(chunk)))
        print(f"  Chunk '{chunk}' terminates at node {cur}")

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

    print("\n--- Step 3: Searching text for chunks ---")
    n = len(T)
    pat_len = len(P)
    C = [0] * (n + 2)

    cur = 0
    for i, c in enumerate(T):
        prev = cur
        cur = go[cur].get(c, 0)
        print(f"  i={i+1} char='{c}': state {prev} -> {cur}")

        tmp = cur
        while tmp != 0:
            if pats[tmp]:
                for (ci, lpos, clen) in pats[tmp]:
                    start = i - clen - lpos + 1
                    if 0 <= start and start + pat_len <= n:
                        C[start] += 1
                        print(f"    Chunk '{chunks[ci][1]}' found, "
                              f"pattern would start at {start+1} "
                              f"(C[{start}]={C[start]})")
            if tmp == cur:
                tmp = term[tmp]
            else:
                tmp = term[tmp]
            if tmp == -1:
                break

    print("\n--- Step 4: Checking counter array ---")
    results = []
    for i in range(n):
        if C[i] == k and i + pat_len <= n:
            results.append(i + 1)
            print(f"  Position {i+1}: C[{i}]={C[i]} == {k} -> MATCH")

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    for pos in results:
        print(pos)


# ── MENU ──────────────────────────────────────────────────
print("Выберите задание (1 или 2):")
choice = input().strip()

if choice == "1":
    solve_task1()
elif choice == "2":
    solve_task2()
else:
    print("Неверный выбор. Введите 1 или 2.")