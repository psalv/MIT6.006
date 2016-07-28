#!/usr/bin/env python

#This code is significantly more elegant than my own.



class BSTNode(object):
    """A node in the vanilla BST tree."""
    
    def __init__(self, parent, k):
        """Creates a node.
        
        Args:
            parent: The node's parent.
            k: key of the node.
        """
        self.key = k
        self.parent = parent
        self.left = None
        self.right = None
  
    def _str(self):
        """Internal method for ASCII art."""
        label = str(self.key)
        if self.left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.left._str()
        if self.right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.right._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
           self is self.parent.left and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.': label = ' ' + label[1:]
        if label[-1] == '.': label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
          [left_line + ' ' * (width - left_width - right_width) + right_line
           for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width
    def __str__(self):
        return '\n'.join(self._str()[0])

    def find(self, k):
        """Finds and returns the node with key k from the subtree rooted at this 
        node.
        
        Args:
            k: The key of the node we want to find.
        
        Returns:
            The node with key k.
        """
        if k == self.key:
            return self
        elif k < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(k)
        else:
            if self.right is None:  
                return None
            else:
                return self.right.find(k)
    
    def find_min(self):
        """Finds the node with the minimum key in the subtree rooted at this 
        node.
        
        Returns:
            The node with the minimum key.
        """
        current = self
        while current.left is not None:
            current = current.left
        return current
       
    def next_larger(self):
        """Returns the node with the next larger key (the successor) in the BST.

        This code is clever af. The return current.parent is the most important step.

        To find next_smaller interchange left and right, replace min with max.
        """
        if self.right is not None:
            return self.right.find_min()
        current = self
        while current.parent is not None and current is current.parent.right:
            current = current.parent
        return current.parent

    def insert(self, node):
        """Inserts a node into the subtree rooted at this node.
        
        Args:
            node: The node to be inserted.
        """
        if node is None:
            return
        if node.key < self.key:
            if self.left is None:
                node._parent = self
                self.left = node
            else:
                self.left.append(node)
        else:
            if self.right is None:
                node._parent = self
                self.right = node
            else:
                self.right.append(node)
  
    def delete(self):
        """Deletes and returns this node from the BST.

        This code finds the successor (the next greater) and replaces the node with this one.
        We do this because taking the left child means that the left child could in itself have two children:
        We need a node with either no children or only a right child: this is the trivial case that enters the first if statement.
        O(h)
        """
        if self.left is None or self.right is None:

            #If this node is on the left (change pointers).
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left._parent = self.parent

            #Or on the right (change pointers).
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right._parent = self.parent
            return self
        else:
            s = self.next_larger()
            self.key, s.key = s.key, self.key
            return s.delete()
    
    def check_ri(self):
        """Checks the BST representation invariant around this node.
    
        Raises an exception if the RI is violated.
        """
        if self.left is not None:
            if self.left.key > self.key:
                raise RuntimeError("BST RI violated by a left node key")
            if self.left._parent is not self:
                raise RuntimeError("BST RI violated by a left node parent "
                                   "pointer")
            self.left.check_ri()
        if self.right is not None:
            if self.right.key < self.key:
                raise RuntimeError("BST RI violated by a right node key")
            if self.right._parent is not self:
                raise RuntimeError("BST RI violated by a right node parent "
                                   "pointer")
            self.right.check_ri()

class MinBSTNode(BSTNode):
    """A BSTNode which is augmented to keep track of the node with the 
    minimum key in the subtree rooted at this node.

    Since this class keeps track of all mins, can find the min of any one node in O(1).
    """
    def __init__(self, parent, key):
        """Creates a node.
        
        Args:
            parent: The node's parent.
            k: key of the node.
        """
        super(MinBSTNode, self).__init__(parent, key)
        self.min = self
  
    def find_min(self):
        """Finds the node with the minimum key in the subtree rooted at this 
        node.
        
        Returns:
            The node with the minimum key.
        """
        return self.min

    def insert(self, node):
        """Inserts a node into the subtree rooted at this node.
        
        Args:
            node: The node to be inserted.
        """
        if node is None:
            return
        if node.key < self.key:
            # Updates the min of this node if the inserted node has a smaller
            # key.
            if node.key < self.min.key:
                self.min = node
            if self.left is None:
                node._parent = self
                self.left = node
            else:
                self.left.append(node)
        else:
            if self.right is None:
                node._parent = self
                self.right = node
            else:
                self.right.append(node)
  
    def delete(self):
        """Deletes this node itself.
        
        Returns:
            This node.
        """
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left._parent = self.parent
                    self.parent.min = self.parent.left.min
                else: 
                    self.parent.min = self.parent
                # Propagates the changes upwards.
                c  = self.parent
                while c._parent is not None and c is c._parent.left:
                    c._parent.min = c.min
                    c = c._parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right._parent = self.parent
            return self
        else:
            s = self.next_larger()
            self.key, s.key = s.key, self.key
            return s.delete()

class BST(object):
    """A binary search tree."""
    def __init__(self, klass = BSTNode):
        """Creates an empty BST.
        
        Args:
            klass (optional): The class of the node in the BST. Default to 
                BSTNode.
        """
        self.root = None
        self.klass = klass
        
    def __str__(self):
        if self.root is None: return '<empty tree>'
        return str(self.root)

    def find(self, k):
        """Finds and returns the node with key k from the subtree rooted at this 
        node.
        
        Args:
            k: The key of the node we want to find.
        
        Returns:
            The node with key k or None if the tree is empty.
        """
        return self.root and self.root.find(k)
                
    def find_min(self):
        """Returns the minimum node of this BST."""
        
        return self.root and self.root.find_min()
    
    def insert(self, k):
        """Inserts a node with key k into the subtree rooted at this node.
        
        Args:
            k: The key of the node to be inserted.
            
        Returns:
            The node inserted.
        """
        node = self.klass(None, k)
        if self.root is None:
            # The root's parent is None.
            self.root = node
        else:
            self.root.append(node)
        return node
            
    def delete(self, k):
        """Deletes and returns a node with key k if it exists from the BST.
        
        Args:
            k: The key of the node that we want to delete.
            
        Returns:
            The deleted node with key k.
        """
        node = self.find(k)
        if node is None:
            return None
        if node is self.root:
            pseudoroot = self.klass(None, 0)
            pseudoroot.left = self.root
            self.root._parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root._parent = None
            return deleted
        else:
            return node.delete()   
        
    def next_larger(self, k):
        """Returns the node that contains the next larger (the successor) key in
        the BST in relation to the node with key k.
        
        Args:
            k: The key of the node of which the successor is to be found.
            
        Returns:
            The successor node.
        """
        node = self.find(k)
        return node and node.next_larger()
    
    def check_ri(self):
        """Checks the BST representation invariant.
        
        Raises:
            An exception if the RI is violated.
        """
        if self.root is not None:
            if self.root._parent is not None:
                raise RuntimeError("BST RI violated by the root node's parent " 
                                   "pointer.")
            self.root.check_ri()
    

class MinBST(BST):
    """An augmented BST that keeps track of the node with the minimum key."""
    def __init__(self):
        super(MinBST, self).__init__(MinBSTNode)

def test(args=None, BSTtype=BST):
    import random, sys
    if not args:
        args = sys.argv[1:]
    if not args:
        print 'usage: %s <number-of-random-items | item item item ...>' % \
              sys.argv[0]
        sys.exit()
    elif len(args) == 1:
        items = (random.randrange(100) for i in xrange(int(args[0])))
    else:
        items = [int(i) for i in args]

    tree = BSTtype()
    print tree
    for item in items:
        tree.insert(item)
        print
        print tree

if __name__ == '__main__': test()
