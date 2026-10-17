# Mo phong chuoi Markov: pi_{k+1} = pi_k * P, dung som khi hoi tu (trang thai dung pi*)
def simulate_markov_chain(P, pi_0, num_steps=50, tol=1e-6):
    n = len(pi_0)
    pi = list(pi_0)

    for step in range(1, num_steps + 1):
        # Tinh pi_next = pi * P
        pi_next = [0.0] * n
        for j in range(n):
            pi_next[j] = sum(pi[i] * P[i][j] for i in range(n))

        converged = all(abs(pi_next[j] - pi[j]) < tol for j in range(n))
        pi = pi_next
        if converged:
            print(f"  (Hoi tu sau {step} buoc)")
            break

    return [round(val, 4) for val in pi]


if __name__ == "__main__":
    S = ['Nang', 'Mua']
    P = [
        [0.8, 0.2],  # Nang
        [0.4, 0.6]   # Mua
    ]
    pi_0 = [1.0, 0.0]  # Ngay dau chac chan Nang

    for k in (1, 2, 3):
        print(f"Phan phoi sau {k} ngay (Nang, Mua):", simulate_markov_chain(P, pi_0, k))

    pi_star = simulate_markov_chain(P, pi_0, 50)
    print("Phan phoi xac suat Trang thai dung pi* (Nang, Mua):", pi_star)
    # Ky vong: [0.6667, 0.3333] ~ (2/3 Nang, 1/3 Mua)

# Kiem chung giai tich: pi* = pi* P va pi_N + pi_M = 1
# -> pi_N = 0.8 pi_N + 0.4 pi_M -> 0.2 pi_N = 0.4 pi_M -> pi_N = 2 pi_M -> pi* = (2/3, 1/3).
