from collections import deque


# PageRank: PR(j) = (1 - d) / N + d * sum_i PR(i) * P[i][j]
# Dinh treo (khong co lien ket ra) duoc coi nhu nhay deu sang moi dinh.
def compute_pagerank(P_web, damping_factor=0.85, max_iter=100, tol=1e-8):
    n = len(P_web)
    d = damping_factor
    pr = [1.0 / n] * n

    for _ in range(max_iter):
        dangling_mass = sum(pr[i] for i in range(n) if sum(P_web[i]) == 0)
        new_pr = [0.0] * n
        for j in range(n):
            link_sum = sum(pr[i] * P_web[i][j] for i in range(n))
            new_pr[j] = (1 - d) / n + d * (link_sum + dangling_mass / n)

        diff = sum(abs(new_pr[j] - pr[j]) for j in range(n))
        pr = new_pr
        if diff < tol:
            break

    return pr


# Ford-Fulkerson (BFS) tra ve max flow va mang thang du cuoi cung
def max_flow_residual(C, s, t):
    n = len(C)
    residual = [row[:] for row in C]
    flow = 0
    while True:
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
            return flow, residual

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
        flow += bottleneck


# Min-Cut: S = cac dinh con den duoc tu s tren mang thang du sau khi chay xong Max Flow
def find_min_cut(C, s, t):
    flow, residual = max_flow_residual(C, s, t)
    n = len(C)

    S = {s}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in range(n):
            if v not in S and residual[u][v] > 0:
                S.add(v)
                queue.append(v)
    T = set(range(n)) - S

    # Cac canh cat: di tu S sang T trong mang goc (deu bi bao hoa)
    cut_edges = [(u, v, C[u][v]) for u in sorted(S) for v in sorted(T) if C[u][v] > 0]
    return flow, S, T, cut_edges


if __name__ == "__main__":
    names = ['A', 'B', 'C', 'D']

    # 1. PageRank
    P_web = [
        [0.0, 0.5, 0.5, 0.0],  # A -> B, C
        [0.0, 0.0, 1.0, 0.0],  # B -> C
        [1.0, 0.0, 0.0, 0.0],  # C -> A
        [0.0, 0.5, 0.5, 0.0]   # D -> B, C
    ]
    pr = compute_pagerank(P_web)
    print("Diem PageRank (d = 0.85):")
    for name, score in sorted(zip(names, pr), key=lambda x: -x[1]):
        print(f"  Server {name}: {score:.4f}")
    print(f"  Tong = {sum(pr):.4f}")
    # D khong co lien ket den -> chi nhan phan nhay ngau nhien (1 - d) / N = 0.0375

    # 2. Min-Cut: bang thong (Gbps) giua cac server, du lieu di tu A (gateway) den D (storage)
    capacity = [
        # A   B   C   D
        [0, 10,  8,  0],  # A
        [0,  0,  3,  4],  # B
        [0,  0,  0,  7],  # C
        [0,  0,  0,  0]   # D
    ]
    flow, S, T, cut_edges = find_min_cut(capacity, 0, 3)
    print(f"\nMax Flow A -> D = {flow} Gbps")
    print(f"Lat cat hep nhat: S = {{{', '.join(names[i] for i in sorted(S))}}}, "
          f"T = {{{', '.join(names[i] for i in sorted(T))}}}")
    print("Cac duong cap la diem nghen (bao hoa 100%):")
    for u, v, c in cut_edges:
        print(f"  {names[u]} -> {names[v]}: {c} Gbps")
    print(f"Tong dung luong lat cat = {sum(c for _, _, c in cut_edges)} = Max Flow (dinh ly Max-Flow Min-Cut)")
    # Muon tang thong luong toan he thong thi phai nang cap chinh cac cap B->D, C->D;
    # nang cap A->B hay A->C se khong co tac dung.

# Vi sao trang thai dung cua PageRank la vector rieng ung voi tri rieng lambda = 1 cua P^T?
# - PageRank la chuoi Markov: pi_{k+1} = pi_k * G, voi G = d * P + (1 - d)/N * J la ma tran
#   ngau nhien hang (moi hang tong = 1).
# - Trang thai dung thoa pi* = pi* * G. Chuyen vi 2 ve: G^T * pi*^T = 1 * pi*^T, tuc pi*^T chinh
#   la vector rieng cua G^T ung voi tri rieng lambda = 1 (dinh nghia A v = lambda v o Bai 3.1).
# - Vi G ngau nhien hang nen G * 1 = 1 -> lambda = 1 luon la tri rieng cua G (va cua G^T vi cung
#   da thuc dac trung). Theo dinh ly Perron-Frobenius, G duong hoan toan (nho damping) nen
#   lambda = 1 la tri rieng lon nhat, don, vector rieng co the chon duong -> pi* ton tai, duy nhat.
# - Vong lap lap lai pi <- pi * G o tren chinh la Power Iteration tim vector rieng troi; toc do
#   hoi tu phu thuoc |lambda_2| <= d = 0.85.
