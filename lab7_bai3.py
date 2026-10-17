from collections import deque


# Tim duong tang luong s -> t tren mang thang du bang BFS, tra ve mang parent (hoac None)
def bfs_augmenting_path(residual, s, t):
    n = len(residual)
    parent = [-1] * n
    parent[s] = s
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in range(n):
            if parent[v] == -1 and residual[u][v] > 0:
                parent[v] = u
                if v == t:
                    return parent
                queue.append(v)
    return None


# Ford-Fulkerson (tim duong tang bang BFS = Edmonds-Karp)
def ford_fulkerson(C, s, t, verbose=False):
    residual = [row[:] for row in C]
    max_flow = 0

    while True:
        parent = bfs_augmenting_path(residual, s, t)
        if parent is None:
            break  # Khong con duong tang luong

        # Truy vet duong di tu t ve s
        path = []
        v = t
        while v != s:
            path.append((parent[v], v))
            v = parent[v]
        path.reverse()

        # Dung luong nghen
        bottleneck = min(residual[u][v] for u, v in path)

        # Cap nhat mang thang du: canh thuan giam, canh nghich tang
        for u, v in path:
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck

        max_flow += bottleneck
        if verbose:
            nodes = [path[0][0]] + [v for _, v in path]
            print(f"  Duong tang luong {nodes}, bottleneck = {bottleneck}")

    return max_flow


if __name__ == "__main__":
    # Ma tran dung luong C (4 dinh: 0, 1, 2, 3)
    C = [
        [0, 10, 10, 0],  # s (0)
        [0, 0,  2,  8],  # u (1)
        [0, 0,  0,  9],  # v (2)
        [0, 0,  0,  0]   # t (3)
    ]
    print("Cac buoc tang luong:")
    print("Luong cuc dai Max Flow (s=0, t=3):", ford_fulkerson(C, 0, 3, verbose=True))  # 17
