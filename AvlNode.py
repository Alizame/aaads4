from __future__ import annotations


class AvlNode:
    def __init__(self, data):
        self.left: AvlNode = None
        self.right: AvlNode = None
        self.val = data
        self.height = 1

    def __str__(self):
        ret = "%s(h: %s, b: %s): " % (self.val, self.height, self.get_balance())

        if self.left is not None:
            ret += "%s(h: %s, b: %s), " % (self.left.val, self.left.height, self.left.get_balance())
        else:
            ret += "null, "

        if self.right is not None:
            ret += "%s(h: %s, b: %s)" % (self.right.val, self.right.height, self.right.get_balance())
        else:
            ret += "null"
        return ret  # + " id=%s" % id(self)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _get_height(node: AvlNode) -> int:
        if not node:
            return 0
        return node.height

    def get_height(self) -> int:
        """
        returns the height of this node (leafs have height of 0)
        :return: height of node
        """
        return self._get_height(self)

    def _get_balance(self, node: AvlNode) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def get_balance(self):
        """
        returns the balance of this node (leafs have a balance of 0)
        :return: balance of node
        """
        return self._get_balance(self)


if __name__ == "__main__":
    a = AvlNode(2)
    a.left = AvlNode(1)
    a.right = AvlNode(3)
    a.right.right = AvlNode(4)

    assert a.get_balance() == 0
    assert a.left.get_height() == 1
    assert a.right.get_height() == 1

