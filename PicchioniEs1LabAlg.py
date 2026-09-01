from math import inf, log, ceil
from time import perf_counter as timer
import matplotlib.pyplot as plt
import random


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
            return
        self.heap[i] = key
        while i > 0 and self.heap[self.get_parent(i)] < self.heap[i]:
            swapped = self.heap[self.get_parent(i)]
            self.heap[self.get_parent(i)] = self.heap[i]
            self.heap[i] = swapped
            i = self.get_parent(i)

    # works on the index of the element, not the value
    def is_leaf(self, i):
        return i > (len(self.heap) // 2) and i <= len(self.heap)

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

    def increase_key(self, i, key):
        self.remove_at_index(i)
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


def plot_graph(data_type, number_of_operation, time):
    if data_type == 0:
        label = "Heap"
        color = "r"
    elif data_type == 1:
        label = "OrderedLinkedList"
        color = "g"
    else:
        label = "LinkedList"
        color = "b"
    plt.plot(number_of_operation, time, color, label=label)
    print("-- finished testing for " + label)


def measure_insert_time(data_type, number_of_operation, elements, time, repeats):
    if data_type == 0:
        prio_queue = Heap()
    elif data_type == 1:
        prio_queue = OrderedLinkedList()
    else:
        prio_queue = LinkedList()
    for i in number_of_operation:
        best = inf
        for j in range(repeats):
            new_value = elements[i]
            start = timer()
            prio_queue.insert(new_value)
            end = timer()
            best = min(best, end - start)
            if j == repeats - 1:
                break
            prio_queue.remove(new_value)

        time.append(best)
    plot_graph(data_type, number_of_operation, time)


def insert_test(
    test_type,
    types_to_test,
    number_of_elements,
    number_of_operation,
    interval_end,
    number_of_repeats,
    inputs,
):
    # Testing insertion of highest value
    if test_type == 1:
        test_type_string = "highest"
        inputs = range(number_of_elements)
        print("## Testing insertion of highest value")
    # Testing insertion of lowest value
    elif test_type == 2:
        test_type_string = "lowest"
        inputs = range(number_of_elements, 0, -1)
        print("## Testing insertion of lowest value")
    else:
        # Testing insertion of random value
        test_type_string = "random"
        inputs = random.choices(range(interval_end), k=number_of_elements)
        print("## Testing insertion of a random value")

    for i in types_to_test:
        time = []
        measure_insert_time(
            i,
            number_of_operation,
            inputs,
            time,
            number_of_repeats,
        )

    plt.title("Insertion Performance, " + test_type_string + " value")
    if len(types_to_test) < 3:
        test_type_string = "no_ordered"
    plt.xlabel("Size")
    plt.ylabel("time")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("insertion_performance_" + test_type_string + ".png")
    plt.clf()


def remove_max_test(
    data_type,
    number_of_operation,
    number_of_repeats,
    inputs,
):

    time = []
    for k in number_of_operation:
        best = inf
        for _ in range(number_of_repeats):
            if data_type == 0:
                prio_queue = Heap()
            elif data_type == 1:
                prio_queue = OrderedLinkedList()
            else:
                prio_queue = LinkedList()
            for e in inputs[:k]:
                prio_queue.insert(e)

            start = timer()
            prio_queue.remove_max()
            end = timer()
            best = min(best, end - start)
        time.append(best)

    plot_graph(data_type, number_of_operation, time)


def increase_key_test(
    data_type,
    number_of_operation,
    interval_end,
    number_of_repeats,
    inputs,
):
    time = []

    for k in number_of_operation:
        best = inf
        for _ in range(number_of_repeats):
            if data_type == 0:
                prio_queue = Heap()
            elif data_type == 1:
                prio_queue = OrderedLinkedList()
            else:
                prio_queue = LinkedList()
            for e in inputs[:k]:
                prio_queue.insert(e)

            random_index = k - 1
            value = prio_queue.get_value(random_index)
            if value is None:
                value = 0
            random_value = random.choice(range(value, interval_end))
            start = timer()
            prio_queue.increase_key(random_index, random_value)
            end = timer()
            best = min(best, end - start)
        time.append(best)

    plot_graph(data_type, number_of_operation, time)


number_of_elements = 300
step = 1
number_of_operation = range(step, number_of_elements, step)
interval_end = 30000
number_of_repeats = 10
inputs = random.choices(range(interval_end), k=number_of_elements)

print("# Testing Insertion cases")
types_to_test = range(3)
for i in range(3):
    insert_test(
        i,
        types_to_test,
        number_of_elements,
        number_of_operation,
        interval_end,
        number_of_repeats,
        inputs,
    )

print("# Testing Insertion cases, only Heap and LinkedList")
types_to_test = [0, 2]
insert_test(
    1,
    types_to_test,
    number_of_elements,
    number_of_operation,
    interval_end,
    number_of_repeats,
    inputs,
)

print("# Testing Remove_Max")
for i in range(3):
    remove_max_test(
        i,
        number_of_operation,
        number_of_repeats,
        inputs,
    )

plt.title("Remove_Max Performance")
plt.xlabel("Size")
plt.ylabel("time")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("remove_max_performance.png")
plt.clf()

print("# Testing Remove_Max, only Heap and OrderedLinkedList")
for i in range(2):
    remove_max_test(
        i,
        number_of_operation,
        number_of_repeats,
        inputs,
    )

plt.title("Remove_Max Performance")
plt.xlabel("Size")
plt.ylabel("time")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("remove_max_performance_no_linked.png")
plt.clf()

print("# Testing Increase_key")
for i in range(3):
    increase_key_test(
        i,
        number_of_operation,
        interval_end,
        number_of_repeats,
        inputs,
    )

plt.title("Increase_key Performance")
plt.xlabel("Size")
plt.ylabel("time")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("increase_key_performance.png")
plt.clf()
