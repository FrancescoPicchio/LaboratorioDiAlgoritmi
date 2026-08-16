from math import inf
from timeit import default_timer as timer
import random
import matplotlib.pyplot as plt

# Heap


class Heap:
    def __init__(self, arr=None):
        self.heap = []
        if arr is None:
            return
        else:
            for x in arr:
                self.insert(x)

    def is_empty(self):
        return len(self.heap) == 0

    def heapify(self, i):
        n = len(self.heap)
        left = 2 * i
        right = (2 * i) + 1

        if left < n and self.heap[left] < self.heap[i]:
            max = left
        else:
            max = i
        if right < n and self.heap[right] < self.heap[i]:
            max = right

        if max != i:  # else the heap is already a max-heap
            swapped = self.heap[i]
            self.heap[i] = self.heap[max]
            self.heap[max] = swapped
            self.heapify(max)

    def insert(self, x):
        self.heap.append(-inf)
        self.increase_key(len(self.heap) - 1, x)

    def get_max(self):
        return self.heap[0]

    def remove_max(self):
        max = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.remove(-1)
        self.heapify(0)
        return max

    def increase_key(self, i, key):
        if key < self.heap[i]:
            print("error: new key is smaller than the older one")
            return
        self.heap[i] = key
        while i > 0 and self.heap[i // 2] < self.heap[i]:
            swapped = self.heap[i // 2]
            self.heap[i // 2] = self.heap[i]
            self.heap[i] = swapped
            i = i // 2

    def print(self):
        print(self.heap)


# base Node, used by both type of lists


class Node:
    def __init__(self, data, head, next=None):
        self.head = head
        self.next = next
        self.data = data


# Unordered Linked List


class LinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def find_set(self):
        return self.head

    # FIXME maybe this method isn't necessary
    def union(self, list):
        if not isinstance(list, LinkedList):
            print(
                "error: tried to make a union with something that isn't a linked list"
            )
            return
        other_head = list.find_set()
        self.tail.next = other_head
        self.tail = list.tail

    # x is supposed to be data, not a Node
    def insert(self, x):
        new_node = Node(x, self, None)
        if self.head is not None:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node

    def get_max(self):
        if self.head is None:
            print("error: list has no elements")
            return
        node = self.head
        current_max = node
        while node is not None:
            if current_max.data < node.data:
                current_max = node
            node = node.next
        return current_max

    def remove_max(self):
        if self.head is None:
            print("error: no elements in list")
            return
        node = self.head
        current_max_value = node.data
        current_max_node = node
        node_before_max = self.head
        previous = None

        while node is not None:
            if current_max_value < node.data:
                current_max_value = node.data
                current_max_node = node
                node_before_max = previous
            previous = node
            node = node.next

        if current_max_node.next is None:
            self.tail = node_before_max
        if node_before_max is not None:
            node_before_max.next = current_max_node.next
        else:
            self.head = current_max_node.next

        return current_max_node

    def increase_key(self, x, key):
        if x > key:
            print("error: new key is lower than current value")
            return
        node = self.head
        while node is not None:
            if node.data == x:
                node.data = key
                return
            node = node.next
        print("error: couldn't find node with value " + x)

    def print(self):
        node = self.head
        if node is None:
            print("list is empty")
            return
        result = str(node.data)
        while node is not None:
            result += "-> " + str(node.data)
            node = node.next
        print(result + " end of list")


# Ordered Linked List


class OrderedLinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    # x is supposed to be data, not a Node
    def insert(self, x):
        if self.head is None:
            new_node = Node(x, self, None)
            self.head = new_node
            self.tail = new_node
            return

        node = self.head
        previous = None
        while node is not None:
            if x >= node.data:
                new_node = Node(x, self, node)
                if previous is not None:
                    previous.next = new_node
                else:
                    self.head = new_node
                    self.tail = node
                return
            else:
                previous = node
                node = node.next

    def get_max(self):
        return self.head

    def remove_max(self):
        if self.head is None:
            print("error: list has no elements")
            return
        max = self.head
        self.head = self.head.next
        return max

    def increase_key(self, x, key):
        if x > key:
            print("error: new key is smaller than older one")
            return
        node = self.head
        while node is not None:
            if node.data == x:
                node.data = key
                return
            node = node.next
        print("error: couldn't find node with value " + x)

    def print(self):
        node = self.head
        if node is None:
            print("list is empty")
            return
        result = ""
        while node is not None:
            result += str(node.data)
            node = node.next
            if node is not None:
                result += "-> "
        print(result + " end of list")


number_of_elements = 1000
time_per_operation = []
number_of_operation = range(number_of_elements)

interval_start = 1
interval_end = 300
test = random.choices(range(interval_start, interval_end), k=number_of_elements)
max_heap = Heap(test)
start = timer()
for e in test:
    max_heap.insert(e)
    end = timer()
    time_per_operation.append(end - start)

plt.plot(number_of_operation, time_per_operation, "r", label="Heap")
plt.title("Insertion Performance")
plt.xlabel("# insertion")
plt.ylabel("time")

unordered_list = LinkedList()
time_per_operation = []
start = timer()
for e in test:
    unordered_list.insert(e)
    end = timer()
    time_per_operation.append(end - start)
plt.plot(number_of_operation, time_per_operation, "b", label="UnorderedLinkedList")

ordered_list = OrderedLinkedList()
time_per_operation = []
start = timer()
for e in test:
    ordered_list.insert(e)
    end = timer()
    time_per_operation.append(end - start)
plt.plot(number_of_operation, time_per_operation, "g", label="OrderedLinkedList")

plt.legend(loc="upper left")
plt.savefig("max_heap.png")
