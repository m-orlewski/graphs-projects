from random import sample,random
from src.adj_list import AdjList

def gen_n_l(n,l):
    if n<2 or l<0 or l>(n*(n-1))/2 :
        raise
    edges=[(i,j) for i in range(1,n+1) for j in range(i+1,n+1)] #lista wszyskich możliwych krawendzi
    edges=sample(edges,l) #wybranie losowo danej liczby krawedzi
    adlist={i:[] for i in range(1,n+1)}  #Stworzenie słownika pod raprezentacje adj_list
    for e in edges: #Dodanie wylosowanych krawedzi do reprezentacji
        adlist[e[0]].append(e[1])
        adlist[e[1]].append(e[0])
    print(adlist)
    return adlist

def gen_n_p(n,p):
    if n<2 or p<0 or p>1 :
        raise
    adlist={i:[] for i in range(1,n+1)} #Stworzenie słownika pod raprezentacje adj_list
    for i in range(1,n+1): #Przejsie po wszystch możliwych wierzchołkach
        for j in range(i+1,n+1): #Przejscie po wszystkich możliwych krawedzich
            if random() < p: #Losowe wybranie zależne od prawdopodobieństwa czy dodać krawedz do reprezentacji
                adlist[i].append(j)
                adlist[j].append(i)
    return adlist