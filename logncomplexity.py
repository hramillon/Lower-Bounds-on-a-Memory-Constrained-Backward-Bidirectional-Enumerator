import math

class LogNEnumerator:
    
    def __init__(self, n: int):
        self.n = n
        
        self.pos = 0
        self.ops = 0
        
        #next indice to remove in forward pass
        self.next_rmv= 1
        #smaller gap between two checkpoints
        self.smaller_size= 2
        #distance between last checkpoint and position
        self.marginal_dist=0
        
        # Current checkpoints in memory
        self.check=0
        self.checkpoints = [0]
        
        # Direction: True = forward, False = backward
        self.direction = True
    
    def computer_rmv(self):
        self.checkpoints.pop(self.next_rmv)
        
        if(self.next_rmv == self.check):
            return (1,self.checkpoints[1] -self.checkpoints[0])
        elif(self.next_rmv == self.check -1):
            return(self.check, self.checkpoints[self.next_rmv] -self.checkpoints[self.next_rmv-1])
        elif(self.checkpoints[self.next_rmv] -self.checkpoints[self.next_rmv-1] == self.checkpoints[self.next_rmv +1] -self.checkpoints[self.next_rmv]):
            return (self.next_rmv,self.checkpoints[self.next_rmv] -self.checkpoints[self.next_rmv-1])
        return (self.next_rmv+1,self.checkpoints[self.next_rmv+1] -self.checkpoints[self.next_rmv])
    
    def next(self) -> bool:
        self.pos+=1
        self.ops+=1
        self.marginal_dist+=1
        if ((self.pos & (self.pos - 1)) == 0 and self.pos != 1):
            self.checkpoints.append(self.pos)
            self.check+=1
            self.marginal_dist=0
        if self.marginal_dist >= self.smaller_size:
            (self.next_rmv,self.smaller_size) = self.computer_rmv()
            self.checkpoints.append(self.pos)
            self.marginal_dist=0
        if(self.pos < self.n):
            return True
        return False
    
    def compute_checks(self):
        #we check if there is a room for a checpoint between intervals
        free_room_start = len(self.checkpoints)-2
        free_room_end =len(self.checkpoints)-1
        
        index_replace = free_room_end
        while(free_room_end != 0):
            if(self.checkpoints[free_room_end] - self.checkpoints[free_room_start] > 1):
                self.checkpoints.insert(index_replace,self.checkpoints[free_room_start] + ((self.checkpoints[free_room_end] - self.checkpoints[free_room_start])//2))
                self.ops+= ((self.checkpoints[free_room_end] - self.checkpoints[free_room_start])//2)
                break
            else:
                free_room_start-=1
                free_room_end-=1
                index_replace-=1
        #If there is no more place we remove the unnecessaries checkpoints
        self.check-=1
        
    
    def prev(self) -> bool:
        if(self.pos == self.checkpoints[-1]):
            self.compute_checks()
            self.checkpoints.pop()
            self.pos-=1
        else:
            self.pos-=1
            self.ops+= (self.pos - self.checkpoints[-1])
        return True
                
    
    def run_full_cycle(self):
        
        while self.next():
            pass
        while self.pos > 0:
            self.prev()
        self.ops -= math.ceil(math.log2(self.n))
    
    def get_metrics(self):
        n_logn = math.ceil(self.n * math.log2(self.n))
        return {
            'n': self.n,
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
    
    for n in [128,256,1024,2048]:
        enum = LogNEnumerator(n)
        
        enum.run_full_cycle()
        m = enum.get_metrics()
        print(f"ops={m['ops']:8d}, n×log(n)={m['n_logn']:6d}, ratio={m['ratio']:7.3f}")