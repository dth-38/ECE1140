# ------------------------------------------------------------------------------------------------------
#  Doubly linked list class(es) and functions
#  source: https://www.tutorialspoint.com/python_data_structure/python_advanced_linked_list.htm
# ------------------------------------------------------------------------------------------------------

# Create the node class
class Node:
    def __init__(self, data):
        # Standard node
        self.data = data
        self.name = str(data.get_section()) + str(data.get_number())
        self.next = None
        self.prev = None

        # Linked to more than 1 node
        self.next2 = None
        self.prev2 = None
        self.next3 = None
        self.prev3 = None

    def get_name(self):
        return self.name

    def get_block_number(self):
        return self.data.get_number()

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

    # Set other next values according to switch (or lackthereof)
    def set_other_links(self, node, switch_bool, switch):
        # Reverse direction
        node.next2 = node.prev
        node.prev2 = node.next

    # Print the Doubly Linked list		
    def tracklistprint(self, node):
        i = 0
        if node.prev is not None:
            print("node " + str(-1) + ":", end = " ")
            print(node.prev.get_name())

        while (node is not None):
            print("node " + str(i) + ":", end = " ")
            print(node.get_name())
            last = node
            node = node.next
            i += 1
