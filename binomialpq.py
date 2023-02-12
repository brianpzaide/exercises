from minpq import *
class BinomialTree:
    def __init__(self, order, other = None):
        self.order = order
        self.value = 0
        self.subtrees = []
        if other is not None:
            self.value = other.value
            for subtree in other.subtrees:
                self.subtrees.append(BinomialTree.deep_copy_tree(subtree))

    
    def add(self, other):
        if other.order == self.order:
            lowerValue, highervalue = (self,other) if self.value <= other.value else (other,self)
            c = BinomialTree(lowerValue.order+1, lowerValue)
            c.subtrees.append(BinomialTree.deep_copy_tree(highervalue))
            return c
        else:
            raise Exception("adding binomial trees of different orders not allowed")

    def deep_copy_tree(binomial_tree):
        new_tree = BinomialTree(binomial_tree.order)
        new_tree.value = binomial_tree.value
        for subtree in binomial_tree.subtrees:
            new_tree.subtrees.append(BinomialTree.deep_copy_tree(subtree))
        return new_tree
    
    def construct_subtree(current_order, minpq):
        if not minpq.isempty():
            new_tree = BinomialTree(current_order)
            new_tree.value =  minpq.delmin()

            for i in range(current_order):
                new_tree.subtrees.append(BinomialTree.construct_subtree(i, minpq))
            return new_tree
    
    def construct_via_minPQ(order, values):
        if len(values) != 2**order:
            raise Exception("in sufficient number of elements passed")
        
        pq = MinPQ(lambda a,b: a-b)
        for value in values:
            pq.insert(value)
        print(pq.pq)
        
        return BinomialTree.construct_subtree(order, pq)
        
    def print_binomial_tree(tree, spacings):
        print(spacings+"<order {} value {}>".format(tree.order, tree.value))
        for subtree in tree.subtrees:
            BinomialTree.print_binomial_tree(subtree, spacings+" ")
        print(spacings+"</order {} value {}>".format(tree.order, tree.value))

