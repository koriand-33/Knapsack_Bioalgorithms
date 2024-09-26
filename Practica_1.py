import random

# Configuración
CAPACIDAD = 30
POBLACION = 10
GENERACIONES = 50
PROBABILIDAD_CRUCE = 0.85
PROBABILIDAD_MUTACION = 0.1

# Items
peso = [4, 2, 5, 5, 2, 1.5, 1]
costo = [10, 8, 12, 6, 3, 2, 2]
restriction = [0, 3, 0, 2, 0, 0, 0]
n = len(peso)

# Funciones

# Validar que el cromosoma no exceda el peso máximo permitido
def evaluar_individuo(individuo):
    peso_total = sum(individuo[i] * peso[i] for i in range(n))
    return peso_total <= CAPACIDAD

# Generar un cromosoma válido
def generar_individuo():
    individuo = [random.randint(restriction[i], 10) for i in range(n)]
    while not evaluar_individuo(individuo):
        individuo = [random.randint(restriction[i], 10) for i in range(n)]
    return individuo

# Generar la población inicial
def generar_poblacion():
    poblacion = [generar_individuo() for _ in range(POBLACION)]
    return poblacion

# Evaluar el valor total de un individuo
def valor_total(individuo):
    return sum(individuo[i] * costo[i] for i in range(n))

# Obtener las probabilidades acumuladas (ruleta)
def obtener_probabilidades_acumuladas(poblacion):
    valores_totales = [valor_total(individuo) for individuo in poblacion]
    suma_total = sum(valores_totales)
    probabilidades = [v / suma_total for v in valores_totales]
    
    acumulado = 0
    probabilidades_acumuladas = []
    for prob in probabilidades:
        acumulado += prob
        probabilidades_acumuladas.append(acumulado)
    
    return probabilidades_acumuladas

# Selección de padres usando ruleta
def seleccionar_padres(probabilidades_acumuladas):
    def seleccionar():
        r = random.uniform(0, 1)
        for i, prob in enumerate(probabilidades_acumuladas):
            if r < prob:
                return i 
        return len(probabilidades_acumuladas) - 1

    padre1 = seleccionar()
    padre2 = seleccionar()
    while padre1 == padre2:
        padre2 = seleccionar()

    return padre1, padre2

# Cruce entre dos individuos
def cruzar(padre1, padre2):
    hijo1, hijo2 = padre1[:], padre2[:]
    if random.random() < PROBABILIDAD_CRUCE:
        punto_cruce = random.randint(1, n - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    
    return hijo1, hijo2

# Mutar un individuo
def mutar(individuo):
    for i in range(n):
        if random.random() < PROBABILIDAD_MUTACION:
            individuo[i] = random.randint(restriction[i], 10)
    
    while not evaluar_individuo(individuo):
        individuo = [random.randint(restriction[i], 10) for i in range(n)]
    
    return individuo

# Función principal
def main():
    mejores_combinaciones = []

    poblacion = generar_poblacion()

    for generacion in range(GENERACIONES):
        probabilidades_acumuladas = obtener_probabilidades_acumuladas(poblacion)
        nueva_poblacion = []

        for _ in range(POBLACION // 2):
            # Selección de padres
            idx_padre1, idx_padre2 = seleccionar_padres(probabilidades_acumuladas)
            padre1 = poblacion[idx_padre1]
            padre2 = poblacion[idx_padre2]

            # Cruce
            hijo1, hijo2 = cruzar(padre1, padre2)

            # Mutación
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)

            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion

        # Almacenar las combinaciones actuales
        for individuo in poblacion:
            valor = valor_total(individuo)
            peso_total = sum(individuo[j] * peso[j] for j in range(n))
            mejores_combinaciones.append((individuo, valor, peso_total))

    # Ordenar las combinaciones por el valor total
    mejores_combinaciones.sort(key=lambda x: x[1], reverse=True)

    # Imprimir las 5 mejores combinaciones
    print("\nLas 5 mejores combinaciones:")
    for i in range(5):
        individuo, valor, peso_total = mejores_combinaciones[i]
        print(f"Combinación {i + 1}: {individuo}, Valor: {valor}, Peso: {peso_total}")

if __name__ == "__main__":
    main()
