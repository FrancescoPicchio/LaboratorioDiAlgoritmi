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
        if i >= len(self.heap):
            print("index out of range")
            return
        if key < self.heap[i]:
            # print("error: new key is smaller than the older one")
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

    def get_len(self):
        return len(self.heap)

    def get_value(self, i):
        if i > len(self.heap):
            return
        else:
            return self.heap[i]


# base Node, used by both type of lists


class Node:
    def __init__(self, data, list, next=None):
        self.list = list
        self.next = next
        self.data = data

    def get_list(self):
        return self.list

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_list(self, new_list):
        self.list = new_list

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next


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
        if self.tail is None:
            self.tail = list.tail
        else:
            self.tail.set_next(other_head)
            self.tail = list.tail

    # x is supposed to be data, not a Node
    def insert(self, x):
        new_node = Node(x, self, None)
        if self.head is None:
            self.head = new_node
        else:
            self.tail.set_next(new_node)
        self.tail = new_node

    def remove(self, x):
        if self.head is None:
            print("error: list contains no elements")
        node = self.head
        previous = None
        while node is not None:
            if node.get_data() == x:
                if previous is None:
                    self.head = node.get_next()
                else:
                    previous.set_next(node.get_next())
                    if self.tail == node:
                        self.tail = previous
                return
            else:
                previous = node
                node = node.get_next()
        print("error: no matching item to remove was found")

    def get_max(self):
        if self.head is None:
            print("error: list has no elements")
            return
        node = self.head
        current_max = node
        while node is not None:
            if current_max.get_data() < node.get_data():
                current_max = node
            node = node.get_next
        return current_max

    def remove_max(self):
        if self.head is None:
            print("error: no elements in list")
            return
        node = self.head
        current_max_value = node.get_data()
        current_max_node = node
        node_before_max = self.head
        previous = None

        while node is not None:
            if current_max_value < node.get_data():
                current_max_value = node.get_data()
                current_max_node = node
                node_before_max = previous
            previous = node
            node = node.get_next()

        if current_max_node.get_next() is None:
            self.tail = node_before_max
        if node_before_max is not None:
            node_before_max.set_next(current_max_node.get_next())
        else:
            self.head = current_max_node.get_next()

        return current_max_node

    def increase_key(self, i, key):
        node = self.head
        if node is None:
            print("list is empty")
            return
        for _ in range(i):
            if node.next is None:
                print("index out of range")
                return
            node = node.next
        if node.data > key:
            # print("new key is smaller than older key")
            return
        node.data = key

    def get_len(self):
        node = self.head
        i = 0
        while node is not None:
            i += 1
            node = node.get_next()
        return i

    def get_value(self, i):
        if self.head is None:
            return
        node = self.head
        for _ in range(i):
            if node.get_next() is None:
                return
            node = node.get_next()
        return node.get_data()

    def print(self):
        node = self.head
        if node is None:
            print("list is empty")
            return
        result = ""
        while node is not None:
            result += str(node.get_data())
            node = node.get_next()
            if node is not None:
                result += " -> "
        print(result + " end of list")


# Ordered Linked List


class OrderedLinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def is_empty(self):
        return self.head == None

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
            if x >= node.get_data():
                new_node = Node(x, self, node)
                if previous is not None:
                    previous.set_next(new_node)
                else:
                    self.head = new_node
                    self.tail = node
                return
            else:
                previous = node
                if node.get_next() is None:
                    new_node = Node(x, self, None)
                    node.set_next(new_node)
                    return
                else:
                    node = node.next
        print("error: no matching item to remove was found")

    def remove(self, x):
        if self.head is None:
            print("error: list contains no elements")
            return
        node = self.head
        previous = None
        while node is not None:
            if node.get_data() == x:
                if previous is None:
                    self.head = node.get_next()
                else:
                    previous.set_next(node.get_next())
                    if self.tail == node:
                        self.tail = previous
                return
            else:
                previous = node
                node = node.get_next()
        print("error: no matching item to remove was found")

    def get_max(self):
        return self.head

    def remove_max(self):
        if self.head is None:
            # print("error: list has no elements")
            return
        max = self.head
        self.head = self.head.get_next()
        return max

    def increase_key(self, i, key):
        node = self.head
        if node is None:
            print("list is empty")
            return
        for _ in range(i):
            if node.get_next() is None:
                print("index out of range")
                return
            node = node.get_next()
        if node.get_data() > key:
            # print("new key is smaller than older key")
            return
        self.remove(node.get_data())
        self.insert(key)

    def get_len(self):
        node = self.head
        i = 0
        while node is not None:
            i += 1
            node = node.get_next()
        return i

    def get_value(self, i):
        if self.head is None:
            return
        node = self.head
        for _ in range(i):
            if node.get_next() is None:
                return
            node = node.get_next()
        return node.get_data()

    def print(self):
        node = self.head
        if node is None:
            print("list is empty")
            return
        result = ""
        while node is not None:
            result += str(node.get_data())
            node = node.get_next()
            if node is not None:
                result += " -> "
        print(result)


