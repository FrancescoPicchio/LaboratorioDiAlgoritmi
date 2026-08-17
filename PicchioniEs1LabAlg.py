from math import inf
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import random

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
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left < n and self.heap[left] > self.heap[largest]:
            largest = left
        if right < n and self.heap[right] > self.heap[largest]:
            largest = right
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.heapify(largest)

    def insert(self, x):
        self.heap.append(-inf)
        self.increase_key(len(self.heap) - 1, x)

    def remove(self, x):
        i = 0  # root node
        while i < len(self.heap) and self.heap[i] != x:
            i += 1
        if i == len(self.heap):
            print("couldn't find match")
            return
        if self.heap[i] == self.heap[-1]:
            self.heap.pop(-1)
            return
        self.heap[i] = self.heap[-1]
        self.heap.pop(-1)
        self.heapify(i)

    def get_max(self):
        return self.heap[0]

    def remove_max(self):
        max = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop(-1)
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

    # works on the index of the element, not the value
    def is_leaf(self, i):
        return i > (len(self.heap) // 2) and i <= len(self.heap)

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

    def remove(self, x):
        if self.head is None:
            print("error: list contains no elements")
        node = self.head
        previous = None
        while node is not None:
            if node.data == x:
                if previous is None:
                    self.head = node.next
                else:
                    previous.next = node.next
                    if self.tail == node:
                        self.tail = previous
                return
            else:
                previous = node
                node = node.next
        print("error: no matching item to remove was found")

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
        result = ""
        while node is not None:
            result += str(node.data)
            node = node.next
            if node is not None:
                result += " -> "
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

    def remove(self, x):
        if self.head is None:
            print("error: list contains no elements")
        node = self.head
        previous = None
        while node is not None:
            if node.data == x:
                if previous is None:
                    self.head = node.next
                else:
                    previous.next = node.next
                    if self.tail == node:
                        self.tail = previous
                return
            else:
                previous = node
                node = node.next
        print("error: no matching item to remove was found")

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
                result += " -> "
        print(result + " end of list")


def measure_insert_time(data, elements, output):
    start = timer()
    for e in elements:
        data.insert(e)
        end = timer()
        output.append(end - start)


def measure_get_max(data, n, output):
    start = timer()
    # _ so linters and such know that the index isn't important
    for _ in range(n):
        data.remove_max()
        end = timer()
        output.append(end - start)


number_of_elements = 1000
number_of_operation = range(number_of_elements)
interval_start = 1
interval_end = 300
inputs = random.choices(range(interval_start, interval_end), k=number_of_elements)
plt.subplot(2, 1, 1)

time_per_operation = []
max_heap = Heap()
measure_insert_time(max_heap, inputs, time_per_operation)
plt.plot(number_of_operation, time_per_operation, "r", label="Heap")

time_per_operation = []
unordered_list = LinkedList()
measure_insert_time(unordered_list, inputs, time_per_operation)
plt.plot(number_of_operation, time_per_operation, "b", label="UnorderedLinkedList")

time_per_operation = []
ordered_list = OrderedLinkedList()
measure_insert_time(ordered_list, inputs, time_per_operation)
plt.plot(number_of_operation, time_per_operation, "g", label="OrderedLinkedList")


plt.xlabel("# insertion")
plt.ylabel("time")
plt.legend(loc="upper left")


plt.subplot(2, 1, 2)
time_per_operation = []
max_heap = Heap(inputs)
measure_get_max(max_heap, number_of_elements, time_per_operation)
plt.plot(number_of_operation, time_per_operation, "r", label="Heap")

plt.xlabel("# removal")
plt.ylabel("time")

plt.savefig("max_heap.png")
