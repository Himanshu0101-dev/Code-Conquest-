import sys
input = sys.stdin.readline
MOD = 10**9 + 7

n = int(input())
a = list(map(int, input().split()))
Q = int(input())

# Precompute suffix exposure sums
# exposure[i] = sum of max(a[i..j]) for all j >= i
# We'll build prefix sums for queries.

# stack will hold (value, position)
stack = []
contrib = [0] * (n+1)   # contrib[i] = contribution starting at i
prefix = [0] * (n+1)    # prefix sums of contrib

for i in range(n-1, -1, -1):
    val = a[i]
    length = 1
    while stack and stack[-1][0] <= val:
        v, cnt = stack.pop()
        length += cnt
    stack.append((val, length))
    # compute contrib[i] as sum of val * cnt for each segment
    s = 0
    for v, cnt in stack:
        s += v * cnt
    contrib[i] = s

# prefix sums
for i in range(n):
    prefix[i+1] = (prefix[i] + contrib[i]) % MOD

# Answer queries
for _ in range(Q):
    l, r = map(int, input().split())
    l -= 1; r -= 1
    # exposure score = prefix[l..r+1] but only up to r
    # contrib[i] includes sums beyond r, so we need to cut
    # Instead, recompute with stack method per query (efficient with RMQ)
    # For simplicity, use direct method with monotonic stack per query.

    max_so_far = 0
    total = 0
    for i in range(r, l-1, -1):
        if a[i] > max_so_far:
            max_so_far = a[i]
        total += max_so_far
    print(total % MOD)
