import random

MAXCAP = 30
POBLACION = 10
GENERACIONES = 50
PROBABILIDAD = 0.85
PROBABILIDAD_MUTACION = 0.1

class Producto:
    def __init__(self, nombre, peso, precio=None):
        self.nombre = nombre
        self.peso = peso
        self.precio = precio

productos = [
    Producto("Decoy Detonator", 4, 10),
    Producto("Love Potion", 2, 8),
    Producto("Extendable Ears", 5, 12),
    Producto("Skiving Snackbox", 5, 6),
    Producto("Fever Fudge", 2, 3),
    Producto("Puking Pastilles", 1.5),
    Producto("Nosebleed Nougat", 1, 2)
]


def generar_individuo():
    return [random.radint(0,1) for _ in range(len(productos))]

def evaluar_individuo(individuo):
    peso_total= sum(individuo[i] * productos[i].peso for i in range(len(productos)))
    valor_total=sum(individuo[i] * (productos[i].precio or 0) for i in range(len(productos)))

    count_love_potion = sum(individuo[i] for i in range(len(productos)) if productos[i].nombre == "Love Potion")
    count_skiving_snackbox = sum(individuo[i] for i in range(len(productos)) if productos[i].nombre == "Skiving Snackbox")

    if peso_total> MAXCAP or count_love_potion > 3 or count_skiving_snackbox > 3:
        return 0
    return valor_total

def generar_poblacion(tamano):
    return [generar_individuo() for _ in range(tamano)]


def seleccionar_padres(poblacion):
    fitness_totales = [evaluar_individuo(individuo) for ind in poblacion]
    suma_fitness= sum(fitness_totales)
    seleccionados=[]

    for _ in range(2):
        punto_ruleta = random.uniform(0,suma_fitness)
        acumulado=0

        for i, fitness in enumerate(fitness_totales):
            acumulado += fitness
            if acumulado>= punto_ruleta:
                seleccionados.append(poblacion[i])
                break

    return seleccionados

def cruzar(padre1, padre2):
    punto_cruce = random.randint(1,len(productos)-1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]

    return hijo1, hijo2

def mutar(individuo):
    for i in range(len(individuo)):
        if random.random()< PROBABILIDAD_MUTACION:
            individuo[i]= 1 - individuo[i]


            

 

     

    
    

    

def main():
    capacidad= MAXCAP
    minLp= 3
    minSS= 2 
    


if __name__ == "__main__":
    main()