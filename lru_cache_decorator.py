from hashlib import blake2b
from functools import wraps
import time
import pickle


class LinkList:
    def __init__(self, res = None, hashed_key = None, left = None, right = None):
        self.res = res
        self.hashed_key = hashed_key
        self.left = left
        self.right = right

def my_lru_cache(max_size=128):
    def decorator(func):
        cache = {}
        head = LinkList()
        tail = head
        n = 0
            

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal head, tail, n
            hashed_key = blake2b(pickle.dumps((args, kwargs))).hexdigest()
            node = cache.get(hashed_key, None)
            if node:
                # detaching the node from the linked list
                res = node.res
                if node.left is not None:
                    node.left.right = node.right
                if node.right is not None:
                    node.right.left = node.left
                node.left = None
                node.right = None
                
                # attaching the node to the head of the linked list
                node.left = head
                head.right = node
                head = node
                return res
            else:
                res = func(*args, **kwargs)
                node = LinkList(res=res, hashed_key=hashed_key)
                cache[hashed_key] = node
                if n == 0:
                    head = node
                    tail = node
                else:
                    # attaching the node to the head of the linked list
                    node.left = head
                    head.right = node
                    head = node
                n += 1
                if n > max_size:
                    del cache[tail.hashed_key]
                    tail = tail.right
                    if tail:
                        tail.left = None
                    n -= 1
                return res
        return wrapper
    return decorator

@my_lru_cache(5)
def sleeping_function(a, b, c, d = 1, e=2):
    time.sleep(1)
    print(f"{a**1}, {b**2}, {c**3}, {d**4}, {e**5}")


if __name__ == '__main__':
    for i in range(10):
        sleeping_function(i,i,i,d=i,e=i)
    
    # expectation: should not even result in the function call that is no print statements on stdout 
    for i in range(5, 10):
        sleeping_function(i,i,i,d=i,e=i)