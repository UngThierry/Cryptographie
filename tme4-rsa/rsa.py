import random
import time

### Generation de premiers

def is_probable_prime(N, nbases=20):
    """
    True if N is a strong pseudoprime for nbases random bases b < N.
    Uses the Miller--Rabin primality test.
    """

    def miller(a, n):
        """
        Returns True if a proves that n is composite, False if n is probably prime in base n
        """

        def decompose(i, k=0):
            """
            decompose(n) returns (s,d) st. n = 2**s * d, d odd
            """
            if i % 2 == 0:
                return decompose(i // 2, k + 1)
            else:
                return (k, i)

        (s, d) = decompose(n - 1)
        x = pow(a, d, n)
        if (x == 1) or (x == n - 1):
            return False
        while s > 1:
            x = pow(x, 2, n)
            if x == n - 1:
                return False
            s -= 1
        return True

    if N == 2:
        return True
    for i in range(nbases):
        import random
        a = random.randint(2, N - 1)
        if miller(a, N):
            return False
    return True

def random_probable_prime(bits):
    """
    Returns a probable prime number with the given number of bits.
    Remarque : on est sur qu'un premier existe par le postulat de Bertrand
    """
    n = 1 << bits
    import random
    p = random.randint(n, 2 * n - 1)
    while (not (is_probable_prime(p))):
        p = random.randint(n, 2 * n - 1)
    return p

### Fonction TME3

def bezout(a,b):
	"""
	Retourne le pgcd et les 2 coefficient de Bezout de a et b
	@param a,b
	@return res
	"""
	r0 = a
	r1 = b 
	u0 = 0
	u1 = 1-u0
	v0 = 1
	v1 = int(-r0/r1)              
	res = [r1,u0,v0]
		       
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
		res = [r1,u0,v0]
		
	return res
	
def exp(a,n,p):
	"""
	Retourne le resultat de a^n dans le groupe Z/pZ
	@param a, n : puissance entier positif, p : groupe Z/pZ
	@return res
	"""
	res = 1

	while(p>0): 
		if(p%2!=0):    
			res = (res*a)%n     
		a = (a*a)%n
		p = p//2

	return res%n

def inv_mod(a,n):
	"""
	Retourne l'inverse de a dans Z/nZ
	@param a,n : groupe Z/nZ
	@return inverse de a dans Z/nZ
	"""
	(r,u,v) = bezout(a,n)

	if(r==1):                  
		return u%n
	else:
		return False

#Exercice 1
#Q1
def rsa_chiffrement(x,N,e):
	"""
	Retourne le chiffrement de rsa
	@param x : message, N : mod, e : exposant
	@return message_chiffre
	"""
	message_chiffre = exp(x,N,e)
	return message_chiffre

def rsa_dechiffrement(y,p,q,d):
	"""
	Retourne le dechiffrement de rsa
	@param y : message_chiffre, p*q : N, d : inverse de e mod phi(N)
	@return message_dechiffre
	"""
	message_dechiffre = exp(y,p*q,d)
	return message_dechiffre

#Q2
# Retourne s tel que s % n1 == a1 et s % n2 == a2
def crt2(a1,a2,n1,n2):
	"""
	Retourne le theoreme des reste chinois
	@param a1, a2 : entier positif, n1, n2 : entier premier entre eux
	@return n,m
	"""
	x = inv_mod(n1,n2)
	y = inv_mod(n2,n1)
	n = n2*y*a1+a2*x*n1
	m = n2*n1
	return n,m

#Q3
def rsa_dechiffrement_crt (y,p,q,up,uq,dp,dq,N):
	m1 = exp(y,dp,p)
	m2 = exp(y,dq,q)
	h = exp(uq*(m1-m2),p,1)

	return m2+h*q

#Q4

def cryptosystemeRSA(bits):
	p = random_probable_prime(bits)
	q = random_probable_prime(bits)
	phi_n = (p-1)*(q-1)
	e = random.randint(1,phi_n-1)
	pgcd,u,v = bezout(phi_n,e)
	while not pgcd == 1:
		e = random.randint(1,phi_n-1)
		pgcd,u,v = bezout(phi_n,e)
	d = v
	assert((e*d) % phi_n == 1)
	
	return p,q,e,d

taille = [256,512,1024,2048]
T = []

for t in taille:
	start = time.time()
	cryptosystemeRSA(t)
	te = time.time() - start
	T.append(te)
	print(te)

print("Cryptosysteme RSA\n",T)

#Exercice 2
#Q1
#### Wiener
def cfrac(a,b):
	"""
	Retourne la fraction continue de a/b
	@param a,b : entier premier entre eux
	@return Q
	"""
	r, u, v, r1, u1, v1 = a, 1, 0, b, 0, 1
	Q = []
	
	while(r1!=0):
		q = r//r1
		r, u, v, r1, u1, v1 = r1, u1, v1, r-q*r1, u-q*u1, v-q*v1
		Q.append(q)
		
	return Q
    
def reduite(L):
	if(len(L)==1): 
		return L[0], 1
		
	a, b = reduite(L[1:])
	
	return L[0]*a+b, a

#Q2
def Wiener(m,c,N,e):
	"""
	Retourne l'attaque de Wiener
	@param m : message d'origine, c : message chiffré, N, e : clé publique
	@return clé secrète
	"""
	Q = cfrac(e,N)
	i = 1
	
	while(exp(c,N,reduite(Q[:i])[1])!=m):
		i+=1
		
	return reduite(Q[:i])[1]