class BinomialHeap:
    def __init__(self, fixed_head = None, children=None, to_deep_copy=False):
        if children is None:
            self.fixed_head = fixed_head
        else:
            back_head_heapnode = None 
            front_head_heapnode = None
            initial = True
            sub_trees = []
            if to_deep_copy:
                for i in range(len(children)):
                    sub_trees.append(BinomialTree.deep_copy_tree(children[i]))
            else:
                sub_trees = children

            for subtree in sub_trees:
                if initial:
                    back_head_heapnode = {"tree":subtree, "prev":None, "next":None}
                    self.fixed_head = back_head_heapnode
                    initial = False
                    continue
                front_head_heapnode = {"tree": subtree, "prev":None, "next":None}
                front_head_heapnode["prev"] = back_head_heapnode
                back_head_heapnode["next"] = front_head_heapnode
                back_head_heapnode = front_head_heapnode
    
    def insert(minheap, x):
        new_tree = BinomialTree(0)
        new_tree.value = x
        new_node = {"tree":new_tree, "prev":None, "next":None}
        return BinomialHeap.merge(minheap, BinomialHeap(fixed_head=new_node))
    
    def peek_min(minheap):
        min = 2147483647
        head = minheap.fixed_head
        while(not head is None):
            k = head.get("tree").value
            if min >= k:
                min = k
            head = head.get("next")
        return min
    
    def extract_min(min_heap):
        min_value = BinomialHeap.peek_min(min_heap)
        head = min_heap.fixed_head
        while(True):
            if head.get("tree").value == min_value:
                break
            head = head.get("next")
        prev_node = head.get("prev")
        next_node = head.get("next")
        if not prev_node is None:
            prev_node["next"] = next_node
        else:
            min_heap.fixed_head = next_node
        if not next_node is None:
            next_node["prev"] = prev_node

        subtrees = head.get("tree").subtrees
        if len(subtrees) > 0:
            new_heap = BinomialHeap(children=subtrees)
            # print("from line 113 new_heap = ")
            # BinomialHeap.print_heap(new_heap)

            merged = new_heap if (prev_node is None) and (next_node is None) else BinomialHeap.merge(min_heap, new_heap)

            return min_value, merged
        else:
            # print("from line 123 new_heap = null")
            return min_value, min_heap
    
    def merge(min_heap1, min_heap2):

        n1 = min_heap1.fixed_head
        n2 = min_heap2.fixed_head

        f_carry_head, b_carry_head = None, None
        f_new_head, b_new_head = None, None

        carry_node = None
        new_node = None

        carry_initial = True
        new_initial = True
        new_heap = None
        carry_heap = None

        while((n1 is not None) and (n2 is not None)):
            if (n1.get("tree").order == n2.get("tree").order):
                carry_node = {"tree": n1.get("tree").add(n2.get("tree")), "next": None, "prev": None}
                if carry_initial:
                    carry_heap = BinomialHeap(fixed_head=carry_node)
                    f_carry_head = carry_node
                    b_carry_head = carry_node
                    carry_initial = False
                else:
                    f_carry_head = carry_node
                    f_carry_head["prev"] = b_carry_head
                    b_carry_head["next"] = f_carry_head
                    b_carry_head = f_carry_head
                
                n1 = n1.get("next")
                n2 = n2.get("next")
            
            elif (n1.get("tree").order < n2.get("tree").order):
                new_node = {"tree": BinomialTree.deep_copy_tree(n1.get("tree")), "next": None, "prev": None}
                if new_initial:
                    new_heap = BinomialHeap(fixed_head=new_node)
                    f_new_head = new_node
                    b_new_head = new_node
                    new_initial = False
                else:
                    f_new_head = new_node
                    f_new_head["prev"] = b_new_head
                    b_new_head["next"] = f_new_head
                    b_new_head = f_new_head
                
                n1 = n1.get("next")

            else:
                new_node = {"tree": BinomialTree.deep_copy_tree(n2.get("tree")), "next": None, "prev": None}
                if new_initial:
                    new_heap = BinomialHeap(fixed_head=new_node)
                    f_new_head = new_node
                    b_new_head = new_node
                    new_initial = False
                else:
                    f_new_head = new_node
                    f_new_head["prev"] = b_new_head
                    b_new_head["next"] = f_new_head
                    b_new_head = f_new_head
                
                n2 = n2.get("next")

        # drain heap2
        if n1 is None:
            while(n2 is not None):
                new_node = {"tree": BinomialTree.deep_copy_tree(n2.get("tree")), "next": None, "prev": None}
                if new_initial:
                    new_heap = BinomialHeap(fixed_head=new_node)
                    f_new_head = new_node
                    b_new_head = new_node
                    new_initial = False
                else:
                    f_new_head = new_node
                    f_new_head["prev"] = b_new_head
                    b_new_head["next"] = f_new_head
                    b_new_head = f_new_head
                
                n2 = n2.get("next")
        
        # drain heap1
        if n2 is None:
            while(n1 is not None):
                new_node = {"tree": BinomialTree.deep_copy_tree(n1.get("tree")), "next": None, "prev": None}
                if new_initial:
                    new_heap= BinomialHeap(fixed_head=new_node)
                    f_new_head = new_node
                    b_new_head = new_node
                    new_initial = False
                else:
                    f_new_head = new_node
                    f_new_head["prev"] = b_new_head
                    b_new_head["next"] = f_new_head
                    b_new_head = f_new_head
                
                n1 = n1.get("next")
        
        if (carry_heap is not None) and (new_heap is not None):
            return BinomialHeap.merge(new_heap, carry_heap)
        else:
            return new_heap if carry_heap is None else carry_heap

    def print_heap(min_heap):
        head = min_heap.fixed_head
        k = 0
        while(head is not None):
            print("level: {}".format(k))
            BinomialTree.print_binomial_tree(head.get("tree"), "")
            k += 1
            head = head.get("next")   

def main():
    # values = [i for i in range(8, 0, -1)]
    # tree = BinomialTree.construct_via_minPQ(3, values)
    # BinomialTree.print_binomial_tree(tree, "")

    values1 = [11,11,11,11,11,11,11,11,11,11]
    heap1 = BinomialHeap(fixed_head={"tree": BinomialTree.construct_via_minPQ(0, [11]), "next":None, "prev": None})

    for i in values1:
        heap1 = BinomialHeap.insert(heap1, i)
    # print("================heap1===================")
    # BinomialHeap.print_heap(heap1)

    values2 = [11,11,11,11,11,11]
    heap2 = BinomialHeap(fixed_head={"tree": BinomialTree.construct_via_minPQ(0, [11]), "next":None, "prev": None})

    for i in values2:
        heap2 = BinomialHeap.insert(heap2, i)
    # print("================heap2===================")
    # BinomialHeap.print_heap(heap2)

    #print("================(merge heap1, heap2)===================")
    merged_heap = BinomialHeap.merge(heap1, heap2)
    #BinomialHeap.print_heap(merged_heap)

    print("================(extract_min merged_heap)===================")
    i = 18
    while(i > 0):
        BinomialHeap.print_heap(merged_heap)
        min, merged_heap = BinomialHeap.extract_min(merged_heap)
        print("extracted_value: {}".format(min))
        print("----------------------------------------------------")
        i -= 1
    BinomialHeap.print_heap(merged_heap)

    print("adding new values...")
    for i in range(9, -1, -1):
        merged_heap = BinomialHeap.insert(merged_heap, i)
    BinomialHeap.print_heap(merged_heap)

    print("----------------------------------------------------")
    for i in range(9, 0, -1):
        min, merged_heap = BinomialHeap.extract_min(merged_heap)
        print("extracted min: {}".format(min))
        BinomialHeap.print_heap(merged_heap)
    BinomialHeap.print_heap(merged_heap)

if __name__=="__main__":
    main()