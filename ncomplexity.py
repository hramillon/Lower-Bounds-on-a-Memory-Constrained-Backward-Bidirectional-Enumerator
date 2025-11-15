
    
class NElementBiDiWrapper:
    
    def __init__(self, start_iterator, n):
        self.n = n
        self.current = start_iterator
        # Stack des positions sauvegardées (LIFO)
        self.saved_positions = []
        self.distance = 0 
    
    def next(self):
        self.distance += 1
        self.saved_positions.append(self.current.clone())
        
        self.current.next()
    
    def prev(self):
        if len(self.saved_positions) == 0:
            raise ValueError("Cannot move backward: no saved positions")
        
        # Libérer la position actuelle
        self.distance -= 1
        self.saved_positions.pop()
        # Récupérer la dernière position sauvegardée (LIFO)
        self.current.prev()
    
    def can_prev(self):
        return len(self.saved_positions) > 0
    
    @classmethod
    def get_count(cls):
        return cls.operation_count


# Test with operation counting
class CountingIterator:
    operation_count = 0
    
    def __init__(self, pos=0):
        self.pos = pos
    
    def clone(self):
        return CountingIterator(self.pos)
    
    def next(self):
        CountingIterator.operation_count += 1
        self.pos += 1
        
    def prev(self):
        CountingIterator.operation_count += 1
        self.pos += 1
    
    def free(self):
        pass
    
    @classmethod
    def reset_count(cls):
        cls.operation_count = 0
    
    @classmethod
    def get_count(cls):
        return cls.operation_count


def test_correctness():
    """Test that positions are correct"""
    print("=== CORRECTNESS TEST ===")
    for n in [100, 200, 300]:
        print(f"\nTesting n={n}")
        wrapper = NElementBiDiWrapper(CountingIterator(0), n)
        
        # Go forward
        for i in range(n):
            wrapper.next()
        
        # Check correctness
        expected_pos = n
        actual_pos = wrapper.current.pos
        distance = wrapper.distance
        
        print(f"After {n} forward steps:")
        print(f"  distance={distance}, current.pos={actual_pos}, expected={expected_pos}")
        print(f"  Correct: {distance == expected_pos == actual_pos}")
        
        # Go backward and check each step
        correct_steps = 0
        for i in range(n):
            wrapper.prev()
            expected_pos -= 1
            if wrapper.distance == expected_pos == wrapper.current.pos:
                correct_steps += 1
        position = wrapper.distance
        
        print(f"After {n} backward steps: {correct_steps}/{n} positions correct we are at the position {position}")

def test_complexity():
    """Test actual complexity by counting operations"""
    print("\n=== COMPLEXITY TEST ===")
    
    test_distances = [100, 400, 900, 1600]
    
    for n in test_distances:
        print(f"\nTesting n={n} (expected O({n}))")
        print("Distance\tOps\tTheoretical\tRatio")
        
        wrapper = NElementBiDiWrapper(CountingIterator(0), n)
        
        for j in range(n):
            wrapper.next()
        CountingIterator.reset_count()
            
        for j in range(n):
            wrapper.prev()
        ops = CountingIterator.get_count()
            
        # Theoretical complexity: O(n)
        theoretical = n
        ratio = ops / theoretical if theoretical > 0 else 0
            
        print(f"{n}\t{ops}\t{theoretical:.1f}\t\t{ratio:.3f}")

def comprehensive_test():
    """Run all tests"""
    test_correctness()
    test_complexity()
    

if __name__ == "__main__":
    comprehensive_test()

