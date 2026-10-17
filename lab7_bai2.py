from collections import deque


# Kiem tra do thi hai phia bang BFS to 2 mau (0 va 1)
def is_bipartite_bfs(adj_list, num_nodes):
    color = {}  # 0 hoac 1

    # Duyet moi dinh de xu ly do thi nhieu thanh phan roi rac
    for start in range(num_nodes):
        if start in color:
            continue

        queue = deque([start])
        color[start] = 0

        while queue:
            u = queue.popleft()
            for v in adj_list[u]:
                if v not in color:
                    color[v] = 1 - color[u]  # To mau doi lap
                    queue.append(v)
                elif color[v] == color[u]:
                    return False  # Xung dot mau -> co chu trinh le

    return True


if __name__ == "__main__":
    # Chu trinh 4 dinh (do dai chan) -> Hai phia
    g_even = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
    print("g_even la do thi hai phia:", is_bipartite_bfs(g_even, 4))  # True

    # Chu trinh 3 dinh (tam giac le) -> Khong phai hai phia
    g_odd = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    print("g_odd la do thi hai phia:", is_bipartite_bfs(g_odd, 3))    # False
