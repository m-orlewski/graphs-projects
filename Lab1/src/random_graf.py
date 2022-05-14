from random import sample,random

def gen_n_l(n,l):
    n=int(n)
    l=int(l)
    edges=[(i,j) for i in range(1,n+1) for j in range(i+1,n+1)]
    print(len(edges))
    edges=sample(edges,l)
    adlist={i:[] for i in range(1,n+1)}
    for e in edges:
        adlist[e[0]].append(e[1])
        adlist[e[1]].append(e[0])
    return adlist

def gen_n_p(n,p):
    n=int(n)
    p=float(p)

    adlist={i:[] for i in range(1,n+1)}
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            if random() < p:
                adlist[i].append(j)
                adlist[j].append(i)
    return adlist