use std::cell::RefCell;
use std::rc::Rc;

type NodeRef = Option<Rc<RefCell<Node>>>;

struct Node {
    val: i32,
    prev: NodeRef,
    next: NodeRef,
    child: NodeRef,
}

impl Node {
    fn new(val: i32) -> NodeRef {
        Some(Rc::new(RefCell::new(
            Node { val, prev: None, next: None, child: None }
        )))
    } 
}

fn flatten(head: NodeRef) -> NodeRef {
    let mut runner = head.clone();
    let mut stack = Vec::new();

    while let Some(current) = runner.clone() {
        let mut current_borrow = current.borrow_mut();

        // if child exists, flatten it
        if let Some(child) = current_borrow.child.take() {
            // push the next node to the stack, to process it later once the it is done processing the child
            if let Some(next) = current_borrow.next.take() {
                stack.push(next);
            }

            // create links between the child node and the current node as next and prev respectively
            current_borrow.next = Some(child.clone());
            child.borrow_mut().prev = Some(current.clone());
        }

        // if no next node(at this point done processing the child node), next take from the stack(thus maintaining order)
        if current_borrow.next.is_none() && !stack.is_empty() {
            if let Some(next) = stack.pop() {
                current_borrow.next = Some(next.clone());
                next.borrow_mut().prev = Some(current.clone());
            }
        }

        // move to the next node
        runner = current_borrow.next.clone();
    }

    head
}


fn main(){
    let node1 = Node::new(1);
    let node2 = Node::new(2);
    let node3 = Node::new(3);
    let node4 = Node::new(4);
    let node5 = Node::new(5);
    let node6 = Node::new(6);
    let node7 = Node::new(7);
    let node8 = Node::new(8);
    let node9 = Node::new(9);
    let node10 = Node::new(10);
    let node11 = Node::new(11);
    let node12 = Node::new(12);


    if let Some(node1_ref) = node1.clone() {
        node1_ref.borrow_mut().next = node2.clone();
    }
    if let Some(node2_ref) = node2.clone() {
        node2_ref.borrow_mut().prev = node1.clone();
        node2_ref.borrow_mut().next = node3.clone();
    }
    if let Some(node3_ref) = node3.clone() {
        node3_ref.borrow_mut().prev = node2.clone();
        node3_ref.borrow_mut().next = node4.clone();
        node3_ref.borrow_mut().child = node7.clone();
    }
    if let Some(node4_ref) = node4.clone() {
        node4_ref.borrow_mut().prev = node3.clone();
        node4_ref.borrow_mut().next = node5.clone();
    }
    if let Some(node5_ref) = node5.clone() {
        node5_ref.borrow_mut().prev = node4.clone();
        node5_ref.borrow_mut().next = node6.clone();
    }
    if let Some(node6_ref) = node6.clone() {
        node6_ref.borrow_mut().prev = node5.clone();
    }
    if let Some(node7_ref) = node7.clone() {
        node7_ref.borrow_mut().next = node8.clone();
    }
    if let Some(node8_ref) = node8.clone() {
        node8_ref.borrow_mut().prev = node7.clone();
        node8_ref.borrow_mut().next = node9.clone();
        node8_ref.borrow_mut().child = node11.clone();
    }
    if let Some(node9_ref) = node9.clone() {
        node9_ref.borrow_mut().prev = node8.clone();
        node9_ref.borrow_mut().next = node10.clone();
    }
    if let Some(node10_ref) = node10.clone() {
        node10_ref.borrow_mut().prev = node9.clone();
    }
    if let Some(node11_ref) = node11.clone() {
        node11_ref.borrow_mut().next = node12.clone();
    }
    if let Some(node12_ref) = node12.clone() {
        node12_ref.borrow_mut().prev = node11.clone();
    }

    let flattened = flatten(node1);
    let mut runner = flattened;

    while let Some(current) = runner.clone(){
        print!("{} -> ", current.borrow().val);
        runner = current.borrow().next.clone();
    }
    println!("None")
}