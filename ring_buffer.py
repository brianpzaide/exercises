import unittest


class RingBuffer:
    def __init__(self):
        self.n = 1
        self.arr = [None]*1
        self.rpointer, self.wpointer = 0, 0
        self.is_full = False
    
    def insert(self, k):
        if self.is_full:
            self.resize()
        
        self.arr[self.wpointer] = k
        self.wpointer = (self.wpointer + 1)%self.n

        if self.wpointer == self.rpointer:
            self.is_full = True
    
    def pop(self):
        if (not self.is_full) and self.rpointer == self.wpointer:
            raise RuntimeError("the buffer is empty")
        
        val = self.arr[self.rpointer]
        self.rpointer = (self.rpointer + 1)%self.n
        self.is_full = False
        
        num_elements = (self.wpointer - self.rpointer + self.n) % self.n
        if self.n > 1 and num_elements < self.n //2:
            self.resize(to_increase=False)
        
        return val
    
    def size(self):
        if self.is_full:
            return self.n
        return (self.wpointer - self.rpointer + self.n) % self.n
    
    def resize(self, to_increase = True):
        old_n = self.n
        new_n = old_n * 2 if to_increase else max(1, old_n // 2)
        num_elements =  self.size()
        new_arr = [None] * new_n

        for i in range(num_elements):
            new_arr[i] = self.arr[(self.rpointer + i) % old_n]

        self.arr = new_arr
        self.n = new_n
        self.rpointer = 0
        self.wpointer = num_elements
        self.is_full = False

class TestRingBuffer(unittest.TestCase):
    def test_insert_pop(self):
        rb = RingBuffer()
        rb.insert(1)
        rb.insert(2)
        self.assertEqual(rb.pop(), 1)
        rb.insert(3)
        self.assertEqual(rb.pop(), 2)

    def test_doubling_buffer_size(self):
        rb = RingBuffer()
        rb.insert(1)
        rb.insert(2)
        self.assertEqual(rb.n, 2)
        rb.insert(3)
        self.assertEqual(rb.n, 4)
    
    def test_halving_buffer_size(self):
        rb = RingBuffer()
        for i in range(5):
            rb.insert(i)
        rb.pop()
        rb.pop()
        self.assertEqual(rb.n, 4)

    def test_empty_buffer(self):
        rb = RingBuffer()
        with self.assertRaises(RuntimeError):
            rb.pop()

def main():
    rb = RingBuffer()
    # rb.insert(1)
    # print(rb.arr)
    # rb.insert(2)
    # print(rb.arr)
    # rb.insert(3)
    # print(rb.arr)
    # rb.insert(4)
    # print(rb.arr)
    rb.insert(1)
    print(rb.arr, rb.n)
    rb.insert(2)
    print(rb.arr, rb.n)
    print(rb.pop())
    print(rb.arr, rb.n)
    rb.insert(3)
    print(rb.arr, rb.n)
    print(rb.pop())
    print(rb.arr, rb.n)

if __name__ == '__main__':
    unittest.main()
    # main()