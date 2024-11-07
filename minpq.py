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
            raise Exception("priority queue is empty")
        else:
            return self.pq[0]
    
    def insert(self, x):
        (self.pq).append(x)
        self.rise(len(self.pq)-1)
    
    def delmin(self):
        n = len(self.pq) 
        if n == 0:
            raise Exception("priority queue is empty")
        x = self.pq[0]
        self.pq[0], self.pq[n-1] = self.pq[n-1], self.pq[0]
        self.pq = self.pq[:n-1]
        self.sink(0)
        return x
    
    def rise(self, k):
        pq = self.pq
        parent = (k-1)//2
        while k > 0 and self.greater(parent, k):
            pq[parent], pq[k] = pq[k], pq[parent]
            k = parent

    def sink(self, k):
        pq = self.pq
        n = len(pq)
        while 2*k+1 < n:
            left = 2*k+1
            right = 2*k+2
            smallest = left
            if right < n and self.greater(left, right):
                smallest = right
            if self.greater(smallest, k):
                break
            pq[k], pq[smallest] = pq[smallest], pq[k]
            k = smallest 

    def greater(self, a, b):
        pq = self.pq
        return self.comparator(pq[a], pq[b]) > 0