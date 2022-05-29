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

randutils::mt19937_rng rng;

using pointType = std::tuple<int, int>;
using pathType = std::vector<pointType>;

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

void printPath(const pathType& path){
    for(pointType point : path){
        std::cout << "X: " << std::get<0>(point) << " Y: " << std::get<1>(point) << std::endl;
    }
}

void printPathSimple(const pathType& path){
    for(pointType point : path){
        std::cout << std::get<0>(point) << " " << std::get<1>(point) << std::endl;
    }
}

std::array<int, 2> pickRandomEdges(int pointCount){
    std::array<int, 2> ans;

    ans[0] = rng.uniform(0,pointCount-1);

    std::array<int, 3> forbidden = {ans[0]-1, ans[0], ans[0]+1};

    if(forbidden[0] == -1)
        forbidden[0] = pointCount-1;
    if(forbidden[2] == pointCount)
        forbidden[2] = 0;

    do{
        ans[1] = rng.uniform(0, pointCount-1);
    } while ((ans[1] == forbidden[0]) || (ans[1] == forbidden[1]) || (ans[1] == forbidden[2]));

    return ans;
}

void swapEdges(std::array<int, 2> edges, pathType& path){
    
    if(edges[0]==path.size()-1){
        std::swap(path[0], path[edges[1]]);
        return;
    }

    std::swap(path[edges[0]+1], path[edges[1]]);
}

double pathLength(pathType& path){
    double totalLength = 0;
    int x = std::get<0>(path[0]);
    int y = std::get<1>(path[0]);
    for(int i=1; i<path.size(); i++){
        totalLength += sqrt(pow(std::get<0>(path[i]) - x,2) + pow(std::get<1>(path[i]) - y, 2));
        // std::cout<<"x= "<<x<<" y= "<<y<<std::endl;
        x = std::get<0>(path[i]);
        y = std::get<1>(path[i]);
    }
    totalLength += sqrt(pow(std::get<0>(path[0]) - x,2) + pow(std::get<1>(path[0]) - y, 2));

    return totalLength;
}

void simulatedAnnealing(pathType& path){
    double T;
    double d = pathLength(path);
    
    for(int i = 100; i>=1; i--){
        T = 0.001*i*i;
        // T = pow(0.001*i,2);
        std::cout<<"I="<<i<<std::endl;
        for(int it = 0; it<MAX_IT; it++){
            // std::cout<<path.size();
            auto picked = pickRandomEdges(path.size());
            // std::cout<<"Will swap "<<picked[0]<<" and "<<picked[1]<<std::endl;
            pathType newPath = pathType(path);
            swapEdges(picked, newPath);
            double dNew = pathLength(newPath);
            if(dNew < d){
                path = newPath;
                d = dNew;
            }
            else{
                double r = rng.uniform(0., 1.);
                // std::cout<<"old="<<d<<" new="<<dNew<<std::endl;
                double f = -1.0*(dNew-d)/T;
                double exponent = exp(f);
                // std::cout<<"R="<<r<<" f="<<f<<" exp="<<exponent<<std::endl;
                if(r<exponent){
                    path = newPath;
                    d = dNew;
                }
            }
        }
        std::cout<<"d="<<d<<std::endl;
    }
}

int main(){
    auto path = readFromFile("input_150.dat");
    // double len1 = pathLength(path);
    // printPathSimple(path);

    // std::array<int, 2> testEdges = {1, 3};
    // swapEdges(testEdges, path);
    // std::cout<<"\n\n\n";
    // double len2 = pathLength(path);
    // printPathSimple(path);
    
    // std::cout<<len1<<" "<<len2<<std::endl;

    simulatedAnnealing(path);


    printPathSimple(path);

    // for(int i=0; i<30; i++){
    //     auto edges = pickRandomEdges(10);
    //     std::cout<<edges[0]<<" "<<edges[1]<<std::endl;
    // }
    return 0;
}