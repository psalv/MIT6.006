#!/usr/bin/env python

import bst

def height(node):
    if node is None:
        return -1
    else:
        return node.height

def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1


class AVL(bst.BST):
    """
AVL binary search tree implementation.
Supports insert, delete, find, find_min, next_larger each in O(lg n) time.
"""
    def left_rotate(self, x):
        y = x.right
        y._parent = x._parent
        if y._parent is None:
            self.root = y
        else:
            if y._parent.left is x:
                y._parent.left = y
            elif y._parent.right is x:
                y._parent.right = y
        x.right = y.left
        if x.right is not None:
            x.right._parent = x
        y.left = x
        x._parent = y

        #The order heights are updated in matters, since the correspond with the order in the tree (bottom update first).
        update_height(x)
        update_height(y)

    def right_rotate(self, x):
        y = x.left
        y._parent = x._parent
        if y._parent is None:
            self.root = y
        else:
            if y._parent.left is x:
                y._parent.left = y
            elif y._parent.right is x:
                y._parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left._parent = x
        y.right = x
        x._parent = y
        update_height(x)
        update_height(y)

    def rebalance(self, node):
        """There are only four possible cases to deal with in rebalancing.
        This works since we are working under the principle that all of th nodes below are balanced."""
        while node is not None:
            update_height(node)

            #If the left side is larger:
            if height(node.left) >= 2 + height(node.right):

                #If we are dealing with a left-left heavy situation:
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)

                #Otherwise it's a left-right heavy situation, so requires two steps:
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)

            #If the right side is larger:
            elif height(node.right) >= 2 + height(node.left):

                #One step rotation:
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)

                #Two step rotation:
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)

            #Move to the parent and rebalance again until you reach the root.
            node = node.parent

    ## find(k), find_min(), and next_larger(k) inherited from bst.BST

    def insert(self, k):
        """Inserts a node with key k into the subtree rooted at this node.
        This AVL version guarantees the balance property: h = O(lg n).
        
        Args:
            k: The key of the node to be inserted.
        """
        node = super(AVL, self).insert(k)
        self.rebalance(node)

    def delete(self, k):
        """Deletes and returns a node with key k if it exists from the BST.
        This AVL version guarantees the balance property: h = O(lg n).
        
        Args:
            k: The key of the node that we want to delete.
            
        Returns:
            The deleted node with key k.
        """
        node = super(AVL, self).delete(k)
        ## node.parent is actually the old parent of the node,
        ## which is the first potentially out-of-balance node.
        self.rebalance(node._parent)

# def test(args=None):
#     bst.test(args, BSTtype=AVL)
#
# if __name__ == '__main__': test()


A = AVL()
for i in xrange(1, 11):
    A.insert(i)

print A