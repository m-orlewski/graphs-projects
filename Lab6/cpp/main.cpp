//Zadanie 6.2
#define MAX_IT 10000

#include <iostream>
#include <tuple>
#include <vector>
#include <array>
#include <fstream>
#include <string>
#include <random>
#include <algorithm>
#include <cmath>
#include "randutils.hpp"

randutils::mt19937_rng rng; //generator liczb losowych

using pointType = std::tuple<int, int>;
using pathType = std::vector<pointType>;

//Odczyt z pliku
pathType readFromFile(std::string filename){
    pathType path;
    int currentX;
    int currentY;

    std::ifstream file(filename);

    while(file >> currentX >> currentY){
        path.push_back(std::make_tuple(currentX, currentY));
    }

    file.close();

    return path;
}

//Wypisanie ścieżki na konsolę, wersja z prefixami
void printPath(const pathType& path){
    for(pointType point : path){
        std::cout << "X: " << std::get<0>(point) << " Y: " << std::get<1>(point) << std::endl;
    }
}

//Wypisanie ściezki na konsolę, wersja uproszczona
void printPathSimple(const pathType& path){
    for(pointType point : path){
        std::cout << std::get<0>(point) << " " << std::get<1>(point) << std::endl;
    }
}

//Zapis ścieżki do pliku
void printPathToFile(const pathType& path){
    std::ofstream file("out.dat");
    for(pointType point : path){
        file << std::get<0>(point) << " " << std::get<1>(point) << std::endl;
    }
    file.close();
}

//Funkcja losująca dwie krawędzie które zostaną zamienione
std::array<int, 2> pickRandomEdges(int pointCount){
    std::array<int, 2> ans;

    ans[0] = rng.uniform(0,pointCount-1); //pierwsza krawędź do zamiany

    std::array<int, 3> forbidden = {ans[0]-1, ans[0], ans[0]+1}; //tablica krawędzi których już nie możemy wybrać

    if(forbidden[0] == -1) //poprawa zabronionych gdy wylosowaliśmy zerowy punkt
        forbidden[0] = pointCount-1;
    if(forbidden[2] == pointCount) //poprawa zabronionych gdy wylosowaliśmy ostatni punkt
        forbidden[2] = 0;

    do{
        ans[1] = rng.uniform(0, pointCount-1); //druga krawędź
    } while ((ans[1] == forbidden[0]) || (ans[1] == forbidden[1]) || (ans[1] == forbidden[2])); //musi spełnić warunki

    return ans;
}

//Zamiana krawędzi
void swapEdges(std::array<int, 2> edges, pathType& path){
    
    if(edges[0]==path.size()-1){ //zamiana krawędzi w przypadku gdy wylosowaliśmy ostatni punkt
        std::swap(path[0], path[edges[1]]);
        return;
    }

    std::swap(path[edges[0]+1], path[edges[1]]); //zamiana krawędzi
}

//Obliczanie długości ścieżki
double pathLength(pathType& path){
    double totalLength = 0;
    int x = std::get<0>(path[0]);
    int y = std::get<1>(path[0]);
    for(int i=1; i<path.size(); i++){
        totalLength += sqrt(pow(std::get<0>(path[i]) - x,2) + pow(std::get<1>(path[i]) - y, 2));
        x = std::get<0>(path[i]);
        y = std::get<1>(path[i]);
    }
    totalLength += sqrt(pow(std::get<0>(path[0]) - x,2) + pow(std::get<1>(path[0]) - y, 2));

    return totalLength;
}

// Algorytm symulowanego wyżarzania 
void simulatedAnnealing(pathType& path){
    double T;
    double d = pathLength(path);
    
    for(int i = 100; i>=1; i--){
        T = 0.001*i*i;
        std::cout<<"I="<<i<<std::endl;
        for(int it = 0; it<MAX_IT; it++){
            auto picked = pickRandomEdges(path.size());
            pathType newPath = pathType(path);
            swapEdges(picked, newPath);
            double dNew = pathLength(newPath);
            if(dNew < d){
                path = newPath;
                d = dNew;
            }
            else{
                double r = rng.uniform(0., 1.);
                double f = -1.0*(dNew-d)/T;
                double exponent = exp(f);
                if(r<exponent){
                    path = newPath;
                    d = dNew;
                }
            }
        }
        //std::cout<<"d="<<d<<std::endl;
    }
}

int main(int argc, char* argv[]){
    
    if(argc != 2){
        std::cout<<"Podaj nazwe pliku wejsciowego jako argument"<<std::endl;
        return 0;
    }

    std::string filename = argv[1];

    auto path = readFromFile(filename);
    double len1 = pathLength(path);

    std::cout << "Length before: " << len1 << std::endl;

    simulatedAnnealing(path);

    double len2 = pathLength(path);
    
    std::cout << "Length after: " << len2 << std::endl;

    printPathToFile(path);

    return 0;
}
