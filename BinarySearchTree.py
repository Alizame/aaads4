from StudiObject import StudiObject
from TreeNode import TreeNode


class BinarySearchTree:

    def __init__(self, key=lambda x: x):
        self.root = None
        self.key = key

    def __iter__(self):
        yield from self.inorder()

    def _find_parent(self, child_node):
        current_parent = self.root
        # special case child_node is root:
        if id(current_parent) == id(child_node):
            raise Exception("root-node has no parent!")

        while current_parent is not None:
            # if it is parent, return it
            if current_parent.left is child_node or current_parent.right is child_node:
                return current_parent
            # this isn't the parent, try next one
            if self.key(child_node.key) <= self.key(current_parent.key):
                current_parent = current_parent.left
            else:
                current_parent = current_parent.right

        raise Exception("no parent found!")

    def search(self, my_key_data, key=None):
        ret = []
        current: TreeNode = self.root

        if key is None or key is self.key:
            while current is not None:
                if my_key_data == self.key(current.key):
                    ret.append(current)
                if my_key_data <= self.key(current.key):
                    current = current.left
                else:
                    current = current.right
        else:  # we need to use a different key-func, so our nicely sorted BST is irrelevant and we need to find it by iterating over everything ;(
            for current in self._node_inorder(self.root):
                if my_key_data == key(current.key):
                    ret.append(current)
        return ret  # returns [] if nothing found


    def _insert(self, root: TreeNode, new_node: TreeNode):
        if self.key(new_node.key) <= self.key(root.key):
            # muss links von root eingefügt werden
            if root.left is None:
                root.left = new_node
            else:
                self._insert(root.left, new_node)
        else:
            # muss rechts von root eingefügt werden
            if root.right is None:
                root.right = new_node
            else:
                self._insert(root.right, new_node)

    def insert(self, val):
        new_node = TreeNode(val)
        # special case root is empty:
        if self.root is None:
            self.root = new_node
            return
        # normal case:
        self._insert(self.root, new_node)
        return new_node

    @staticmethod
    def _inorder(root):
        if root:
            yield from BinarySearchTree._inorder(root.left)
            yield root.key
            yield from BinarySearchTree._inorder(root.right)

    @staticmethod
    def _node_inorder(root):
        if root:
            yield from BinarySearchTree._node_inorder(root.left)
            yield root
            yield from BinarySearchTree._node_inorder(root.right)

    def inorder(self):
        return BinarySearchTree._inorder(self.root)

    def delete(self, what, key=None):  # deletes all found, returns list of deleted nodes
        ret = self.search(what, key)
        for node in ret:
            self.delete_node(node)
        #return ret

    def _get_inorder_successor(self, node: TreeNode):
        try:
            my_generator = self._node_inorder(node.right)
            successor = next(my_generator)  # if this fails it means it didn't have 2 children
            return successor
        except:
            raise Exception("no successor found!")

    def delete_node(self, del_node: TreeNode):
        if del_node is None:
            return print("Can't delete a non-existing Node!")

        # Node is a leaf
        elif del_node.left is None and del_node.right is None:
            parent = self._find_parent(del_node)
            if self.key(del_node.key) <= self.key(parent.key):
                parent.left = None
            else:
                parent.right = None

        # Node has a left child
        elif del_node.left is not None and del_node.right is None:
            if del_node is self.root:
                self.root = del_node.left
            else:
                parent = self._find_parent(del_node)
                if parent.right is del_node:
                    parent.right = del_node.left
                elif parent.left is del_node:
                    parent.left = del_node.left
                else:
                    raise Exception("ok, we just destroyed causality!?")

        # Node has a right child
        elif del_node.left is None and del_node.right is not None:
            if del_node is self.root:
                self.root = del_node.right
            else:
                parent = self._find_parent(del_node)
                if parent.right is del_node:
                    parent.right = del_node.right
                elif parent.left is del_node:
                    parent.left = del_node.right
                else:
                    raise Exception("ok, we just destroyed causality!?")

        # Node has 2 children
        else:
            # 1. find minimum from right subtree
            my_generator = self._node_inorder(del_node.right)
            minimum_node = next(my_generator)  # if this fails it means it didn't have 2 children
            # 2. replace value of del_node with this minimum-value
            tmp = minimum_node.key
            # 3. call delete for minimum-node
            self.delete_node(minimum_node)
            del_node.key = tmp

    def change_value(self, modified_node):
        val = modified_node.key
        self.delete_node(modified_node)
        self.insert(val)


if __name__ == "__main__":

    bst = BinarySearchTree()

    # bst.insert(StudiObject("B", 2))
    # bst.insert(StudiObject("A", 1))
    # bst.insert(StudiObject("C", 99999))
    # bst.insert(StudiObject("D", 10))
    # bst.insert(StudiObject("E", 223))

    a = bst.insert(100)
    bst.insert(99)
    bst.insert(98)


    print("Traversal:")
    for k in bst:
        print(k)

    s = bst.search(99)
    print("search for 99: %s" % s)

    print("Delete searched node:")
    bst.delete_node(s[0])

    print("Traversal:")
    for k in bst:
        print(k)

