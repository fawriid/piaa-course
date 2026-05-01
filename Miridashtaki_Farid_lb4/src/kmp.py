import sys
input = sys.stdin.readline

def compute_prefix(p):
    m = len(p)
    pi = [0] * m
    k = 0
    print("Computing prefix function")
    print()
    print("pi[0] = 0 by definition")
    print()
    for i in range(1, m):
        while k > 0 and p[k] != p[i]:
            print("k > 0 and characters " + p[k] + "(" + str(k) + ") and " + p[i] + "(" + str(i) + ") are different")
            print("k is replaced by previous prefix value at index [k-1] = " + str(pi[k - 1]))
            print()
            k = pi[k - 1]
        if p[k] == p[i]:
            print("Characters at positions (" + str(k) + ") and (" + str(i) + ") matched")
            k += 1
            print("k increases by 1")
            pi[i] = k
            print("pi[" + str(i) + "] = " + str(k))
            print("i increases by 1")
            print()
        else:
            print("Characters at positions (" + str(k) + ") and (" + str(i) + ") are different")
            pi[i] = 0
            print("pi[" + str(i) + "] = 0")
            print("i increases by 1")
            print()
    return pi

def kmp_search(p, t):
    m, n = len(p), len(t)
    pi = compute_prefix(p)

    print("Prefix function values for each character of the pattern:")
    print(" ".join(list(p)))
    print(" ".join(map(str, pi)))
    print()

    print("Computing occurrences")
    print()

    results = []
    k = 0
    for i in range(n):
        while k > 0 and p[k] != t[i]:
            print("k > 0 and characters " + t[i] + "(" + str(i) + ") and " + p[k] + "(" + str(k) + ") are different")
            print("k is replaced by previous prefix value = " + str(pi[k - 1]))
            print()
            k = pi[k - 1]
        if p[k] == t[i]:
            print("Characters at text position (" + str(i) + ") and pattern position (" + str(k) + ") matched")
            k += 1
            if k == m:
                start = i - m + 1
                print("Full match found in interval {" + str(start) + ":" + str(i) + "}")
                results.append(start)
                k = pi[k - 1]
                print("k moves to " + str(k))
            else:
                print("k increases by 1")
        else:
            print("Characters at text position (" + str(i) + ") and pattern position (" + str(k) + ") are different")
            if k == 0:
                print("Pattern start did not match current text position. i increases by 1.")
        print()
    return results

p = input().strip()
t = input().strip()

res = kmp_search(p, t)

if res:
    print("Occurrences found:")
    print(','.join(map(str, res)))
else:
    print(-1)