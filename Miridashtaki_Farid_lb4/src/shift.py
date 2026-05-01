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

def kmp_first(p, b):
    m = len(p)
    n = len(b)
    pi = compute_prefix(p)

    print("Prefix function values for each character of the pattern:")
    print(" ".join(list(p)))
    print(" ".join(map(str, pi)))
    print()

    print("Computing cyclic shift")
    print()

    k = 0
    for j in range(2 * n):
        c = b[j % n]
        while k > 0 and p[k] != c:
            print("k > 0 and characters " + p[k] + "(" + str(k) + ") and " + c + "(" + str(j) + ") are different")
            print("k is replaced by previous prefix value = " + str(pi[k - 1]))
            print()
            k = pi[k - 1]
        if p[k] == c:
            if j >= n:
                print("Characters at positions (" + str(k) + ") and (" + str(j % n) + ") - modulo length, matched")
            else:
                print("Characters at positions (" + str(k) + ") and (" + str(j % n) + ") matched")
            k += 1
            print("k increases by 1")
            print("j increases by 1")
            print()
            if k == m:
                pos = j - m + 1
                if pos < n:
                    print("Full match found")
                    print()
                    return pos
                k = pi[k - 1]
        else:
            print("Characters at positions (" + str(k) + ") and (" + str(j % n) + ") are different")
            print("j increases by 1")
            print()
    return -1

a = input().strip()
b = input().strip()

if len(a) != len(b):
    print(-1)
else:
    res = kmp_first(b, a)
    if res == -1:
        print(-1)
        print("A is not a cyclic shift of B")
    else:
        print("Shift by " + str(res))