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

    def __init__(self):
        self.head = None

    def __iter__(self):
        tmp = self.head
        while tmp is not None:
            yield tmp
            tmp = tmp.get_next()

    def clear(self):
        self.head = None

    def attach(self, data):
        self.head = Node(data, self.head)

    def attach_sorted(self, data, key=default_sorting_eval):
        # special case: empty list, just insert new node
        if self.head is None:
            return self.attach(data)

        # special case: new ist bigger than head
        if key(data) <= key(self.head.get_data()):
            return self.attach(data)

        # normal case (also handles special case where it new_node only fits to the end):
        new_node, next_node = Node(data), self.head
        #   search for corresponding gap in LL
        while (next_node.get_next() is not None) \
                and \
                not (key(next_node.get_data()) <= key(new_node.get_data()) <= key(next_node.get_next().get_data())):
            next_node = next_node.get_next()

        new_node.set_next(next_node.get_next())  # print("found next_node is %s" % next_node)
        next_node.set_next(new_node)

    def search(self, my_key_data, key=default_sorting_eval):
        ret = []
        for node in self:
            if my_key_data == key(node.get_data()):
                ret.append(node)
        return ret

    def delete(self, my_key_data, key=default_sorting_eval):  # deletes all found, returns list of deleted nodes
        ret = []  # list of deleted elements

        # special case: head should be deleted (and the following new heads...):
        while my_key_data == key(self.head.get_data()):
            ret.append(self.head)
            self.head = self.head.get_next()

        # normal case:
        next_node = self.head  # self.head is now a "not to be deleted node"
        while next_node is not None and next_node.get_next() is not None:  # 1. part is because of deleted nodes
            if my_key_data == key(next_node.get_next().get_data()):  # find matching node
                ret.append(next_node.get_next())
                next_node.set_next(next_node.get_next().get_next())
            next_node = next_node.get_next()
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
        ll.attach_sorted(i)

    print("ok")
    ll.attach_sorted(8)
    ll.attach_sorted(3.5)
    ll.attach_sorted(0)
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
