class MinPQ:
    def __init__(self, comparator):
        self.pq = []
        self.comparator = comparator
    
    def isempty(self):
        return len(self.pq) == 0

    def size(self):
        return len(self.pq)

    def min(self):
        if len(self.pq) == 0:
            raise Exception("Priority queue underflow")
        else:
            return self.pq[0]
    
    def insert(self, x):
        (self.pq).append(x)
        self.swim(len(self.pq)-1)
        # print("inserting {} ".format(x), self.pq)
        assert self.isMinHeap()
    
    def delmin(self):
        n = len(self.pq) 
        if n == 0:
            raise Exception("Priority queue underflow")
        x = self.pq[0]
        self.pq[0], self.pq[n-1] = self.pq[n-1], self.pq[0]
        self.pq = self.pq[:n-1]
        self.sink(0)
        assert self.isMinHeap()
        return x
    
    def swim(self, k):
        pq = self.pq
        while k > 0 and self.greater((k-1)//2, k):
            pq[(k-1)//2], pq[k] = pq[k], pq[(k-1)//2]
            k = (k-1)//2

    def sink(self, k):
        pq = self.pq
        n = len(pq)
        while k < (n-1)//2 and (self.greater(k, 2*k+1) or self.greater(k, 2*k+2)):
            m = 2*k+2 if self.greater(2*k+1, 2*k+2) else 2*k+1
            pq[k], pq[m] = pq[m], pq[k]
            k = m

    def isMinHeap(self):
        n = len(self.pq)
        for i in range(n):
            if self.pq[i] is None: return False
        
        return self.isMinHeapOrdered(0)
    
    def isMinHeapOrdered(self, k):
        # print(k, len(self.pq))
        if k >= (len(self.pq)-1)//2:
            return True
        left = 2*k + 1
        right = 2*k + 2
        if self.greater(k, left): return False
        if self.greater(k, right): return False
        return self.isMinHeapOrdered(left) and self.isMinHeapOrdered(right)

    def greater(self, a, b):
        pq = self.pq
        return self.comparator(pq[a], pq[b]) > 0