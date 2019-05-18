from TreeNode import TreeNode


class BinarySearchTree:
    def search(self, my_key_data, key=None):
        if key is None:
            key = self.key

        ret = []
        current: TreeNode = self.root
        while current is not None:
            if my_key_data == key(current.key):
                ret.append(current)
            if my_key_data <= key(current.key):
                current = current.left
            else:
                current = current.right
        return ret  # nothing found

    def __init__(self, key=lambda x: x):
        self.root = None
        self.key = key

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

    @staticmethod
    def _node_inorder(root):
        if root:
            yield from BinarySearchTree._node_inorder(root.left)
            yield root.key
            yield from BinarySearchTree._node_inorder(root.right)

    def inorder(self):
        return BinarySearchTree._node_inorder(self.root)

    def __iter__(self):
        yield from self.inorder()

if __name__ == "__main__":
    bst = BinarySearchTree()

    bst.insert(50)
    bst.insert(30)
    bst.insert(20)
    bst.insert(40)
    bst.insert(70)
    bst.insert(60)
    bst.insert(80)
    bst.insert(50)

    print("Traversal:")
    for key in bst:
        print(key)


    print("Search for 80:")
    print(bst.search(80).key)

