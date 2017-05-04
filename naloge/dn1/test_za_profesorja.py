from users import import_helper,trees



from tree.FilipKoprivec.RedBlackTree import RedBlackTree
from tree.EvaErzin.SplayTree import SplayTree
from tree.SamoKralj_234Tree.Tree234 import Tree_234
from tree.ZigaZupancic.BTree import BTree
from tree.KevinStampar.Treap import Treap
from tree.LukaAvbreht.AvlTree import AvlTree
from tree.NinaSlivnik.MyList import SkipList
from tree.Jan_Golob.BplusTree import BplusTree
from tree.LukaLajovic.ScapeGoat import ScapeGoat

print("Drevesa, ki jih lahko uporabljamo")
for tree in trees:
	print("{0} ki ga uporabimo kot tree = {0}()".format(tree[2]))

	

	
	
	
