import random
import math
import matplotlib.pyplot as plt

# Este programa busca implementar una combinacion de algoritmos geneticos y estrategias evolutivas para poder resolver el
# problema del agente viajero.

bandera = 0
ciudades = 1000
poblacion = 10 #miu


lista_ciudades = [0] * ciudades #Lista de las ciudades que vamos a recorrer
lista_poblacion = [0] * poblacion #Lista para guardar la poblacion
lista_fitness = [0] * poblacion #lista que va a guardar los fitness de cada individuo
p_s = [0] * poblacion #lista que almacenara los miu seleciconados


lista_graficar_fitness = []
lista_mejor_fitness = []
mejor_combinacion = [0] * ciudades
lista_de_valores_min_por_corrida = []
mejor_fitness = None

r = 0.1 #El porcentaje de lambda que se va a generar por cruza
m = 0.1 #El porcentaje de lambda que se va a generar por mutacion (r + m = 1, M es mas importante)

selec_prob_all = round(r*poblacion) # todos los elementos que se van a usar para la cruza\
if(selec_prob_all%2 != 0):
    selec_prob_all = selec_prob_all-1 #If que nos ayuda a que el numero total de individuos no sea impar

selec_prob_pairs = round(selec_prob_all/2) # los pares necesarios

print(selec_prob_all)


#Funcion de prueba para la generacion aleatoria de las ciudades de prueba--------------
for i in range(ciudades):
    lista_ciudades[i] = [0] * 2
    x_ciudad = random.randint(0, 1000) #X's
    y_ciudad = random.randint(0, 1000) #Y's

    while [x_ciudad,y_ciudad] in lista_ciudades:
        x_ciudad = random.randint(0, 1000) #X's
        y_ciudad = random.randint(0, 1000) #Y's
    lista_ciudades[i][0] = x_ciudad
    lista_ciudades[i][1] = y_ciudad


#lista_ciudades = [[7, 5], [1, 1], [2, 4], [4, 6], [7, 4], [3, 8], [4, 0], [10, 5], [7, 2], [8, 7]] 
print('Ciudades a recorrer: ')
print(lista_ciudades)


#Ciclo para generar la lista de listas
for i in range(poblacion):
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


def calcular_fitness():
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
    lista_de_valores_min_por_corrida.append(min(lista_fitness, key= float))


def mutacion(mut):
    global lista_poblacion, bandera, p_s

    a_mutar = mut*poblacion

    for i in range(round(a_mutar)):
        #print('Muta a :' + str(mut))
        tributo = random.randrange(poblacion) #Sacamos el individuo que va a ser mutado
        #print('A MUTAR', str(tributo), str(p_s[tributo]))

       #se sacan las 2 ciudades a intercambiar
        ciudad1 = random.randrange(ciudades)
        ciudad2 = random.randrange(ciudades)

        temp = p_s[tributo][ciudad1]
        p_s[tributo][ciudad1] = p_s[tributo][ciudad2]
        p_s[tributo][ciudad2] = temp

        #intercambiar otras 2 ciudades***********************************
        if bandera == 1:
            print('entro aqui')
            ciudad1 = random.randrange(ciudades)
            ciudad2 = random.randrange(ciudades)
            temp = p_s[tributo][ciudad1]
            p_s[tributo][ciudad1] = p_s[tributo][ciudad2]
            p_s[tributo][ciudad2] = temp
        #print('mutado', str(p_s[tributo]))


def torneo_cruza(prim, seg):
    if lista_fitness[prim] <= lista_fitness[seg]:
        return prim
    else:
        return seg 

