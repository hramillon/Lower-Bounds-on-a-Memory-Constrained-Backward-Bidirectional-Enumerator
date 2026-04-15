import math

class logenumerator:
    def __init__(self, n: int):
        self.n = n
        self.pos = 0
        self.ops = 0
        # On utilise un dictionnaire pour stocker les checkpoints par niveau
        # pour simuler l'accès mémoire. Clé = niveau k, Valeur = position
        self.checkpoints = {0: 0} 
        
    def _update_checkpoints(self):
        """
        La logique de Raskin : pour chaque niveau k, 
        on garde le marqueur correspondant à pos sans ses k derniers bits.
        """
        # Le nombre de niveaux nécessaires est log2(n)
        max_level = math.ceil(math.log2(self.n)) if self.n > 0 else 1
        
        new_checks = {0: 0} # Le début est toujours là
        for k in range(1, max_level + 1):
            # Position du marqueur de niveau k pour la position actuelle
            marker_pos = self.pos & ~((1 << k) - 1)
            new_checks[k] = marker_pos
            
        # On simule le coût de recomputation si un nouveau checkpoint 
        # doit être créé à partir d'un ancien.
        # Dans le modèle Raskin, on ne recule jamais "dans le vide"
        self.checkpoints = new_checks

    def next(self) -> bool:
        if self.pos >= self.n:
            return False
        self.pos += 1
        self.ops += 1
        self._update_checkpoints()
        return True

    def prev(self) -> bool:
        if self.pos <= 0:
            return False
        
        target = self.pos - 1
        
        # Trouver le checkpoint le plus proche derrière la cible
        # (Dans l'algo de Raskin, il y en a toujours un très proche)
        closest_check = 0
        for cp in self.checkpoints.values():
            if cp <= target:
                closest_check = max(closest_check, cp)
        
        # Coût pour reconstruire l'état depuis le checkpoint
        self.ops += (target - closest_check)
        
        self.pos = target
        self._update_checkpoints()
        return True

    def run_full_cycle(self):
        # Aller jusqu'au bout
        while self.next():
            pass
        # Revenir au début
        while self.pos > 0:
            self.prev()

    def get_metrics(self):
        n_logn = math.ceil(self.n * math.log2(self.n))
        return {
            'n': self.n,
            'ops': self.ops,
            'n_logn': n_logn,
            'ratio_logn': self.ops / n_logn if n_logn > 0 else 0,
            'ratio_n': self.ops / self.n if self.n > 0 else 0,
            'mem': len(set(self.checkpoints.values())),
        }
    
if __name__ == "__main__":
    header = f"{'n':>8} | {'Ops/n':>10} | {'Ops/(n log n)':>15} | {'Ops/(n log log n)':>18}"
    print(header)
    print("-" * len(header))
    
    for i in range(7, 16): # n de 128 à 32768
        n = 2**i
        enum = logenumerator(n)
        enum.run_full_cycle()
        
        ops = enum.ops
        log_n = math.log2(n)
        log_log_n = math.log2(log_n) if log_n > 0 else 1
        
        r_n = ops / n
        r_logn = ops / (n * log_n)
        r_loglogn = ops / (n * log_log_n)
        
        print(f"{n:8d} | {r_n:10.3f} | {r_logn:15.3f} | {r_loglogn:18.3f}")