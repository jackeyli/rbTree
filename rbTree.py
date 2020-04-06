
import random
import time
class RedBlackNode:
    def __init__(self, val, color):
        self.val = val
        self.color = color
        self.left = self.right = self.parent = None
    def __eq__(self,other):
        return self.val == other
    def __ne__(self,other):
        return self.val != other
    def __lt__(self,other):
        return self.val < other
    def __gt__(self,other):
        return self.val > other
    def __le__(self,other):
        return self.val <= other
    def __ge__(self,other):
        return self.val >= other
class RedBlackTree:
    COLOR_RED = 0
    COLOR_BLACK = 1
    def __init__(self):
        self.root = None
    def __iadd__(self,other):
        self.__addVal(other)
        return self
    def __isub__(self,other):
        self.__delVal(other)
        return self
    def __addVal(self,val):
        if self.root is None:
            self.root = RedBlackNode(val,RedBlackTree.COLOR_BLACK)
            return
        else:
            pNode = self.__findInsert(self.root,val)
            if pNode is None:
                return
            else:
                newNode = RedBlackNode(val,RedBlackTree.COLOR_RED)
                if pNode.val > val:
                    pNode.left = newNode
                else:
                    pNode.right = newNode
                newNode.parent = pNode
                self.__insertFix(pNode,newNode)
        if __debug__:
            self.__checkRules()
    def __getBrother(self,node : RedBlackNode):
        pParent : RedBlackNode = node.parent
        if pParent.left == node:
            return pParent.right
        else:
            return pParent.left
    def __assertParentPt(self,node:RedBlackNode):
        if node.left is not None:
            if node.left.parent is not node:
                assert(False)
            self.__assertParentPt(node.left)
        if node.right is not None:
            if node.right.parent is not node:
                assert (False)
            self.__assertParentPt(node.right)
    def __rotateRight(self,parent:RedBlackNode,child:RedBlackNode):
        if __debug__:
            self.__assertParentPt(self.root)
        pParent = parent.parent
        if pParent is not None:
            isParentLeft = pParent.left == parent
            if isParentLeft:
                pParent.left = child
            else:
                pParent.right = child
            parent.left = child.right
            if child.right is not None:
                child.right.parent = parent
            child.right = parent
            parent.parent = child
            child.parent = pParent
        else:
            self.root = child
            parent.left = child.right
            if child.right is not None:
                child.right.parent = parent
            child.right = parent
            parent.parent = child
            child.parent = None
        if __debug__:
            self.__assertParentPt(self.root)
    def __rotateLeft(self,parent:RedBlackNode,child:RedBlackNode):
        if __debug__:
            self.__assertParentPt(self.root)
        pParent = parent.parent
        if pParent is not None:
            isParentLeft = pParent.left == parent
            if isParentLeft:
                pParent.left = child
            else:
                pParent.right = child
            parent.right = child.left
            if child.left is not None:
                child.left.parent = parent
            child.left = parent
            parent.parent = child
            child.parent = pParent
        else:
            self.root = child
            parent.right = child.left
            if child.left is not None:
                child.left.parent = parent
            child.left = parent
            parent.parent = child
            child.parent = None
        if __debug__:
            self.__assertParentPt(self.root)
    def __writeNode(self,node:RedBlackNode,content):
        content += f'{node.val}[style=filled,fillcolor={"red" if node.color == RedBlackTree.COLOR_RED else "black"}]\n'
        if node.left is not None:
            content += f'{node.val}->{node.left.val}\n'
            content = self.__writeNode(node.left,content)
        if node.right is not None:
            content += f'{node.val}->{node.right.val}\n'
            content = self.__writeNode(node.right,content)
        return content
    def __dotFile(self):
        content = "digraph G{\nnode[fontcolor=white]\n"
        if self.root is not None:
            content = self.__writeNode(self.root,content)
        content += "}"
        return content
    def __insertFix(self,parent : RedBlackNode,newNode : RedBlackNode):
        if parent.color == RedBlackTree.COLOR_BLACK:
            return
        else:
            pParent: RedBlackNode = parent.parent
            uncle:RedBlackNode = self.__getBrother(parent)
            if uncle is not None and uncle.color == RedBlackTree.COLOR_RED and parent.color == RedBlackTree.COLOR_RED:
                uncle.color = RedBlackTree.COLOR_BLACK
                parent.color = RedBlackTree.COLOR_BLACK
                if parent.parent == self.root:
                    parent.parent.color = RedBlackTree.COLOR_BLACK
                else:
                    pParent.color = RedBlackTree.COLOR_RED
                    self.__insertFix(pParent.parent,pParent)
            elif pParent.left is parent:
                if parent.left is newNode:
                    pParent.color = RedBlackTree.COLOR_RED
                    parent.color = RedBlackTree.COLOR_BLACK
                    self.__rotateRight(pParent,parent)
                else:
                    self.__rotateLeft(parent,newNode)
                    pParent.color = RedBlackTree.COLOR_RED
                    newNode.color = RedBlackTree.COLOR_BLACK
                    self.__rotateRight(pParent,newNode)
            else:
                if parent.right is newNode:
                    pParent.color = RedBlackTree.COLOR_RED
                    parent.color = RedBlackTree.COLOR_BLACK
                    self.__rotateLeft(pParent,parent)
                else:
                    self.__rotateRight(parent,newNode)
                    pParent.color = RedBlackTree.COLOR_RED
                    newNode.color = RedBlackTree.COLOR_BLACK
                    self.__rotateLeft(pParent,newNode)
    def __findInsert(self,node : RedBlackNode,val):
        if node > val:
            if node.left is None:
                return node
            else:
                return self.__findInsert(node.left,val)
        elif node < val:
            if node.right is None:
                return node
            else:
                return self.__findInsert(node.right,val)
        else:
            # Do nothing
            return None
    def __getitem__(self,val):
        node = self.__search(self.root,val)
        return node.val if node is not None else None
    def __search(self,node:RedBlackNode,val):
        if node == val:
            return node
        elif node > val:
            if node.left is None:
                return None
            else:
                return self.__search(node.left,val)
        else:
            if node.right is None:
                return None
            else:
                return self.__search(node.right,val)
    def recordNode(self,type,val):
        self.last = str(self)
        self.lasttype = type
        self.lastId = val
    def __checkRules(self):
        print(1)
        if self.root is not None:
            self.__assertParentPt(self.root)
        assert(self.root is None or self.root.color == RedBlackTree.COLOR_BLACK)
        self.__checkNode(self.root)
    def __checkNode(self,node:RedBlackNode):
        if node is None:
            return 1
        else:
            if node.left is not None:
                if node.left.parent is not node:
                    assert (False)
                if node.left.color == RedBlackTree.COLOR_RED and node.color == RedBlackTree.COLOR_RED:
                    assert(False)
            if node.right is not None:
                if node.right.parent is not node:
                    assert(False)
                if node.right.color == RedBlackTree.COLOR_RED and node.color == RedBlackTree.COLOR_RED:
                    assert(False)
            if node.left is node.right and node.left is not None:
                assert(False)
            resultL = self.__checkNode(node.left)
            resultR = self.__checkNode(node.right)
            if resultL != resultR:
                assert(False)
            if node.color == RedBlackTree.COLOR_BLACK:
                return resultL + 1
            else:
                return resultL
    def __retrieveNext(self,node:RedBlackNode):
        if node.right is None:
            return None
        else:
            cur:RedBlackNode = node.right
            while cur.left is not None:
                cur = cur.left
            return cur
    def __swapContent(self,node1:RedBlackNode,node2:RedBlackNode):
        temp = node1.val
        node1.val = node2.val
        node2.val = temp
    def __fixAfterDelete(self,node:RedBlackNode,delnode:RedBlackNode):
        if node.color == RedBlackTree.COLOR_RED:
            node.color = delnode.color
            return
        elif node.parent is None:
            return
        else:
            parent:RedBlackNode = node.parent
            if parent.left is node:
                brother : RedBlackNode = self.__getBrother(node)
                if brother.color == RedBlackTree.COLOR_RED:
                    parent.color = RedBlackTree.COLOR_RED
                    brother.color = RedBlackTree.COLOR_BLACK
                    self.__rotateLeft(parent,brother)
                    self.__fixAfterDelete(node,node)
                elif brother.right is not None and brother.right.color == RedBlackTree.COLOR_RED:
                    #兄弟节点的右子节点为红
                    brother.color = parent.color
                    parent.color = RedBlackTree.COLOR_BLACK
                    brother.right.color = RedBlackTree.COLOR_BLACK
                    self.__rotateLeft(parent,brother)
                elif brother.left is not None and brother.left.color == RedBlackTree.COLOR_RED:
                    brother.color = RedBlackTree.COLOR_RED
                    brother.left.color = RedBlackTree.COLOR_BLACK
                    self.__rotateRight(brother,brother.left)
                    self.__fixAfterDelete(node,node)
                else:
                    brother.color = RedBlackTree.COLOR_RED
                    self.__fixAfterDelete(parent,node)
            else:
                brother:RedBlackNode = self.__getBrother(node)
                if brother.color == RedBlackTree.COLOR_RED:
                    parent.color = RedBlackTree.COLOR_RED
                    brother.color = RedBlackTree.COLOR_BLACK
                    self.__rotateRight(parent,brother)
                    self.__fixAfterDelete(node,node)
                elif brother.left is not None and brother.left.color == RedBlackTree.COLOR_RED:
                    brother.color = parent.color
                    parent.color = RedBlackTree.COLOR_BLACK
                    brother.left.color = RedBlackTree.COLOR_BLACK
                    self.__rotateRight(parent,brother)
                elif brother.right is not None and brother.right.color == RedBlackTree.COLOR_RED:
                    brother.color = RedBlackTree.COLOR_RED
                    brother.right.color = RedBlackTree.COLOR_BLACK
                    self.__rotateLeft(brother,brother.right)
                    self.__fixAfterDelete(node,node)
                else:
                    brother.color = RedBlackTree.COLOR_RED
                    self.__fixAfterDelete(parent,node)
    '''
    def __prepareReplaceNode2(self,node:RedBlackNode):
        if node.left is None and node.right is None:
            return node
        if node.left is None and node.right is not None:
            if node.color == RedBlackTree.COLOR_RED:
                return node
            else:
                self.__swapContent(node,node.right)
                return self.__prepareReplaceNode(node.right)
        if node.right is None and node.left is not None:
            if node.color == RedBlackTree.COLOR_RED:
                return node
            else:
                self.__swapContent(node,node.left)
                return self.__prepareReplaceNode(node.left)
        nextNode = self.__retrieveNext(node)
        self.__swapContent(node,nextNode)
        return self.__prepareReplaceNode(nextNode)
    '''
    def __prepareReplaceNode(self,node:RedBlackNode):
        if node.left is None and node.right is None:
            return node
        if node.left is None and node.right is not None:
            self.__swapContent(node,node.right)
            return self.__prepareReplaceNode(node.right)
        if node.right is None and node.left is not None:
            self.__swapContent(node,node.left)
            return self.__prepareReplaceNode(node.left)
        nextNode = self.__retrieveNext(node)
        self.__swapContent(node,nextNode)
        return self.__prepareReplaceNode(nextNode)
    def __delVal(self, val):
        delNode: RedBlackNode = self.__search(self.root, val)
        if delNode is None:
            return
        else:
            repNode: RedBlackNode = self.__prepareReplaceNode(delNode)
            self.__fixAfterDelete(repNode, repNode)
            if repNode.parent is None:
                self.root = None
            elif repNode.parent.left is repNode:
                repNode.parent.left = None
                repNode.parent = None
            else:
                repNode.parent.right = None
                repNode.parent = None
        if __debug__:
            self.__checkRules()
    '''
    def __delVal2(self,val):
        delNode:RedBlackNode = self.__search(self.root,val)
        if delNode is None:
            return
        else:
            repNode: RedBlackNode = self.__prepareReplaceNode(delNode)
            if repNode.color == RedBlackTree.COLOR_RED:
                if repNode.left is None and repNode.right is not None:
                    if repNode.parent is None:
                        self.root = repNode.right
                        self.root.color = RedBlackTree.COLOR_BLACK
                    else:
                        isLeft = repNode.parent.left is repNode
                        if isLeft:
                            repNode.parent.left = repNode.right
                            repNode.right.parent = repNode.parent
                        else:
                            repNode.parent.right = repNode.right
                            repNode.right.parent = repNode.parent
                        repNode.parent = None
                elif repNode.right is None and repNode.left is not None:
                    if repNode.parent is None:
                        self.root = repNode.left
                        self.root.color = RedBlackTree.COLOR_BLACK
                    else:
                        isLeft = repNode.parent.left is repNode
                        if isLeft:
                            repNode.parent.left = repNode.left
                            repNode.left.parent = repNode.parent
                        else:
                            repNode.parent.right = repNode.left
                            repNode.left.parent = repNode.parent
                        repNode.parent = None
                else:
                    if repNode.parent is None:
                        self.root = repNode.left
                        self.root.color = RedBlackTree.COLOR_BLACK
                    else:
                        isLeft = repNode.parent.left is repNode
                        if isLeft:
                            repNode.parent.left = repNode.left
                        else:
                            repNode.parent.right = repNode.left
                        repNode.parent = None
            else:
                self.__fixAfterDelete(repNode,repNode)
                if repNode.parent is None:
                    self.root = None
                elif repNode.parent.left is repNode:
                    repNode.parent.left = None
                    repNode.parent = None
                else:
                    repNode.parent.right = None
                    repNode.parent = None
        if __debug__:
            self.__checkRules()
    '''
    def __str__(self):
        return self.__dotFile()
    def __len__(self):
        if self.root is None:
            return 0
        return self._lennode(self.root)
    def _lennode(self,node:RedBlackNode):
        if node is None:
            return 0
        return self._lennode(node.left) + self._lennode(node.right) + 1
rbTree = RedBlackTree()
iter = 0
lst = []
for i in range(1000):
    addedV = int(i)
    rbTree += addedV
    lst.append(addedV)
time1 = time.time()
for i in range(10000):
    if random.random() > 0.5:
        if len(lst) > 0:
            val = lst[int(random.random() * len(lst))]
            rbTree.recordNode("DEL",val)
            try:
                before = len(rbTree)
                rbTree -= val
                lst.remove(val)
                end = len(rbTree)
                assert(end == before + 1)
            except (AssertionError,TypeError) as e:
                print(rbTree.last)
                print(rbTree.lasttype)
                print(rbTree.lastId)
                print(rbTree)
                raise e

    else:
        addedV = int(random.random() * 10000)
        rbTree.recordNode("ADD", addedV)
        try:
            rbTree += addedV
            if addedV not in lst:
                lst.append(addedV)
        except  (AssertionError,TypeError) as e:
            print(rbTree.last)
            print(rbTree.lasttype)
            print(rbTree.lastId)
            print(rbTree)
            raise e
time2 = time.time()
print(time2 - time1)
print(rbTree)
#print(solution.Match("abcbc","a(bc)*.*"))