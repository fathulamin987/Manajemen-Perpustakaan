class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:

    def __init__(self):
        self.root = None

    def insert(self, data):

        if self.root is None:
            self.root = Node(data)

        else:
            self._insert(self.root, data)

    def _insert(self, current, data):

        if data["judul"].lower() < current.data["judul"].lower():

            if current.left is None:
                current.left = Node(data)

            else:
                self._insert(current.left, data)

        else:

            if current.right is None:
                current.right = Node(data)

            else:
                self._insert(current.right, data)

    def inorder(self):

        hasil = []

        self._inorder(self.root, hasil)

        return hasil

    def _inorder(self, node, hasil):

        if node:

            self._inorder(node.left, hasil)

            hasil.append(node.data)

            self._inorder(node.right, hasil)