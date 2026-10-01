from math import inf, log, ceil
from time import perf_counter as timer
import matplotlib.pyplot as plt
import random
from copy import deepcopy
import sys

# to avoid hitting maximum recursion depth when running deepcopy(prio_queue)
sys.setrecursionlimit(100000)


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
            swapped = self.heap[i]
            self.heap[i] = self.heap[largest]
            self.heap[largest] = swapped
            self.heapify(largest)

    def insert(self, key):
        self.heap.append(-inf)
        self.increase_key(len(self.heap) - 1, key)

    def remove(self, key):
        i = 0  # root node
        while i < len(self.heap) and self.heap[i] != key:
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

    def increase_key(self, i, new_key):
        if i >= len(self.heap):
            print("index out of range")
            return
        if new_key < self.heap[i]:
            return
        self.heap[i] = new_key
        while i > 0 and self.heap[self.get_parent(i)] < self.heap[i]:
            swapped = self.heap[self.get_parent(i)]
            self.heap[self.get_parent(i)] = self.heap[i]
            self.heap[i] = swapped
            i = self.get_parent(i)

    def get_parent(self, i):
        return (i - 1) // 2

    def print(self):
        num_of_levels = log(len(self.heap), 2)
        num_of_levels = ceil(num_of_levels)
        start = 1
        for i in range(1, num_of_levels + 2):
            max = 2 ** (i)
            for j in range(start, max):
                if j > len(self.heap):
                    break
                print(self.heap[j - 1], end=", ")
            print("")
            start = max

    def get_len(self):
        return len(self.heap)

    def get_value(self, i):
        if i > len(self.heap):
            return
        else:
            return self.heap[i]


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


class LinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def find_set(self):
        return self.head

    def insert(self, key):
        new_node = Node(key, self, None)
        if self.head is None:
            self.head = new_node
        else:
            self.tail.set_next(new_node)
        self.tail = new_node

    def remove(self, key):
        if self.head is None:
            print("error: list contains no elements")
            return
        node = self.head
        previous = None
        while node is not None:
            if node.get_data() == key:
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

    def remove_at_index(self, i):
        if i >= self.get_len():
            print("error: index is greater than list length")
            return
        node = self.head
        previous = None
        for _ in range(i):
            previous = node
            node = node.get_next()
        if previous is None:
            self.head = node.get_next()
        else:
            previous.set_next(node.get_next())
            if self.tail == node:
                self.tail = previous

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
        node = self.head
        if node is None:
            return
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


class OrderedLinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def is_empty(self):
        return self.head is None

    def insert(self, key):
        if self.head is None:
            new_node = Node(key, self, None)
            self.head = new_node
            self.tail = new_node
            return

        node = self.head
        previous = None
        while node is not None:
            if key >= node.get_data():
                new_node = Node(key, self, node)
                if previous is not None:
                    previous.set_next(new_node)
                else:
                    self.head = new_node
                    self.tail = node
                return
            else:
                previous = node
                if node.get_next() is None:
                    new_node = Node(key, self, None)
                    node.set_next(new_node)
                    return
                else:
                    node = node.next
        print("error: no matching item to remove was found")

    def remove(self, key):
        if self.head is None:
            print("error: list contains no elements")
            return
        node = self.head
        previous = None
        while node is not None:
            if node.get_data() == key:
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

    def remove_at_index(self, i):
        node = self.head
        previous = None
        if node is None:
            print("list is empty")
            return
        for _ in range(i):
            if node.get_next() is None:
                print("index out of range")
                return
            previous = node
            node = node.get_next()
        if previous is None:
            self.head = node.get_next()
        else:
            previous.set_next(node.get_next())
            if self.tail == node:
                self.tail = previous

    def get_max(self):
        return self.head

    def remove_max(self):
        if self.head is None:
            return
        max = self.head
        self.head = self.head.get_next()
        return max

    def increase_key(self, i, new_key):
        self.remove_at_index(i)
        self.insert(new_key)

    def get_len(self):
        node = self.head
        i = 0
        while node is not None:
            i += 1
            node = node.get_next()
        return i

    def get_value(self, i):
        node = self.head
        if node is None:
            return
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