def measure_insert_time(data, step, elements, output, repeats, random_test, test_value):
    for i in range(0, len(elements), step):
        best = inf
        for _ in range(repeats):
            test = data()
            for e in elements[:i]:
                test.insert(e)
            if random_test is True:
                random_value = random.choice(range(test_value))
            else:
                random_value = test_value
            start = timer()
            test.insert(random_value)
            end = timer()
            best = min(best, end - start)
        if i % 100 == 0:
            print(i)
        output.append(best)


def insert_test(test_type):
    number_of_elements = 3000
    step = 100
    number_of_operation = range(0, number_of_elements, step)
    interval_end = 3000
    number_of_repeats = 10
    inputs = random.choices(range(interval_end), k=number_of_elements)

    # Testing insertion of random value
    test_value = interval_end
    random_test = True
    test_type_string = "random"
    # Testing insertion of highest value
    if test_type == 1:
        random_test = False
        test_type_string = "highest"
        print("testing insertion of highest value")
    # Testing insertion of lowest value
    elif test_type == 2:
        random_test = False
        test_value = 1
        test_type_string = "lowest"
        print("testing insertion of lowest value")
    else:
        print("testing insertion of a random value")

    time = []
    print("testing Heap")
    measure_insert_time(
        Heap, step, inputs, time, number_of_repeats, random_test, test_value
    )
    plt.plot(number_of_operation, time, "r", label="Heap")
    print("finished testing Heap")

    time = []
    print("testing OrderedLinkedList")
    measure_insert_time(
        OrderedLinkedList,
        step,
        inputs,
        time,
        number_of_repeats,
        random_test,
        test_value,
    )
    plt.plot(number_of_operation, time, "g", label="OrderedLinkedList")
    print("finished testing OrderedLinkedList")

    time = []
    print("testing LinkedList")
    measure_insert_time(
        LinkedList, step, inputs, time, number_of_repeats, random_test, test_value
    )
    plt.plot(number_of_operation, time, "b", label="UnorderedLinkedList")
    print("finished testing LinkedList")
    plt.title("Insertion Performance, " + test_type_string + " value")
    plt.xlabel("Size")
    plt.ylabel("time")
    plt.legend(loc="upper left")
    plt.savefig("insertion_performance_" + test_type_string + ".png")
    # clears previous graph
    plt.clf()


print("Testing Insertion cases")
for i in range(3):
    insert_test(i)


# Generating random inputs


