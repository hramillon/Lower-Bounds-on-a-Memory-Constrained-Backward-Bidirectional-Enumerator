import math
from collections import deque


class HierarchicalBinaryTree:
    """
    Generate checkpoint positions in a hierarchical binary tree.
    All positions between 0 and n follow a recursive midpoint structure.
    """
    
    def __init__(self, n: int):
        self.n = n
        # Generate all levels: powers of 2, then midpoints at each level
        self.levels = self._build_levels()
    
    def _build_levels(self) -> dict:
        """
        Build checkpoint positions organized by depth/level.
        levels[d] = list of positions at depth d (in order)
        """
        levels = {}
        
        # Level 0: powers of 2
        level_0 = []
        p = 1
        while p <= self.n:
            level_0.append(p)
            p *= 2
        if level_0[-1] != self.n:
            level_0.append(self.n)
        levels[0] = sorted(set(level_0))
        
        # Level 1+: midpoints between adjacent positions at previous level
        current_level = level_0[:]
        depth = 1
        
        while len(current_level) > 1:
            next_level = []
            for i in range(len(current_level) - 1):
                low = current_level[i]
                high = current_level[i + 1]
                mid = (low + high) // 2
                if mid != low and mid != high:
                    next_level.append(mid)
            
            if not next_level:
                break
            
            levels[depth] = sorted(set(next_level))
            current_level = sorted(set(current_level + next_level))
            depth += 1
        
        return levels
    
    def get_positions_at_depth(self, d: int) -> list:
        """Get all checkpoint positions at depth d."""
        return self.levels.get(d, [])
    
    def get_positions_up_to_depth(self, d: int) -> list:
        """Get all positions up to and including depth d, sorted."""
        result = []
        for i in range(d + 1):
            result.extend(self.levels.get(i, []))
        return sorted(set(result))


class ProperLogNEnumerator:
    """
    Correct implementation with proper checkpoint management.
    
    Maintain exactly k checkpoints using hierarchical tree descent/ascent.
    """
    
    def __init__(self, n: int, k: int = None):
        self.n = n
        if k is None:
            k = max(1, math.ceil(math.log2(n)) if n > 0 else 0)
        self.k = k
        
        self.pos = 0
        self.ops = 0
        
        # Build the hierarchical tree
        self.tree = HierarchicalBinaryTree(n)
        
        # Current checkpoints in memory
        self.checkpoints = deque([0], maxlen=self.k)
        
        # Current depth: how deep in the tree are we?
        self.current_depth = 0
        
        # Direction: True = forward, False = backward
        self.direction = True
    
    def _get_next_checkpoint_forward(self, current_pos: int) -> int:
        """
        Get the next checkpoint to add when moving forward from current_pos.
        
        Strategy: find the deepest checkpoint > current_pos
        """
        # Find all positions > current_pos
        all_positions = sorted(set(
            pos for d in self.tree.levels.values() for pos in d
        ))
        candidates = [p for p in all_positions if p > current_pos]
        
        if not candidates:
            return self.n
        
        return candidates[0]
    
    def next(self) -> bool:
        """
        Move forward: pos += 1, manage checkpoints.
        
        Strategy:
        - When moving into a new depth level, ADD that checkpoint
        - If memory full, REMOVE the oldest (lowest depth) checkpoint
        """
        if self.pos >= self.n:
            return False
        
        self.pos += 1
        self.ops += 1
        self.direction = True
        
        # Determine current depth based on position
        all_positions = sorted(set(
            pos for d in self.tree.levels.values() for pos in d
        ))
        positions_up_to_here = [p for p in all_positions if p <= self.pos]
        
        if len(positions_up_to_here) > len(self.checkpoints):
            # We've reached a new checkpoint position
            new_cp = positions_up_to_here[-1] if positions_up_to_here else self.pos
            
            if new_cp not in self.checkpoints:
                if len(self.checkpoints) < self.k:
                    self.checkpoints.append(new_cp)
                else:
                    # Memory full: deque automatically pops oldest (left)
                    self.checkpoints.append(new_cp)
        
        return True
    
    def prev(self) -> bool:
        """
        Move backward: apply inverse of forward checkpoint strategy.
        
        When we remove a checkpoint during backward, cost is: distance from
        removed checkpoint to next saved checkpoint.
        """
        if self.pos <= 0:
            return False
        
        self.direction = False
        
        # Before we move backward, check if we're about to leave a checkpoint depth
        all_positions = sorted(set(
            pos for d in self.tree.levels.values() for pos in d
        ))
        
        target = self.pos - 1
        positions_up_to_target = [p for p in all_positions if p <= target]
        
        # If we're losing checkpoints (going to shallower depth)
        if len(positions_up_to_target) < len(self.checkpoints):
            # Find which checkpoint we're about to drop
            removed_cp = self.checkpoints[-1]
            
            # Cost: recompute from next saved checkpoint to removed checkpoint
            # Actually: we just removed it, so cost is distance we need to traverse
            # The cost manifests when we later need it again
            
            # Remove it from memory (inverse of forward)
            if len(self.checkpoints) > 0:
                self.checkpoints.pop()
                
                # Cost: we had to traverse from removed_cp to where we are now
                # Since we're going backward, this is included in the backward steps
                cost_to_restore = removed_cp - target
                self.ops += cost_to_restore
        else:
            # Normal backward step
            cost = 1
            self.ops += cost
        
        self.pos = target
        return True
    
    def run_full_cycle(self):
        """Execute forward then backward."""
        while self.next():
            pass
        while self.pos > 0:
            self.prev()
    
    def get_metrics(self):
        n_logn = self.n * self.k
        return {
            'n': self.n,
            'k': self.k,
            'ops': self.ops,
            'n_logn': n_logn,
            'ratio': self.ops / n_logn if n_logn > 0 else 0,
            'checkpoints_in_mem': len(self.checkpoints),
        }


if __name__ == "__main__":
    print("=" * 90)
    print("HIERARCHICAL TREE WITH PROPER FORWARD/BACKWARD")
    print("=" * 90)
    print()
    
    for n in [16, 64, 256, 1024,4069]:
        enum = ProperLogNEnumerator(n)
        
        # Show structure
        print(f"\nn = {n}, k = {enum.k}")
        print(f"Positions: {sorted(set(pos for d in enum.tree.levels.values() for pos in d))[:20]}...")
        
        enum.run_full_cycle()
        m = enum.get_metrics()
        print(f"ops={m['ops']:8d}, n×k={m['n_logn']:6d}, ratio={m['ratio']:7.3f}")