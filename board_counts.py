from math import comb, log2

full_total = 0
for count in range(2, 17):
    total = 0
    for P in range(7):
        for N in range(3):
            for p in range(7):
                for n in range(3):
                    if (P + N + p + n != count or P + N == 0 or p + n == 0):
                        continue

                    boards = (comb(64, P) *
                              comb(64 - P, N) *
                              comb(64 - P - N, p) *
                              comb(64 - P - N - p, n))

                    total += boards

    full_total += total
    print(f"{count} -> {total} in {log2(total)} bits ({full_total} in {log2(full_total)} bits)")
