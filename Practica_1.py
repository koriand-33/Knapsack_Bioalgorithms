import random


MAXCAP = 30
POBLACION = 10
GENERACIONES = 50
PROBABILIDAD_CRUCE = 0.85
PROBABILIDAD_MUTACION = 0.1
N_COMBINACIONES = 5  


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
    individuo = [0] * len(productos)  

    # Asegura que haya al menos 3 Love Potions y 2 Skiving Snackboxes
    individuo[1] = 3  # Love Potions
    individuo[3] = 2  # Skiving Snackboxes
    
    # Rellena el resto aleatoriamente (puede ser 0 o 1)
    for i in range(len(productos)):
        if i != 1 and i != 3:  # No afectar los índices de Love Potions y Snackboxes
            individuo[i] = random.randint(0, 1)

    return individuo

# Función para evaluar un individuo
def evaluar_individuo(individuo):
    peso_total = sum(individuo[i] * productos[i].peso for i in range(len(productos)))
    valor_total = sum(individuo[i] * (productos[i].precio or 0) for i in range(len(productos)))

    count_love_potion = sum(individuo[i] for i in range(len(productos)) if productos[i].nombre == "Love Potion")
    count_skiving_snackbox = sum(individuo[i] for i in range(len(productos)) if productos[i].nombre == "Skiving Snackbox")

    if peso_total > MAXCAP:
        return 0, False  # Peso excedido, individuo no válido

    if count_love_potion < 3 or count_skiving_snackbox < 2:
        return 0, False  # Individuo inválido, pocas Love Potions o Snackboxes

    return valor_total, True  

def generar_poblacion(tamano):
    return [generar_individuo() for _ in range(tamano)]

def seleccionar_padres(poblacion):
    fitness_totales = [evaluar_individuo(individuo)[0] for individuo in poblacion]
    suma_fitness = sum(fitness_totales)
    seleccionados = []

    for _ in range(2):
        punto_ruleta = random.uniform(0, suma_fitness)
        acumulado = 0

        for i, fitness in enumerate(fitness_totales):
            acumulado += fitness
            if acumulado >= punto_ruleta:
                seleccionados.append(poblacion[i])
                break

    return seleccionados

def cruzar(padre1, padre2):
    hijo1 = []
    hijo2 = []
    
    for i in range(len(productos)):
        if random.random() < 0.5:  # Umbral de 50%
            hijo1.append(padre1[i])  # Hereda del padre 1
            hijo2.append(padre2[i])  # Hereda del padre 2
        else:
            hijo1.append(padre2[i])  # Hereda del padre 2
            hijo2.append(padre1[i])  # Hereda del padre 1
    
    return hijo1, hijo2

def mutar(individuo):
    for i in range(len(individuo)):
        if random.random() < PROBABILIDAD_MUTACION:
            individuo[i] = 1 - individuo[i]  

def main():
    mejor_combinacion_global = None
    mejor_valor_global = 0

    for n in range(N_COMBINACIONES): 
        print(f"\nEvaluando combinación {n + 1}:")
        poblacion = generar_poblacion(POBLACION)

        for _ in range(GENERACIONES):
            nueva_poblacion = []
            for _ in range(POBLACION // 2):
                padre1, padre2 = seleccionar_padres(poblacion)

                if random.random() < PROBABILIDAD_CRUCE:
                    hijo1, hijo2 = cruzar(padre1, padre2)
                else:
                    hijo1, hijo2 = padre1, padre2
                
                mutar(hijo1)
                mutar(hijo2)
                nueva_poblacion.extend([hijo1, hijo2])
            
            poblacion = nueva_poblacion

        mejor_individuo = max(poblacion, key=lambda ind: evaluar_individuo(ind)[0])
        valor_mejor, valido = evaluar_individuo(mejor_individuo)

        if valido:
            print("Mejor individuo:", mejor_individuo)
            print("Valor máximo:", valor_mejor)

          #Pruebaaa
            print("\nCombinación ideal para llevar en la mochila:")
            total_peso = 0
            total_valor = 0

            for i in range(len(mejor_individuo)):
                if mejor_individuo[i] > 0:  
                    cantidad = mejor_individuo[i]
                    print(f"{productos[i].nombre}: {cantidad} unidades (Peso: {productos[i].peso}, Valor: {productos[i].precio})")
                    total_peso += cantidad * productos[i].peso
                    total_valor += cantidad * (productos[i].precio or 0)

            print(f"Peso total: {total_peso} / {MAXCAP}, Valor total: {total_valor}\n")

            # Actualizar la mejor combinación global
            if valor_mejor > mejor_valor_global:
                mejor_valor_global = valor_mejor
                mejor_combinacion_global = mejor_individuo

    # Imprimir la mejor combinación global al final
    if mejor_combinacion_global:
        print("\nMejor combinación global encontrada:")
        total_peso_global = sum(mejor_combinacion_global[i] * productos[i].peso for i in range(len(productos)))
        total_valor_global = sum(mejor_combinacion_global[i] * (productos[i].precio or 0) for i in range(len(productos)))

        for i in range(len(mejor_combinacion_global)):
            if mejor_combinacion_global[i] > 0:
                print(f"{productos[i].nombre}: {mejor_combinacion_global[i]} unidades (Peso: {productos[i].peso}, Valor: {productos[i].precio})")

        print(f"Peso total: {total_peso_global} / {MAXCAP}, Valor total: {total_valor_global}")

if __name__ == "__main__":
    main()
