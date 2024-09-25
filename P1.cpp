#include <iostream>
#include <vector>
#include <algorithm>

#define MAXCAP 30
#define poblacion 10
#define generaciones 50
#define probabilidad 0.85
#define probabilidad_mutacion 0.1


using namespace std;
   
   struct Producto{
    string nombre;
    float peso;
    int precio;
   };



int main(){
 
 vector<Producto> productos={
    {"Decoy Detonator",4,10},
    {"Love Potion",2,8},
    {"Extendable Ears",5,12},
    {"Skiving Snackbox",5,6},
    {"Fever Fudge",2,3},
    {"Puking Pastilles",1.5},
    {"Nosebleed Nougat",1,2}
 };


int capacidad=MAXCAP;
 int minLP=3;
 int minSS=2;



    return 0;
}