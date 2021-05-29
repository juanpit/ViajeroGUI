import random
import math
import matplotlib.pyplot as plt

# Este programa busca implementar una combinacion de algoritmos geneticos y estrategias evolutivas para poder resolver el
# problema del agente viajero.

bandera = 0
ciudades = 10
poblacion = 10 #miu
individuos_nuevos = 5 #lambda 
suma_de_mu_y_lambda = poblacion + individuos_nuevos


lista_ciudades = [0] * ciudades #Lista de las ciudades que vamos a recorrer
lista_poblacion = [0] * suma_de_mu_y_lambda #Lista para guardar la poblacion
lista_fitness = [0] * suma_de_mu_y_lambda #lista que va a guardar los fitness de cada individuo
lista_seleccionados = [0] * poblacion #lista que almacenara los miu seleciconados

lista_graficar_fitness = []
lista_mejor_fitness = []
mejor_fitness = None

r = 0.4 #El porcentaje de lambda que se va a generar por cruza
m = 1-r #El porcentaje de lambda que se va a generar por mutacion (r + m = 1, M es mas importante)

valor_de_cruza = round(r*individuos_nuevos)
valor_de_mutacion = round(m*individuos_nuevos)

#Funcion de prueba para la generacion aleatoria de las ciudades de prueba
for i in range(ciudades):
    lista_ciudades[i] = [0] * 2
    x_ciudad = random.randint(0, 10) #X's
    y_ciudad = random.randint(0, 10) #Y's

    while [x_ciudad,y_ciudad] in lista_ciudades:
        x_ciudad = random.randint(0, 10) #X's
        y_ciudad = random.randint(0, 10) #Y's
    lista_ciudades[i][0] = x_ciudad
    lista_ciudades[i][1] = y_ciudad
    
print('Ciudades a recorrer: ')
print(lista_ciudades)

#Ciclo para generar la lista de listas
for i in range(suma_de_mu_y_lambda):
    lista_poblacion[i] = [-1] * ciudades #se inicializa en -1 por que el cero es parte de los indices 

def generar_poblacion_inicial(): #Funcion que nos va a generar nuestra poblacion inicial

    for i in range(poblacion):
        for j in range(ciudades):
            ci = random.randrange(ciudades)
            #print(ci)
            while ci in lista_poblacion[i]: #while que va validando que no se repitan los valores
                ci = random.randrange(ciudades)         
            lista_poblacion[i][j] = ci 

    print('**************** POBLAICON INICIAL ******************')
    for i in range(poblacion):
        print('h' + str(i) + '  ' + str(lista_poblacion[i]))


#Funcion que recibe un par de coordenadas y nos regresa la distancia euclidiana entre estas
def distancia_euclidiana(x1, y1, x2, y2):
    res = math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
    return res

def calcular_fitness_inicial():
    global lista_poblacion
    valor_a_guardar = 0
    for i in range(poblacion):
        fit = 0
        for j in range(ciudades-1): #Eeste ciclo recorre todo el conjunto de ciudades y se va almacenando en fit
                                            #Basicamente se calcula la distancia entre la ciudad N y N+1
            fit = fit + distancia_euclidiana( lista_ciudades[lista_poblacion[i][j]][0], lista_ciudades[lista_poblacion[i][j]][1], 
                                            lista_ciudades[lista_poblacion[i][j+1]][0], lista_ciudades[lista_poblacion[i][j+1]][1] )
        lista_fitness[i] = fit
        valor_a_guardar = valor_a_guardar + lista_fitness[i]
    
    promedio = valor_a_guardar/poblacion
    lista_graficar_fitness.append(promedio)


def mutacion():
    global lista_poblacion

    for i in range(valor_de_mutacion):
        print('Muta')
        tributo = random.randrange(poblacion) #Sacamos el individuo que va a ser mutado
        lista_poblacion[i+poblacion] = lista_poblacion[tributo].copy() #Lo copiamos en donde va a estar el individuo mutado para trabajar sobre el
        print(tributo)

        #se sacan las 2 ciudades a intercambiar
        ciudad1 = random.randrange(ciudades)
        ciudad2 = random.randrange(ciudades)
        print('Ciudad 1 ' + str(ciudad1))
        print('Ciudad 2 ' + str(ciudad2))
        
        temp = lista_poblacion[i+poblacion][ciudad1] #guardamos la ciudad 1 en la variable temporal para intercambiarla
        lista_poblacion[i+poblacion][ciudad1] = lista_poblacion[i+poblacion][ciudad2] #intercambiamos la ciudad 2 con la 1
        lista_poblacion[i+poblacion][ciudad2] = temp #guardamos la ciudad 1 en donde estaba la 2
        

