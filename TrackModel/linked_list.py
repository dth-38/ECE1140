# ------------------------------------------------------------------------------------------------------
#  Doubly linked list class(es) and functions
#  source: https://www.tutorialspoint.com/python_data_structure/python_advanced_linked_list.htm
# ------------------------------------------------------------------------------------------------------

# Create the node class
class Node:
    def __init__(self, data):
        # Standard node
        self.data = data
        self.next = None
        self.prev = None

        # Linked to more than 1 node
        self.next2 = None
        self.prev2 = None

# Create the doubly linked list class
class doubly_linked_list:
    def __init__(self):
        self.head = None

    # Define the push method to add elements at the begining
    def push(self, NewVal):
        NewNode = Node(NewVal)
        NewNode.next = self.head
        if self.head is not None:
            self.head.prev = NewNode
        self.head = NewNode

    # Define the insert method to insert the element		
    def insert(self, prev_node, NewVal):
        if prev_node is None:
            return
        NewNode = Node(NewVal)
        NewNode.next = prev_node.next
        prev_node.next = NewNode
        NewNode.prev = prev_node
        if NewNode.next is not None:
            NewNode.next.prev = NewNode

    # Define the append method to add elements at the end
    def append(self, NewVal):
        NewNode = Node(NewVal)
        NewNode.next = None
        if self.head is None:
            NewNode.prev = None
            self.head = NewNode
            return
        last = self.head
        while (last.next is not None):
            last = last.next
        last.next = NewNode
        NewNode.prev = last
        return
