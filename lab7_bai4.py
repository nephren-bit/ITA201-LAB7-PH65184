from collections import deque


def ford_fulkerson(C, s, t):
    n = len(C)
    residual = [row[:] for row in C]
    max_flow = 0
    while True:
        # BFS tim duong tang luong
        parent = [-1] * n
        parent[s] = s
        queue = deque([s])
        while queue and parent[t] == -1:
            u = queue.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[t] == -1:
            break

        bottleneck = float('inf')
        v = t
        while v != s:
            bottleneck = min(bottleneck, residual[parent[v]][v])
            v = parent[v]
        v = t
        while v != s:
            residual[parent[v]][v] -= bottleneck
            residual[v][parent[v]] += bottleneck
            v = parent[v]
        max_flow += bottleneck
    return max_flow, residual


# Quy doi Maximum Matching tren do thi hai phia -> Max Flow
def solve_bipartite_matching(L, R, candidate_edges):
    n = len(L) + len(R) + 2
    s, t = n - 2, n - 1  # Voi L = {0, 1}, R = {2, 3}: s = 4, t = 5
    C = [[0] * n for _ in range(n)]

    for u in L:
        C[s][u] = 1          # s -> u, dung luong 1 (moi ung vien nhan toi da 1 viec)
    for u, jobs in candidate_edges.items():
        for v in jobs:
            C[u][v] = 1      # u -> v, dung luong 1
    for v in R:
        C[v][t] = 1          # v -> t, dung luong 1 (moi viec chi giao cho 1 nguoi)

    max_flow, residual = ford_fulkerson(C, s, t)

    # Canh u -> v co luong = 1 khi dung luong thang du giam ve 0
    pairs = [(u, v) for u in L for v in candidate_edges.get(u, [])
             if C[u][v] == 1 and residual[u][v] == 0]
    return max_flow, pairs


if __name__ == "__main__":
    L = [0, 1]                       # Ung vien
    R = [2, 3]                       # Cong viec
    candidate_edges = {0: [2, 3], 1: [2]}

    max_matching, pairs = solve_bipartite_matching(L, R, candidate_edges)
    print("So cap ghep toi da:", max_matching)  # 2
    print("Cac cap ghep:", " , ".join(f"{u}-{v}" for u, v in pairs))  # 0-3 , 1-2
