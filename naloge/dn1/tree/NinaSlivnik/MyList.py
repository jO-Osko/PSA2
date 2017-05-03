from random import randint
from ..AbstractTree import AbstractTree

class MyList:
    def __init__(self, value, right):
        self.value = value
        self.right = right

    def __str__(self):
        if self.right == None:
            return str(self.value) + ':' + '#'
        else:
            return str(self.value) + ':' + self.right.__str__()

    def search(self, x):
        if self.right == None:
            return False
        elif self.right.value == x:
            return True
        elif self.right.value > x:
            return False
        else:
            return self.right.search(x)
    
    def insert(self, x):
        if self.right == None:
            self.right = MyList(x,None)
            if randint(0,1) == 1:
                return self.right
            else:
                return None
        elif self.right.value == x:
            return None
        elif self.right.value > x:
            self.right = MyList(x,self.right)
            if randint(0,1) == 1:
                return self.right
            else:
                return None
        else:
            return self.right.insert(x)

    def remove(self, x):
        if self.right == None:
            return self
        elif self.right.value == x:
            self.right = self.right.right
            return self
        elif self.right.value > x:
            return self
        else:
            self.right = self.right.remove(x)
            return self

class MySkipList:    
    def __init__(self, value, right, down):
        self.value = value
        self.right = right
        self.down = down

    def __str__(self):
        string = ''
        node = self
        while node != None:
            string = string + str(node.value) + ':'
            node = node.right
        string = string + '#'
        if self.down != None:
            string = string + '\n' + self.down.__str__()
        return string

    def search(self, x):
        if self.right == None:
            return self.down.search(x)
        elif self.right.value == x:
            return True
        elif self.right.value > x:
            return self.down.search(x)
        else:
            return self.right.search(x)
    
    def insert(self, x):
        if self.right == None:
            y = self.down.insert(x)
            if y != None:
                self.right = MySkipList(y.value,None,y)
                if randint(0,1) == 1:
                    return self.right
                else:
                    return None
            else:
                return None
        elif self.right.value == x:
            return None
        elif self.right.value > x:
            y = self.down.insert(x)
            if y != None:
                self.right = MySkipList(y.value,self.right,y)
                if randint(0,1) == 1:
                    return self.right
                else:
                    return None
            else:
                return None
        else:
            return self.right.insert(x)

    def remove(self, x):
        if self.right == None:
            return self.down.remove(x)
        elif self.right.value == x:
            self.right = self.right.right
            return self.down.remove(x)
        elif self.right.value > x:
            return self.down.remove(x)
        else:
            return self.right.remove(x)

class SkipList(AbstractTree):
    def __init__(self):
        self.list = MySkipList(None, None, MyList(None,None))
        
    def __str__(self):
        return self.list.__str__()

    def search(self, x):
        return self.list.search(x)

    def insert(self, x):
        y = self.list.insert(x)
        if y != None:
            self.list = MySkipList(None,MySkipList(y.value,None,y),self.list)
        return self

    def remove(self, x):
        self.list.remove(x)
        if self.list.right == None and type(self.list) != MyList:
            self.list = self.list.down
        return self



        