# # Section for insert()
# time = []
# print("heap before")
# measure_insert_time(Heap, step, inputs, time, number_of_repeats, interval_end)
# plt.plot(number_of_operation, time, "r", label="Heap")
# print("heap after")
#
# time = []
# print("ord list before")
# measure_insert_time(
#     OrderedLinkedList, step, inputs, time, number_of_repeats, interval_end
# )
# plt.plot(number_of_operation, time, "g", label="OrderedLinkedList")
# print("ord list after")
#
# time = []
# print("linked list before")
# measure_insert_time(LinkedList, step, inputs, time, number_of_repeats, interval_end)
# plt.plot(number_of_operation, time, "b", label="UnorderedLinkedList")
# print("linked list after")
#
#
# plt.title("Insertion Performance")
# plt.xlabel("Size")
# plt.ylabel("time")
# plt.legend(loc="upper left")
# plt.savefig("insertion_performance.png")
# # clears previous graph
# plt.clf()
#
#
# # TODO maybe remove this?
# # Section to compare insert() in various cases for max_heap
# time = []
# inputs = range(number_of_elements)
# measure_insert_time(Heap, inputs, time, len(inputs), number_of_repeats)
# plt.plot(number_of_operation, time, "g", label="Increasing order")
#
# time = []
# inputs = list(reversed(inputs))
# measure_insert_time(Heap, inputs, time, len(inputs), number_of_repeats)
# plt.plot(number_of_operation, time, "r", label="Decreasing order")
#
# time = []
# measure_insert_time(Heap, inputs, time, len(inputs), number_of_repeats)
# plt.plot(number_of_operation, time, "b", label="Random order")
#
# plt.title("Insertion Performance Max_heap")
# plt.xlabel("Size")
# plt.ylabel("time")
# plt.legend(loc="upper left")
# plt.savefig("max_heap_performance.png")
#
# TODO make section for just searching for the max
# Section for remove_max()
# time = []
# for k in range(0, len(inputs), 10):
#     best = inf
#     for _ in range(number_of_repeats):
#         max_heap = Heap(inputs[:k])
#         start = timer()
#         for _ in range(k):
#             max_heap.remove_max()
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "r", label="Heap")
#
# time = []
# for k in range(0, len(inputs), 10):
#     best = inf
#     for _ in range(number_of_repeats):
#         linked_list = LinkedList()
#         for i in inputs[:k]:
#             linked_list.insert(k)
#         start = timer()
#         for _ in range(k):
#             linked_list.remove_max()
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "b", label="UnorderedLinkedList")
#
# time = []
# for k in range(0, len(inputs), 10):
#     best = inf
#     for _ in range(number_of_repeats):
#         ordered_linked_list = OrderedLinkedList()
#         for i in inputs[:k]:
#             ordered_linked_list.insert(k)
#         start = timer()
#         for _ in range(k):
#             ordered_linked_list.remove_max()
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "g", label="OrderedLinkedList")
#
# plt.title("Remove_Max Performance")
# plt.xlabel("Size")
# plt.ylabel("time")
# plt.legend(loc="upper left")
# plt.savefig("remove_max_performance.png")
# # clears previous graph
# plt.clf()
#
#
# # FIXME change remove to remove based on index, and not value
# ## Section for remove()
# time = []
# for k in range(0, len(inputs), 10):
#     best = inf
#     to_remove = random.sample(inputs[:k], k)
#     for _ in range(number_of_repeats):
#         max_heap = Heap(inputs[:k])
#         start = timer()
#         for i in range(k):
#             max_heap.remove(to_remove[i])
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "r", label="Heap")
#
# time = []
# for k in range(0, len(inputs), 10):
#     best = inf
#     to_remove = random.sample(inputs[:k], k)
#     for _ in range(number_of_repeats):
#         linked_list = LinkedList()
#         for input in inputs[:k]:
#             linked_list.insert(input)
#         start = timer()
#         for i in range(k):
#             linked_list.remove(to_remove[i])
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "b", label="UnorderedLinkedList")
#
# time = []
# for k in range(0, len(inputs), 10):
#     best = inf
#     to_remove = random.sample(inputs[:k], k)
#     for _ in range(number_of_repeats):
#         ordered_linked_list = OrderedLinkedList()
#         for input in inputs[:k]:
#             ordered_linked_list.insert(input)
#         start = timer()
#         for i in range(k):
#             ordered_linked_list.remove(to_remove[i])
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "g", label="OrderedLinkedList")
#
# plt.title("Remove Performance")
# plt.xlabel("Size")
# plt.ylabel("time")
# plt.legend(loc="upper left")
# plt.savefig("remove_performance.png")
#
# # FIXME make these loops into functions
# # Section for increase_key()
# time = []
# number_of_repeats = 5
# number_of_operation = range(10, number_of_elements, 10)
# for k in number_of_operation:
#     best = inf
#     for _ in range(number_of_repeats):
#         prio_queue = Heap(inputs[:k])
#         start = timer()
#         for i in range(k):
#             value = prio_queue.get_value(i)
#             if value is None:
#                 value = 0
#             random_value = random.choice(range(value, interval_end))
#             prio_queue.increase_key(i, random_value)
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "r", label="Heap")
#
# time = []
# for k in number_of_operation:
#     best = inf
#     for _ in range(number_of_repeats):
#         prio_queue = LinkedList()
#         for input in inputs[:k]:
#             prio_queue.insert(input)
#         start = timer()
#         for i in range(k):
#             value = prio_queue.get_value(i)
#             if value is None:
#                 value = 0
#             random_value = random.choice(range(value, interval_end))
#             prio_queue.increase_key(i, random_value)
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "b", label="UnorderedLinkedList")
#
# time = []
# for k in number_of_operation:
#     best = inf
#     for _ in range(number_of_repeats):
#         prio_queue = OrderedLinkedList()
#         for input in inputs[:k]:
#             prio_queue.insert(input)
#         start = timer()
#         for i in range(k):
#             value = prio_queue.get_value(i)
#             if value is None:
#                 value = 0
#             random_value = random.choice(range(value, interval_end))
#             prio_queue.increase_key(i, random_value)
#         end = timer()
#         best = min(best, end - start)
#     if k % 100 == 0:
#         print(k)
#     time.append(best)
# plt.plot(number_of_operation, time, "g", label="OrderedLinkedList")
#
# plt.title("Increase_key Performance")
# plt.xlabel("Size")
# plt.ylabel("time")
# plt.legend(loc="upper left")
# plt.savefig("increase_key_performance.png")