def cruza():
    global lista_poblacion
    print('Inicia Cruza!!!')

    hijo1 = [-1] * ciudades
    hijo2 = [-1] * ciudades


    for i in range(valor_de_cruza):

        print('Cruza# ' + str(i))
        fit_hijo1=0
        fit_hijo2=0
        tributo1 = random.randrange(poblacion)
        tributo2 = random.randrange(poblacion)
        print('tributo1: ' + str(tributo1))
        print('tributo2: ' + str(tributo2))

        #iniciamos proceso para hijo 1
        hijo1[0] = lista_poblacion[tributo1][0]
        indice = lista_poblacion[tributo2].index(hijo1[0])#indice que se usara para manipular el primer hijo
        #iniciamos proceso para hijo 2
        hijo2[0] = lista_poblacion[tributo2][0]
        indice_h2 = lista_poblacion[tributo1].index(hijo2[0])#indice que se usara para manipular el segundo hijo

        while hijo1[indice] == -1:
            hijo1[indice] = lista_poblacion[tributo1][indice]
            indice2 = lista_poblacion[tributo2].index(hijo1[indice])
            indice = indice2

        while hijo2[indice_h2] == -1:
            hijo2[indice_h2] = lista_poblacion[tributo2][indice_h2]
            indice_2h2 = lista_poblacion[tributo1].index(hijo2[indice_h2])
            indice_h2 = indice_2h2  

        for padre in range(ciudades):
            #print('entro')
            #print(hijo1[padre])
            if hijo1[padre] == -1:
                hijo1[padre] = lista_poblacion[tributo2][padre]

            if hijo2[padre] == -1:
                hijo2[padre] = lista_poblacion[tributo1][padre]
            
        print('HIJO1: ' + str(hijo1))
        print('HIJO2: ' + str(hijo2))
        for y in range(ciudades-1):  
            fit_hijo1 = fit_hijo1 + distancia_euclidiana(lista_ciudades[hijo1[y]][0], lista_ciudades[hijo1[y]][1], lista_ciudades[hijo1[y+1]][0], lista_ciudades[hijo1[y+1]][1])
            fit_hijo2 = fit_hijo2 + distancia_euclidiana(lista_ciudades[hijo2[y]][0], lista_ciudades[hijo2[y]][1], lista_ciudades[hijo2[y+1]][0], lista_ciudades[hijo2[y+1]][1])

        if fit_hijo1 < fit_hijo2:
            lista_poblacion[poblacion+valor_de_mutacion+i] = hijo1.copy()
        else:
            lista_poblacion[poblacion+valor_de_mutacion+i] = hijo2.copy()

        for limpia in range(ciudades):
            hijo1[limpia] = -1
            hijo2[limpia] = -1





def calcular_fitness_todos():
    global lista_poblacion
    for i in range(poblacion, suma_de_mu_y_lambda):
        fit = 0
        for j in range(ciudades-1): #Eeste ciclo recorre todo el conjunto de ciudades y se va almacenando en fit
                                            #Basicamente se calcula la distancia entre la ciudad N y N+1
            fit = fit + distancia_euclidiana( lista_ciudades[lista_poblacion[i][j]][0], lista_ciudades[lista_poblacion[i][j]][1], 
                                            lista_ciudades[lista_poblacion[i][j+1]][0], lista_ciudades[lista_poblacion[i][j+1]][1] )
        lista_fitness[i] = fit
    lista_mejor_fitness.append(min(lista_fitness, key=float))


#Funcion que nos da nuestros individuos seleccionado
def seleccion_determinista():
    global lista_poblacion, lista_fitness

    for i in range(poblacion):
        tributo1 = random.randrange(suma_de_mu_y_lambda)
        tributo2 = random.randrange(suma_de_mu_y_lambda)
        print('Tributos:    ' + str(tributo1) + '   ' + str(tributo2))

        if lista_fitness[tributo1] < lista_fitness[tributo2]:
            lista_seleccionados[i] = lista_poblacion[tributo1].copy()
        else:
            lista_seleccionados[i] = lista_poblacion[tributo2].copy()

#inicio del programa
generar_poblacion_inicial()



for ite in range(500):
    calcular_fitness_inicial()
    mutacion() #Se tiene que hacer primero la mutacion y lego la cruza para que funcionen los indices
    cruza()
    print('**************** POBLACION AFTER MUTATION AND CROSSOVER ******************')
    for i in range(suma_de_mu_y_lambda):
        print('h' + str(i) + '  ' + str(lista_poblacion[i]))
    calcular_fitness_todos()



    seleccion_determinista()

    #copiamos la poblacion
    for i in range(poblacion):
        for j in range(ciudades):
            lista_poblacion[i][j] = lista_seleccionados[i][j]

    #borramos los datos que existan en los indices de Lambda
    for i in range(poblacion, suma_de_mu_y_lambda):
        for j in range(ciudades):
            lista_poblacion[i][j] = -1




print('Fitnes final***********************')
for i in range(suma_de_mu_y_lambda):
    print('h' + str(i) + '  ' + str(lista_fitness[i]))

#print('SELECCIONADOS***********************')
#for i in range(poblacion):
#    print('h' + str(i) + '  ' + str(lista_seleccionados[i]))


print('**************** POBLAICON AL FINALIZAR ******************')
for i in range(suma_de_mu_y_lambda):
    print('h' + str(i) + '  ' + str(lista_poblacion[i]))

plt.plot(lista_graficar_fitness)
plt.plot(lista_mejor_fitness)
plt.show()