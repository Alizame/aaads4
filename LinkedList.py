from Node import Node


def default_sorting_eval(data):
    """
   gets only the raw data! not an node object!!!
   :param data: node.get_data()
   :return: evaluated representation of data
   """
    return data


def default_search_eval(data):
    """
   gets only the raw data! not an node object!!!
   :param data: node.get_data()
   :return: evaluated representation of data
   """
    return data


class LinkedList:

    def __init__(self, key=default_sorting_eval):
        self.head = None
        self.key = key

    def __iter__(self):
        tmp = self.head
        while tmp is not None:
            yield tmp
            tmp = tmp.get_next()

    def clear(self):
        self.head = None

    def attach(self, data):
        self.head = Node(data, self.head)

    def insert(self, data):
        # special case: empty list, just insert new node
        if self.head is None:
            return self.attach(data)

        # special case: new ist bigger than head
        if self.key(data) <= self.key(self.head.get_data()):
            return self.attach(data)

        # normal case (also handles special case where it new_node only fits to the end):
        new_node, next_node = Node(data), self.head
        #   search for corresponding gap in LL
        while (next_node.get_next() is not None) \
                and \
                not (self.key(next_node.get_data()) <= self.key(new_node.get_data()) <= self.key(next_node.get_next().get_data())):
            next_node = next_node.get_next()

        new_node.set_next(next_node.get_next())  # print("found next_node is %s" % next_node)
        next_node.set_next(new_node)

    def search(self, my_key_data, key=None):
        if key is None:
            key = self.key
        ret = []
        for node in self:
            if my_key_data == key(node.get_data()):
                ret.append(node)
        return ret

    def delete(self, what, key=None):  # deletes all found, returns list of deleted nodes
        if key is None:
            key = self.key
        ret = self.search(what, key)
        for node in ret:
            self.delete_node(node)
        return ret

    def delete_node(self, del_node):
        # special case: head should be deleted:
        if self.head is del_node:
            self.head = self.head.get_next()
            return

        # normal case:
        next_node = self.head
        while next_node is not None and next_node.get_next() is not None:
            if next_node.get_next() is del_node:
                return next_node.set_next(next_node.get_next().get_next())
            next_node = next_node.get_next()


if __name__ == "__main__":
    ll = LinkedList()

    for i in [1, 2, 3, 4, 5, 6, 7]:
        ll.insert(i)

    print("ok")
    ll.insert(8)
    ll.insert(3.5)
    ll.insert(0)
    print("ok2")

    for itm in ll:
        print(itm)

    try:
        print("search for 3: ", end="")
        print(ll.search(3))
        print("search for 13.37: ", end="")
        print(ll.search(13.37))
    except AttributeError:
        print("Not found!!!")

    print("###################")

    print("Deleting: ")
    ls = list(ll)
    ll.delete_node(ls[0])
    ll.delete_node(ls[4])
    ll.delete_node(ls[-1])
    print("deleted!")

    for itm in ll:
        print(itm)
