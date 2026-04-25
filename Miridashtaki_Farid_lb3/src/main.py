import sys

# get the cost of replace and delete, check if special chars apply
def decide_costs(src_char, tgt_char, replace_cost, delete_cost,
                 r_char=None, r_price=None, d_char=None, d_price=None):
    # if we're replacing WITH the special char, use special price
    r = r_price if (r_char and tgt_char == r_char) else replace_cost
    # if we're deleting the special char, use special price
    d = d_price if (d_char and src_char == d_char) else delete_cost
    return r, d


# build the dp table
def get_distance_matrix(s1, s2, replace_cost, insert_cost, delete_cost,
                        r_char=None, r_price=None, d_char=None, d_price=None):
    m, n = len(s1), len(s2)
    # m+1 rows, n+1 cols, all zeros
    d = [[0] * (n + 1) for _ in range(m + 1)]

    # first row: cost of inserting all chars of s2
    for j in range(1, n + 1):
        d[0][j] = d[0][j - 1] + insert_cost

    # first col: cost of deleting all chars of s1
    # need to check if s1[i] is the special deletable char
    for i in range(1, m + 1):
        _, del_cost = decide_costs(s1[i - 1], '', replace_cost, delete_cost,
                                   r_char, r_price, d_char, d_price)
        d[i][0] = d[i - 1][0] + del_cost

    # fill the rest of the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # chars match, no operation needed
            if s1[i - 1] == s2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
                continue
            # get costs for this specific pair of chars
            r, del_cost = decide_costs(s1[i - 1], s2[j - 1], replace_cost, delete_cost,
                                       r_char, r_price, d_char, d_price)
            # pick the cheapest operation
            d[i][j] = min(
                d[i - 1][j - 1] + r,           # replace
                d[i][j - 1]     + insert_cost,  # insert
                d[i - 1][j]     + del_cost       # delete
            )
    return d


# trace back through the table to get the sequence of operations
def traceback_operations(d, s1, s2, replace_cost, insert_cost, delete_cost,
                         r_char=None, r_price=None, d_char=None, d_price=None):
    i, j = len(s1), len(s2)
    solution = ''

    while i > 0 or j > 0:
        # check match first
        if i > 0 and j > 0 and s1[i-1] == s2[j-1] and d[i][j] == d[i-1][j-1]:
            solution += 'M'
            i -= 1; j -= 1
            continue

        r, del_cost = decide_costs(
            s1[i - 1] if i > 0 else '',
            s2[j - 1] if j > 0 else '',
            replace_cost, delete_cost,
            r_char, r_price, d_char, d_price
        )

        if i > 0 and j > 0 and d[i][j] == d[i-1][j-1] + r:
            solution += 'R'
            i -= 1; j -= 1
        elif j > 0 and d[i][j] == d[i][j-1] + insert_cost:
            solution += 'I'
            j -= 1
        else:
            # only delete left
            solution += 'D'
            i -= 1

    # we built it backwards so reverse it
    return solution[::-1]


# apply the operations to s1 and check if we get s2
def check_solution(s1, s2, solution):
    s = list(s1)
    ptr = 0
    for op in solution:
        print(f"\nWord before operation {''.join(s)}")
        if op == 'M':
            print("Operation M - characters match, nothing to do")
            ptr += 1
            continue
        print(f"Operation {op} on position {ptr + 1}")
        if op == 'R':
            print(f"Replace {s[ptr]} with {s2[ptr]}")
            s[ptr] = s2[ptr]
        elif op == 'I':
            print(f"Insert {s2[ptr]}")
            s.insert(ptr, s2[ptr])
        elif op == 'D':
            print(f"Delete {s[ptr]}")
            del s[ptr]
            ptr -= 1
        ptr += 1
        print(f"Word after operation {''.join(s)}")

    print("\nResult vs target:")
    print(''.join(s))
    print(s2)
    if ''.join(s) == s2:
        print("Match!\n")


# just prints the dp table nicely
def print_matrix(d, s1, s2):
    print('    ', *[c for c in s2], sep='  ')
    for i, row in enumerate(d):
        label = ' ' if i == 0 else s1[i - 1]
        print(label, end='  ')
        for val in row:
            print(f"{val:<3}", end=' ')
        print()
    print()


def main():
    print("Enter replacement, insertion and deletion costs:")
    replace_cost, insert_cost, delete_cost = map(int, input().split())

    print("\nEnter first string (A):")
    s1 = input()

    print("\nEnter second string (B):")
    s2 = input()

    # variant 2 specific input
    r_char = r_price = d_char = d_price = None

    print("\nAdd special replacer and special deletable character? (y/n)")
    if input() == 'y':
        print("Enter cost of replacing with special char, and cost of deleting special char:")
        r_price, d_price = map(int, input().split())
        print("Enter the special replacer char and the special deletable char:")
        r_char, d_char = input().split()

    d = get_distance_matrix(s1, s2, replace_cost, insert_cost, delete_cost,
                            r_char, r_price, d_char, d_price)

    solution = traceback_operations(d, s1, s2, replace_cost, insert_cost, delete_cost,
                                    r_char, r_price, d_char, d_price)

    check_solution(s1, s2, solution)
    print_matrix(d, s1, s2)

    print("Edit distance =", d[len(s1)][len(s2)])
    print(solution, s1, s2, sep='\n')


if __name__ == "__main__":
    main()