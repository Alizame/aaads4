from AvlNode import AvlNode


class AvlTree:
    def __init__(self, key=lambda x: x):
        self.root = None
        self.key = key

    def __iter__(self):
        yield from self.inorder()

    def inorder(self):
        """
        iterator that goes through inorder and returns data
        :return:
        """
        return self._inorder(self.root)

    def inorder_node(self):
        """
        iterator that goes through inorder and returns node-objects
        :return: iterator
        """
        return self._inorder_node(self.root)

    def preorder_node(self):
        """
        iterator that goes through preorder and returns node-objects
        :return: iterator
        """
        return self._preorder_node(self.root)


    def _inorder(self, root: AvlNode):
        if root:
            yield from self._inorder(root.left)
            yield root.val
            yield from self._inorder(root.right)

    def _inorder_node(self, root: AvlNode):
        if root:
            yield from self._inorder_node(root.left)
            yield root
            yield from self._inorder_node(root.right)

    def _preorder_node(self, root: AvlNode):
        if root:
            yield root
            yield from self._inorder_node(root.left)
            yield from self._inorder_node(root.right)

    def search(self, my_key_data, key=None):
        """
        searches for all nodes with a specific key
        :param my_key_data: key-val that should be found
        :param key: key-function
        :return: list of nodes (empty if no nodes found)
        """
        ret = []
        current: AvlNode = self.root

        if key is None or key is self.key:
            while current is not None:
                if my_key_data == self.key(current.val):
                    ret.append(current)
                if my_key_data <= self.key(current.val):
                    current = current.left
                else:
                    current = current.right
        else:  # we need to use a different key-func, so our nicely sorted BST is irrelevant and we need to find it by iterating over everything ;(
            for current in self._inorder_node(self.root):
                if my_key_data == key(current.val):
                    ret.append(current)
        return ret  # returns [] if nothing found

    def insert(self, data):
        """
        insert a new element
        :param data: elements data
        :return: -
        """
        new_node = AvlNode(data)
        if self.root is None:
            self.root = new_node
        else:
            self.root = self._insert(self.root, new_node)

    def _insert(self, root: AvlNode, new_node: AvlNode) -> AvlNode:
        key = self.key(new_node.val)

        # Step 1 - Perform normal BST
        if not root:
            return new_node
        elif key <= self.key(root.val):
            root.left = self._insert(root.left, new_node)
        else:
            root.right = self._insert(root.right, new_node)

        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(root.left.get_height() if root.left else 0,
                              root.right.get_height() if root.right else 0)

        return self._rebalance(root)  # Step 3 & 4, get balance-factor and rebalance if necessary

    def _rebalance(self, root: AvlNode) -> AvlNode:
        # Step 3 - Get the balance factor
        balance = root.get_balance()

        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and root.left.get_balance() >= 0:
            return self._right_rotate(root)

        # Case 2 - Right Right
        if balance < -1 and root.right.get_balance() <= 0:
            return self._left_rotate(root)

        # Case 3 - Left Right
        if balance > 1 and root.left.get_balance() < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Case 4 - Right Left
        if balance < -1 and root.right.get_balance() > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
        return root

    def _right_rotate(self, z: AvlNode) -> AvlNode:
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # update heights
        z.height = 1 + max(z.left.get_height() if z.left else 0,
                           z.right.get_height() if z.right else 0)
        y.height = 1 + max(y.left.get_height() if y.left else 0,
                           y.right.get_height() if y.right else 0)

        # return new root
        return y

    def _left_rotate(self, z: AvlNode) -> AvlNode:
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # update heights
        z.height = 1 + max(z.left.get_height() if z.left else 0,
                           z.right.get_height() if z.right else 0)
        y.height = 1 + max(y.left.get_height() if y.left else 0,
                           y.right.get_height() if y.right else 0)

        # return new root
        return y

    def find_inorder_successor(self, root: AvlNode) -> AvlNode:
        """
        finds inorder successor of a node
        :param root: node of which the inorder successor should be found
        :return: the inorder successor node
        """
        if root is None or root.left is None:
            return root

        return self.find_inorder_successor(root.left)

    def delete_node(self, del_node: AvlNode):
        """
        deletes a node from the Tree
        :param del_node: node that should be deleted
        :return: -
        """
        self.root = self._delete(self.root, del_node)

    def delete(self, what, key=None):  # deletes all found, returns list of deleted nodes
        ret = self.search(what, key)
        for node in ret:
            self.delete_node(node)
        #return ret

    def _delete(self, root: AvlNode, del_node: AvlNode):  # returns new root!
        # Step 1: Perform standard BST delete
        if not root:
            return root
        elif self.key(del_node.val) <= self.key(root.val) and root is not del_node:
            root.left = self._delete(root.left, del_node)
        elif self.key(del_node.val) > self.key(root.val):
            root.right = self._delete(root.right, del_node)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.find_inorder_successor(root.right)
            root.val = temp.val
            root.right = self._delete(root.right, temp)
        # if tree has only one node, simply return it
        if root is None:
            return root

        # Step 2: Update the height of the ancestor node
        root.height = 1 + max(root.left.get_height() if root.left else 0,
                              root.right.get_height() if root.right else 0)

        return self._rebalance(root)  # Step 3 & 4, get balance-factor and rebalance if necessary

    def change_value(self, modified_node):
        val = modified_node.key
        self.delete_node(modified_node)
        self.insert(val)

if __name__ == "__main__":
    # Test for AvlTree
    myTree = AvlTree()
    a = [10, 20, 30, 40, 50, 25, 20]
    for itm in a:
        myTree.insert(itm)

    for itm in a:
        s = myTree.search(itm)
        assert len(s) == 1 or s[0].val == 20
        assert s[0].get_balance() in [-1, 0, 1]

    # expected result (after insertions):
    #              30
    #             / \
    #            20 40
    #            / \  \
    #           10 25  50
    #             \
    #             20
    assert myTree.root.val == 30
    assert myTree.root.right.val == 40
    assert myTree.root.right.right.val == 50
    assert myTree.root.left.val == 20
    assert myTree.root.left.left.val == 10
    assert myTree.root.left.left.right.val == 20
    assert myTree.root.left.right.val == 25

    # test search
    assert myTree.search(30)[0] is myTree.root

    # expected result (after all deletions):
    #          25
    #          / \
    #        20   40
    s = myTree.search(20)[1]
    myTree.delete_node(s)  # delete second found node with value 20 (the leaf one)
    assert myTree.root.val == 30
    assert myTree.root.right.val == 40
    assert myTree.root.right.right.val == 50
    assert myTree.root.left.val == 20
    assert myTree.root.left.left.val == 10
    assert myTree.root.left.left.right is None  # <= deleted node
    assert myTree.root.left.right.val == 25
    myTree.delete_node(myTree.search(30)[0])
    myTree.delete_node(myTree.search(10)[0])
    assert myTree.root.val == 40
    assert myTree.root.left.val == 20
    assert myTree.root.left.right.val == 25
    assert myTree.root.right.val == 50
    myTree.delete_node(myTree.search(50)[0])
    assert myTree.root.val == 25
    assert myTree.root.left.val == 20
    assert myTree.root.right.val == 40

    print("#########")
    print("inorder traversal:")

    for val in myTree.inorder_node():
        print(val)
