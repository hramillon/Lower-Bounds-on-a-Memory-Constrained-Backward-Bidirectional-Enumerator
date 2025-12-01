"""
Recursive hierarchical checkpoint placement.

Each checkpoint j operates at a different "level" of recursion:
- Checkpoint 0: moves in sequence n_k(i), n_k(i+1), n_k(i+2), ...
- Checkpoint 1: moves in sequence n_{k-1}(j) relative to checkpoint 0
- Checkpoint j: moves in sequence n_{k-j}(m) relative to its parent

Position formula:
pos = n_k(i_0) + n_{k-1}(i_1) + n_{k-2}(i_2) + ... + n_1(i_{k-1})

Each checkpoint tracks its own index in its own n sequence.
"""

import math


class RecursiveCheckpointEnumerator:
    """
    Hierarchical recursive checkpoint management.
    """
    
    def __init__(self, n: int, k: int):
        self.n = n
        self.k = k
        self.pos = 0
        self.ops = 0
        
        self.n_sequences = {}
        for m in range(0, k):
            self.n_sequences[k-m] = self._compute_n_sequence(k-m)

        self.checkpoint_indices = [0] * k
    
    def _binomial(self, n, k):
        """Compute C(n, k)"""
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        k = min(k, n - k)
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result
    
    def _compute_n_sequence(self, m: int) -> list:
        """
        Compute n_m(i) = C(m+i-1, m) for i = 0, 1, 2, ...
        """
        seq = []
        i = 1
        val = 0
        if m == self.k :
            limit = self.n
        else:
            length = len(self.n_sequences[m+1])
            limit = self.n_sequences[m+1][length-1] - self.n_sequences[m+1][length-2] - 1
        while val < limit:
            val = self._binomial(m + i - 1, m)
            seq.append(val)
            i += 1
        return seq
    
    def _get_checkpoint_position(self) -> int:
        """
        Reconstruct absolute position from checkpoint indices.
        
        pos = n_k(i_0) + n_{k-1}(i_1) + ... + n_1(i_{k-1})
        """
        total = 0
        for j in range(self.k):
            m = self.k - j
            idx = self.checkpoint_indices[j]
            total += self.n_sequences[m][idx]
        return total
    
    def _update_checkpoints(self):
        """
        Update checkpoint indices to match current position.
        
        For each checkpoint j (operating at level m = k-j):
        Find index i such that sum of checkpoints 0..j equals n_m(i)
        """
        pos_at_level = self.pos
        
        
        for j in range(self.k):
            m = self.k - j
            seq = self.n_sequences[m]
            
            idx = 0
            if self.checkpoint_indices[j] == 0 :
                start = 0
            else :
                start = self.checkpoint_indices[j]-1
            for i in range(start, len(seq)+1):
                if seq[i] <= pos_at_level:
                    idx = i
                else:
                    break
            if self.checkpoint_indices[j] != idx:
                lower_anchor=0
                for jj in range(self.k):
                    m_prev = self.k - jj
                    seq_prev = self.n_sequences[m_prev]
                    idx_prev = self.checkpoint_indices[jj]
                    
                    candidate = seq_prev[idx_prev]
                    if candidate < seq[idx] and candidate > lower_anchor:
                        lower_anchor = candidate
                
                cost = seq[idx] - lower_anchor
                self.ops += cost
            self.checkpoint_indices[j] = idx
            
            if idx < len(seq):
                pos_at_level -= seq[idx]
            
    
    def next(self) -> bool:
        """Move forward one position."""
        if self.pos >= self.n:
            return False
        
        self.pos += 1
        self.ops += 1
        
        self._update_checkpoints()
        
        return True
    
    def prev(self) -> bool:
        """Move backward one position."""
        if self.pos <= 0:
            return False
        
        target = self.pos - 1
        
        # Find nearest checkpoint before current position
        prev_checkpoints = self.checkpoint_indices[:]
        
        # Decrement from the deepest level that can decrement
        can_decrement = False
        for j in range(self.k - 1, -1, -1):
            if self.checkpoint_indices[j] > 0:
                prev_checkpoints = self.checkpoint_indices[:]
                prev_checkpoints[j] -= 1
                # Propagate to deeper levels
                for jj in range(j + 1, self.k):
                    m = self.k - jj
                    prev_checkpoints[jj] = len(self.n_sequences[m]) - 1
                can_decrement = True
                break
        
        if not can_decrement:
            # All checkpoints at 0, can only go to 0
            self.pos = 0
            self.checkpoint_indices = [0] * self.k
            return True
        
        # Calculate cost: distance to nearest previous checkpoint
        prev_pos = 0
        for j in range(self.k):
            m = self.k - j
            prev_pos += self.n_sequences[m][prev_checkpoints[j]]
        
        cost = target - prev_pos if target >= prev_pos else 0
        self.ops += cost
        
        self.pos = target
        self.checkpoint_indices = prev_checkpoints
        
        return True
    
    def run_full_cycle(self):
        """Execute forward then backward."""
        while self.next():
            pass
        while self.pos > 0:
            self.prev()
    
    def get_checkpoints(self) -> list:
        """Get actual checkpoint positions."""
        checkpoints = []
        pos = 0
        for j in range(self.k):
            m = self.k - j
            idx = self.checkpoint_indices[j]
            pos += self.n_sequences[m][idx]
            checkpoints.append(pos)
        return checkpoints
    
    def get_metrics(self):
        theoretical_bound = self.n ** (1.0 + 1.0 / self.k)
        
        return {
            'n': self.n,
            'k': self.k,
            'ops': self.ops,
            'theoretical_bound': theoretical_bound,
            'ratio_theory': self.ops / theoretical_bound if theoretical_bound > 0 else 0,
            'checkpoints': self.get_checkpoints(),
        }


if __name__ == "__main__":
    print("=" * 120)
    print("RECURSIVE HIERARCHICAL CHECKPOINT ENUMERATOR")
    print("Theoretical bound: T(n, k) ∈ Θ(n^(1 + 1/k))")
    print("=" * 120)
    print()
    
    for k in range(10,11):
        print(f"\n{'='*120}")
        print(f"k = {k} memory cells")
        print(f"{'='*120}")
        
        for n in [32, 128, 512, 2048,4096]:
            enum = RecursiveCheckpointEnumerator(n, k)
            enum.run_full_cycle()
            m = enum.get_metrics()
            
            print(f"n={n:5d}: ops={m['ops']:10d}, n^(1+1/k)={m['theoretical_bound']:10.0f}, "
                  f"ratio={m['ratio_theory']:6.3f}")