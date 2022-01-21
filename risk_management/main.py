import numpy as np

def empirical_VaR(X, p, R0=1):
    L = -np.array(X)/R0
    L[::-1].sort()
    print(L)
    n = L.shape[0]

    return L[int(n*p)]

def empirical_ES(X, p, R0=1):
    L = -np.array(X)/R0
    L[::-1].sort()
    print(L)
    n = L.shape[0]
    
    return (1/p)*(L[:int(n*p - 1)].sum()/n + ( p - int(n*p)/n )*L[int(n*p)]) 

if __name__== '__main__':
    X = np.random.randint(100, size=(100))
    p = 0.05

    eVaR = empirical_VaR(X, p)
    print(eVaR)

    eES = empirical_ES(X, p)
    print(eES)
