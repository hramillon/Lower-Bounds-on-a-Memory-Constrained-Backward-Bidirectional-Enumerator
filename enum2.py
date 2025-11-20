from functools import lru_cache
import pandas as pd
import matplotlib.pyplot as plt
import math as m
from collections import defaultdict

def argmin_l(l):
    assert(len(l)>0)
    p=0
    v=l[0]
    for i in range(len(l)):
        if l[i] - v < 0 :
            v = l[i]
            p = i
    return p

def argmin_r(l):
    assert(len(l)>0)
    p=0
    v=l[0]
    for i in range(len(l)):
        if l[i] - v <= 0 :
            v = l[i]
            p = i
    return p


def option_list(n,k):
    return [x + T(n - x , k - 1) + T(x -1, k) for x in range(1,n+1)]

@lru_cache(maxsize=None)
def T(n, k):
    if n == 0:
        return 0
    if k == 0:
        return float('inf')
    return min(option_list(n, k))

@lru_cache(maxsize=None)
def optimal_x_l(n,k):
    if n == 0:
        return None
    if k == 0:
        return None
    return argmin_l(option_list(n, k))

@lru_cache(maxsize=None)
def optimal_x_r(n,k):
    if n == 0:
        return None
    if k == 0:
        return None
    return argmin_r(option_list(n, k))
    

def compute_T(max_n, max_k):
    Tableau = [[0] * (max_k + 1) for _ in range(max_n + 1)]
    for k in range(0, max_k):
        for n in range(0, max_n):
            Tableau[n][k] = optimal_x_l(n,k)
    return Tableau
    
max_n = 1024
max_k = 5

T_values = compute_T(max_n, max_k)

### --- Dataset 1 : k = ⌊log₂(n)⌋ ---
data_logk = []
for n in range(max_n + 1):
    k = max(int(m.log2(n)) if n > 0 else 0, 1)
    data_logk.append((n, k,T(n, k)))

df_logk = pd.DataFrame(data_logk, columns=["n", "k","T(n,k)"])
df_logk.to_csv("T_n_logk.csv", index=False)

data_n = []
for n in range(max_n + 1):
    k =n
    data_n.append((n, k, T(n, k)))

df_n = pd.DataFrame(data_n, columns=["n", "k", "T(n,k)"])
df_n.to_csv("T_n_maxn.csv", index=False)

### --- Dataset 2 : toutes les valeurs de k = 1 à max_k ---
data_allk = []
for k in range(1, max_k + 1):
    for n in range(1,max_n + 1):
        if(optimal_x_r(n,k) == optimal_x_l(n,k)) :
            data_allk.append((n, k,optimal_x_l(n,k), T(n, k)))
        
data = []
for k in range(1, max_k + 1):
    for n in range(0, max_n + 1):
        t_val = T(n, k)
        data.append((n, k, t_val))

df = pd.DataFrame(data, columns=["n", "k", "T(n,k)"])

# --- Calcul des différences ΔT(n,k) = T(n,k) - T(n-1,k)
delta_data = []
for k in range(3, max_k + 1):
    for n in range(1, max_n + 1):
        t_now = T(n, k)
        t_prev = T(n, k-1)
        delta_data.append((n, k, t_prev - t_now))

df_delta = pd.DataFrame(delta_data, columns=["n", "k", "ΔT(n,k)"])

df_allk = pd.DataFrame(data_allk, columns=["n", "k", "opt_x" ,"T(n,k)"])
df_allk.to_csv("T_n_allk2.csv", index=False)
"""
### --- Tracer la courbe pour k = n ---
plt.figure(figsize=(10, 6))
plt.plot(df_n["n"], df_n["T(n,k)"], marker='o', label="k = n")
plt.xlabel("n")
plt.ylabel("T(n,k)")
plt.title("T(n, n) en fonction de n")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

"""
### --- Tracer la courbe pour k = ⌊log₂(n)⌋ ---
plt.figure(figsize=(10, 6))
plt.plot(df_logk["n"], df_logk["T(n,k)"], marker='o', label="k = ⌊log₂(n)⌋")
plt.xlabel("n")
plt.ylabel("T(n,k)")
plt.title("T(n, ⌊log₂(n)⌋) en fonction de n")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
"""
### --- Tracer les courbes pour tous les k de 1 à max_k ---
plt.figure(figsize=(10, 6))
for k in range(1, max_k + 1):
    subset = df_allk[df_allk["k"] == k]
    plt.plot(subset["n"], subset["T(n,k)"], marker='o', label=f"k = {k}")
plt.xlabel("n")
plt.ylabel("T(n,k)")
plt.title("T(n,k) en fonction de n pour différents k")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Tracer le graphe des différences
plt.figure(figsize=(10, 6))
for k in range(1, max_k + 1):
    subset = df_delta[df_delta["k"] == k]
    plt.plot(subset["n"], subset["ΔT(n,k)"], label=f"k = {k}")
plt.xlabel("n")
plt.ylabel("ΔT(n,k) = T(n,k) - T(n-1,k)")
plt.title("Différences successives de T(n,k) selon k")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""