def cruza():
    global lista_poblacion, selec_prob_all, selec_prob_pairs
    #print('Inicia Cruza!!!')

    hijo1 = [-1] * ciudades
    hijo2 = [-1] * ciudades
    lista_trib = [0] * 2

    aiuda_temp = 0
    for i in range(selec_prob_pairs):

        for t in range(2):
            tributo1 = random.randrange(poblacion)
            tributo2 = random.randrange(poblacion)
            lista_trib[t] = torneo_cruza(tributo1, tributo2)

        #print('Cruza# ' + str(i))
        fit_hijo1=0
        fit_hijo2=0
        tributo1 = lista_trib[0]
        tributo2 = lista_trib[1]
        #print('tributo1: ' + str(tributo1))
        #print('tributo2: ' + str(tributo2))

        #iniciamos proceso para hijo 1
        hijo1[0] = lista_poblacion[tributo1][0]
        indice = lista_poblacion[tributo2].index(hijo1[0])#indice que se usara para manipular el primer hijo
        #iniciamos proceso para hijo 2
        hijo2[0] = lista_poblacion[tributo2][0]
        indice_h2 = lista_poblacion[tributo1].index(hijo2[0])#indice que se usara para manipular el segundo hijo

        #SE HACE LA CRUZA CICLADA
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
            
        #print('HIJO1: ' + str(hijo1))
        #print('HIJO2: ' + str(hijo2))
        
        p_s[aiuda_temp] = hijo1.copy()
        p_s[aiuda_temp + 1] = hijo2.copy()
        aiuda_temp += 2

        for limpia in range(ciudades):
            hijo1[limpia] = -1
            hijo2[limpia] = -1




#cambar mi seleccion a solamente elitista******************************
#hacer otro para que sea como Un genetico******************************


#Funcion que nos da nuestros individuos seleccionado
def seleccion_torneo():
    global lista_poblacion, lista_fitness

    for i in range(selec_prob_all ,poblacion):
        tributo1 = random.randrange(poblacion)
        tributo2 = random.randrange(poblacion)
        #print('Tributos:    ' + str(tributo1) + '   ' + str(tributo2))

        if lista_fitness[tributo1] <= lista_fitness[tributo2]:
            p_s[i] = lista_poblacion[tributo1].copy()
        else:
            p_s[i] = lista_poblacion[tributo2].copy()
    


#inicio del programa
generar_poblacion_inicial()


iteraciones = 0
help = 0
aiuda =0
veces = 400#int(input('ITERACIONES:     '))
while iteraciones < veces:

    calcular_fitness()
    
    cruza()
    
    seleccion_torneo()


    if aiuda == 0:
        mejor_fitness = min(lista_fitness, key=float)
        aiuda = aiuda + 1
    
    if ( (min(lista_fitness, key=float)) >= mejor_fitness): #si el mejor fitness de la corrida actual es mayor que el mejor fitness encontrado hasta el momento (NO MEJORA)
        mejor_fitness = min(lista_de_valores_min_por_corrida, key=float)
        mejor_combinacion = lista_poblacion[lista_fitness.index(min(lista_fitness, key=float))].copy()
        lista_mejor_fitness.append(min(lista_de_valores_min_por_corrida, key=float))

    if ( (min(lista_fitness, key=float)) < mejor_fitness):#mejora
        mejor_fitness = min(lista_fitness, key=float) #se iguala al mejor fitness de la corrida
        mejor_combinacion = lista_poblacion[lista_fitness.index(min(lista_fitness, key=float))].copy()
        lista_mejor_fitness.append(min(lista_fitness, key=float))
        help += iteraciones
        iteraciones=0

    #print('mejor por corrida' + str(min(lista_fitness, key=float)))
    #print('mejor_fitness' + str(mejor_fitness))

    if iteraciones < (veces/2):
        bandera = 0
    if iteraciones >= (veces/2):
        bandera = 1

    mutacion(m)


    #copiamos la poblacion
    for pob in range(poblacion):
        for ciu in range(ciudades):
            lista_poblacion[pob][ciu] = p_s[pob][ciu]


    iteraciones += 1




print('Fitnes final***********************')
for i in range(poblacion):
    print('h' + str(i) + '  ' + str(lista_fitness[i]))

#print('SELECCIONADOS***********************')
#for i in range(poblacion):
#    print('h' + str(i) + '  ' + str(p_s[i]))


print('**************** POBLAICON AL FINALIZAR ******************')
for i in range(poblacion):
    print('h' + str(i) + '  ' + str(lista_poblacion[i]))

print('se encontro en ' + str(help) + ' Iteraciones')
print('El mejor fitness encontrado fue:' + str(mejor_fitness))

print('La mejor combinadion es: ')
print(mejor_combinacion)

plt.plot(lista_graficar_fitness)
plt.plot(lista_de_valores_min_por_corrida)
plt.plot(lista_mejor_fitness)
plt.show()