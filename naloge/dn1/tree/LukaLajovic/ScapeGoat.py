#from AbstractTree import *
from ..AbstractTree import AbstractTree

__author__ = "luka lajovic"


alfa=0.7

class Node:
    def __init__(self, key = None):
        self.key = key
   

class ScapeGoat(AbstractTree):
    def __init__(self,data=None,levo=None,desno=None):
        if data is None:
            self.prazno=True
        else:
            self.prazno=False
            self.data=data
            self.levo = self.__class__() if levo is None else levo
            self.desno = self.__class__() if desno is None else desno

    def dodaj(self,element):
        if self.prazno==True:
            self.prazno=False
            self.data=element
            self.levo=ScapeGoat()
            self.desno=ScapeGoat()
            return []
            
        else:
            if self.data<element:
                return [self]+self.desno.dodaj(element)
                
            else:
                return [self]+self.levo.dodaj(element)
    def insert(self,element):
        sez=self.dodaj(element)
        #self.levo.velikost()<=alfa*self.velikost():
        
        if len(sez)>1:
            u=len(sez)-2
            l=0
            d=0
            izb=sez[len(sez)-1].data
            while u>-1:
                if sez[u].data<izb:
                    l=sez[u].levo.size()
                    
                else:
                    d=sez[u].desno.size()
                    
                if l>alfa*(l+d+1):
                    sez[u].sestavi()
                    break
                if d>alfa*(l+d+1):
                    sez[u].sestavi()
                    break
                if sez[u].data<izb:
                    d=d+l+1
                    
                else:
                    l=d+l+1
                    
                izb=sez[u].data
                u-=1
            
    #vrne vrednost predhodnika in ga zbrise
    
    def najbolj_desni(self):
        if self.desno.prazno==True:
            return self
        else:
            return self.desno.najbolj_desni()

    def remove(self,element):
        if self.prazno==True:
            pass
        else:
            if self.data<element:
                self.desno.remove(element)
            else:
                if self.data>element:
                    self.levo.remove(element)
                else:                    
                    if self.levo.prazno==True and self.desno.prazno==True:                        
                        self.prazno=True
                        self.levo=None
                        self.desno=None
                    else:
                        if self.levo.prazno==True:
                            self.data=self.desno.data
                            self.levo = self.desno.levo
                            self.desno = self.desno.desno
                        else:
                            if self.desno.prazno==True:
                                self.data=self.levo.data
                                self.desno=self.levo.desno
                                self.levo=self.levo.levo
                            else:
                                nd=self.levo.najbolj_desni()
                                self.data=nd.data
                                nd.data=element
                                nd.remove(element)
                                

    def in_order_traversal(self):
        if self.prazno==True:
            return []
        else:
            return self.levo.in_order_traversal()+[self.data]+self.desno.in_order_traversal()
        
    def size(self):
        if self.prazno==True:
            return 0
        else:
            return 1+self.levo.size()+self.desno.size()

#    def uravnotezi(self):
#        zap=self.in_order_traversal()
#        novo=ScapeGoat()
#        med=len(zap)//2
#        novo.dodaj(zap[med])
#        l=zap[:med][::-1]
#        d=zap[med+1:]
#        if len(zap)%2==1:
#            for i in range(len(d)):
#                novo.dodaj(l[i])
#                novo.dodaj(d[i])
#        else:
#            for i in range(len(d)):
#                novo.dodaj(l[i])
#                novo.dodaj(d[i])
#            novo.dodaj(l[len(l)-1])
#        return novo
            

                    
                




    def ustvari(self,zap):
        if len(zap)>0:
            m=len(zap)//2
            med=zap[m]
            self.data=med
            if self.prazno==True:
                self.prazno=False
                self.data=med
                self.levo=ScapeGoat()
                self.desno=ScapeGoat()
            
                self.levo.ustvari(zap[:m])
                self.desno.ustvari(zap[m+1:])
            else:
                self.data=med

            
                self.levo.ustvari(zap[:m])
                self.desno.ustvari(zap[m+1:])
        else:
            self.data=None
            self.levo=None
            self.desno=None
            self.prazno=True
                
    #nase drevo sestavi na novo
    #kot uravnoveseno
    def sestavi(self):
        z=self.in_order_traversal()
        self.ustvari(z)
        
               



    
    def kordinate(self,zacx=400,zacy=50,n=200):
        if self.prazno==True:
            return []
        else:
            moja=[zacx,zacy,self.data]
            if self.levo.prazno==True:
                moja+=[False]
            else:
                moja+=[True]                            
            if self.desno.prazno==True:
                moja+=[False]
            else:
                moja+=[True]
            moja+=[n]
            return [moja]+self.levo.kordinate(zacx-n,zacy+100,n/2)+self.desno.kordinate(zacx+n,zacy+100,n/2)



      