class Tests:
    def __init__(
        self,
        intervals,
        repeats,
        max_value,
        max_length,
    ):
        self.intervals = intervals
        self.repeats = repeats
        self.max_value = max_value
        self.max_length = max_length
        self.random_inputs()

    def random_inputs(self):
        self.inputs = random.choices(range(max_value), k=max_length)

    def plot_graph(self, data_type, time):
        if data_type == 0:
            label = "Heap"
            color = "r"
        elif data_type == 1:
            label = "OrderedLinkedList"
            color = "g"
        else:
            label = "LinkedList"
            color = "b"
        plt.plot(self.intervals, time, color, label=label)
        print("-- finished testing for " + label)

    def measure_insert_time(self, data_type, time):
        if data_type == 0:
            prio_queue = Heap()
        elif data_type == 1:
            prio_queue = OrderedLinkedList()
        else:
            prio_queue = LinkedList()

        for k in intervals:
            best = inf
            for i in range(prio_queue.get_len(), k):
                prio_queue.insert(self.inputs[i])
            for _ in range(self.repeats):
                temp_prio = deepcopy(prio_queue)
                new_value = self.inputs[k]
                start = timer()
                temp_prio.insert(new_value)
                end = timer()
                best = min(best, end - start)
            time.append(best)
        self.plot_graph(data_type, time)

    def insert_test(
        self,
        test_type,
    ):
        # Testing insertion of highest value
        if test_type == 1:
            test_type_string = "ascending"
            self.inputs = range(self.max_length)
            print("## Testing insertion of ascending values")
        # Testing insertion of lowest value
        elif test_type == 2:
            test_type_string = "descending"
            self.inputs = range(self.max_length, 0, -1)
            print("## Testing insertion of descending values")
        else:
            # Testing insertion of random value
            test_type_string = "random"
            self.random_inputs()
            print("## Testing insertion of random values")

        # this means that the order they'll be tested will be: Heap, LinkedList and, lastly, OrderedLinkedList
        for i in [0, 2, 1]:
            time = []
            self.measure_insert_time(i, time)
            # Saves the graph without the OrderedLinkedList in separate files
            if i == 2:
                plt.title(
                    "Insertion Performance, " + "no ord" + test_type_string + " values"
                )
                plt.xlabel("Size")
                plt.ylabel("time")
                plt.legend(loc="upper left")
                plt.tight_layout()
                plt.savefig(
                    "insertion_performance_" + test_type_string + "_no_ord" + ".png"
                )

        # Saves the graph with all three data structures
        plt.title("Insertion Performance, " + test_type_string + " values")
        plt.xlabel("Size")
        plt.ylabel("time")
        plt.legend(loc="upper left")
        plt.tight_layout()
        plt.savefig("insertion_performance_" + test_type_string + ".png")
        plt.clf()

    def remove_max_test(
        self,
        data_type,
    ):
        time = []
        if data_type == 0:
            prio_queue = Heap()
        elif data_type == 1:
            prio_queue = OrderedLinkedList()
        else:
            prio_queue = LinkedList()

        for k in self.intervals:
            best = inf
            for i in range(prio_queue.get_len(), k):
                prio_queue.insert(self.inputs[i])
            for _ in range(self.repeats):
                temp_prio = deepcopy(prio_queue)
                start = timer()
                temp_prio.remove_max()
                end = timer()
                best = min(best, end - start)
            time.append(best)

        self.plot_graph(data_type, time)

    def increase_key_test(
        self,
        data_type,
    ):
        time = []
        if data_type == 0:
            prio_queue = Heap()
        elif data_type == 1:
            prio_queue = OrderedLinkedList()
        else:
            prio_queue = LinkedList()

        for k in self.intervals:
            best = inf
            for i in range(prio_queue.get_len(), k):
                prio_queue.insert(self.inputs[i])
            for _ in range(self.repeats):
                temp_prio = deepcopy(prio_queue)
                target_index = temp_prio.get_len() - 1
                value = temp_prio.get_value(target_index)
                if value is None:
                    value = 0
                random_value = random.choice(range(value, self.max_value))

                start = timer()
                temp_prio.increase_key(target_index, random_value)
                end = timer()
                best = min(best, end - start)
            time.append(best)

        self.plot_graph(data_type, time)


max_length = 3000
step = 100
intervals = range(step, max_length, step)
max_value = 30000
repeats = 1
tester = Tests(intervals, repeats, max_value, max_length)


print("# Testing Remove_Max")
# range indicates it'll test all three types of data structures
for i in range(3):
    tester.remove_max_test(i)

    if i == 1:  # case without linked list. save to separate file
        plt.title("Remove_Max Performance")
        plt.xlabel("Size")
        plt.ylabel("time")
        plt.legend(loc="upper left")
        plt.tight_layout()
        plt.savefig("remove_max_performance_no_linked.png")

# saving the graph with all three data structures
plt.title("Remove_Max Performance")
plt.xlabel("Size")
plt.ylabel("time")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("remove_max_performance.png")
plt.clf()

print("# Testing Increase_key")
for i in range(3):
    tester.increase_key_test(i)

plt.title("Increase_key Performance")
plt.xlabel("Size")
plt.ylabel("time")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("increase_key_performance.png")
plt.clf()

print("# Testing Insertion cases")

# the range indicates the types of sets that will be inserted
# 0 random values, 1 ascending values, 2 descending values
for i in range(3):
    tester.insert_test(i)

# TODO make tests to make a table for values
