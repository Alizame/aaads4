
class TreeNode:
    def __init__(self, key):
        self.key = key

        self.left: TreeNode = None
        self.right: TreeNode = None

    def __repr__(self):
        return str(self.key)
