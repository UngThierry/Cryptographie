from prime import is_probable_prime
from math import sqrt
import random


#Exercice 1
#Q1

def pgcd(a, b):
    """
    Retourne le pgcd de a et b
    @param a : entier positif, b : entier positif
    @return: pgcd de a et b
    """
    while(b!=0):
        r = a%b
        a = b
        b = r
    return a

def bezout(a, b):
    """
    Retourne le pgcd et les 2 coefficient de Bezout de a et b
    @param a, b
    @return: res
    """
    r0 = a
    r1 = b 
    u0 = 0
    u1 = 1-u0
    v0 = 1
    v1 = int(-r0/r1)              
    
    res = [r1, u0, v0]            
    while(r0%r1):                   
        r = r0                      
        r0 = r1     
        r1 = r%r1                
        u = u0     
        v = v0 
        u0 = u1 
        v0 = v1 
        q = int(r0/r1)        
        u1 = u-q*u1 
        v1 = v-q*v1 
        
        res = [r1, u0, v0] 
    return res

#Q2

def inv_mod(a, n):
    """
    Retourne l'inverse de a dans Z/nZ
    @param a, n : groupe Z/nZ
    @return inverse de a dans Z/nZ
    """
    (r, u, v ) = bezout(a, n)
    if(r==1):                  
        return u%n
    else:
        return False

def invertibles(N):
    """
    Retourne la liste des elements inversibles dans Z/nZ
    @param N : groupe Z/NZ
    @return res
    """
    res = list()
    for i in range(N):
        if(inv_mod(i, N)!=False):
            res.append(i)
    return res  

#Q3
def phi(N):
    """
    Retourne le nombre d'entier inferieur a N et permier avec N
    @param N : entier positif
    @return res
    """
    res = 0
    for i in range(N):
        if(pgcd(i, N)==1):
            res += 1
    return res


#Exercice 2
#Q1
def exp(a, n, p):
    """
    Retourne le resultat de a^n dans le groupe Z/pZ
    @param a, n : puissance entier positif, p : groupe Z/pZ
    @return res
    """
    res = 1
    while(n!=0): 
        if(n%2==1):    
            res = (res*a)%p
            n = n-1
        else:          
            a = (a*a)%p
            n = n/2
    return res

#Q2
def factor(n):
    """
    Retourne la liste des couples (p, v_p) pour tous les facteurs 
    premiers p avec v_p la valuation p-adique associée
    @param n
    @return fact
    """
    div = 2
    fact = list()
    while(n!=1):
        i = 0
        while(n%div==0):
            n = n//div
            i += 1
        if(i!=0):
            fact.append((div, i))
        div += 1        
    return fact


#Q3
def getFactors(a):
    """
    """
    factors = list()
    for i in range(1,a+1):
        if a%i == 0:
            factors.append(i)
    return factors

def order(a, p, factors_p_minus1):
    """
    """
    if a == 1:
        return 1
    for i in getFactors(p-1):
        if exp(a,i,p) == 1:
            return i

#Q4
def find_generator(p, factors_p_minus1):
    """
    """
    liste = []
    for a in range(1,p):
        if order(a,p,factors_p_minus1) == p-1:
            liste.append(a)
    return liste


#Q5
def generate_safe_prime(k):
    return


#Q6
def bsgs(n, g, p):
    return


#Q8
def next(x,a,b,n,h,p):
    """
    """
    if(x%3==2):
        x = x*x%p
        a = a*2%p
        b = b*2%p
    elif(x%3==1):
        x = x*n%p
        a = a%p
        b = (b+1)%p
    elif(x%3==0):
        x = x*h%p
        a = (a+1)%p
        b = b%p 
    return (x,a,b)

#Q9
def rho_pollard(n, h, q, p):
    return
