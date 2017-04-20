from Treap import Treap
import random

def randomSeznam(size):
    seznam=[]
    for i in range(size):
        seznam.append(random.random())
    return seznam

def randomTreap(size):
    seznam=randomSeznam(size)
    izbrisi=randomList(seznam)
    return (Treap(seznam),izbrisi)

def randomList(sez):
    novi=[]
    stevila=[]
    for i in range(len(sez)):
        stevila.append(random.randint(0,len(sez)-1))
    for i in stevila:
            novi.append(sez[i])
    return list(set(novi))
                
def removing(treap,sez):
    i=0
    for x in sez:
        if x in treap:
            treap.remove(x)
            i=i+1
    print('izbrisanih je bilo {i} elementov'.format(i=i))
    print(treap.size())

def inserting(treap,sez):
    i=0
    for x in sez:
        if x not in treap:
            i=i+1
        treap.insert(x)
    print('dodanih je bilo {i} elementov'.format(i=i))
    print(treap.size())

def addremove(treap,sez):
    print("globina drevesa :" + str(treap.depth()))
    removing(treap,sez)
    inserting(treap,sez)
    print("globina drevesa :" + str(treap.depth()))

def testingDepth(times,size):
    for i in range(times):
        (treap,_) = randomTreap(size)
        print(treap.depth())


(a,b)=randomTreap(1000)
addremove(a,b)

