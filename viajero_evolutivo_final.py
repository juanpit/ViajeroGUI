import random
import math
import matplotlib.pyplot as plt
import time

inicio = time.time()
# Este programa busca implementar una combinacion de algoritmos geneticos y estrategias evolutivas para poder resolver el
# problema del agente viajero.
#Creado por: Juan Pablo Velazquez

bandera = 0 #bandera que nos ayuda a ayudarle a la mutacion despues de que no se encuentre un mejor fitness despues de (iteraciones/2) veces

ciudades = 50 #numero de ciudades a recorer
poblacion = 30 #miu
individuos_nuevos = 20 #lambda 
suma_de_mu_y_lambda = poblacion + individuos_nuevos
r = 0.0 #El porcentaje de lambda que se va a generar por cruza
m = 1-r #El porcentaje de lambda que se va a generar por mutacion (r + m = 1, R es mas importante)


lista_ciudades = [0] * (ciudades + 1)#Lista de las ciudades que vamos a recorrer
lista_poblacion = [0] * suma_de_mu_y_lambda #Lista para guardar la poblacion
lista_fitness = [0] * suma_de_mu_y_lambda #lista que va a guardar los fitness de cada individuo
lista_seleccionados = [0] * poblacion #lista que almacenara los miu seleciconados

lista_graficar_fitness = [] #Lista que va a graficar el promedio del fitness 
lista_mejor_fitness = [] #lista que va a graficar el mejor fitness encontrado y su evoluciom
mejor_combinacion = [0] * (ciudades + 1) #lista que va a almacenar la mejor combinacion encontrada
lista_de_valores_min_por_corrida = [] #lista que va a graficar el mejor fitness encontrado en la corrida actual
mejor_fitness = None #Valor del mejor fitness encontrado

#listas que nos va a ayudar a graficar el camino que el viajero debe tomar
primeras_lista_x = [0] * (ciudades + 1)
primeras_lista_y = [0] * (ciudades + 1)
primer_mejor_fitness = 0
lista_x = [0] * (ciudades  + 1)
lista_y = [0] * (ciudades + 1)


#Valores que nos van a almacenar las veces que se debe ejecutar un ciclo para que se almacenen Lambda nuevos
valor_de_cruza = round(r*individuos_nuevos)
valor_de_mutacion = round(m*individuos_nuevos)

background = plt.imread('mapa.jpg')


#Funcion de prueba para la generacion aleatoria de las ciudades de prueba
def generar_ciudades():
    global lista_ciudades
    for i in range(ciudades):
        lista_ciudades[i] = [0] * 2
        x_ciudad = random.randint(60, 1140) #X's
        y_ciudad = random.randint(23, 725) #Y's

        while [x_ciudad,y_ciudad] in lista_ciudades: #este ciclo nos garantiza que no haya ciudades repetidas
            x_ciudad = random.randint(0, 1200) #X's
            y_ciudad = random.randint(0, 758) #Y's
        lista_ciudades[i][0] = x_ciudad
        lista_ciudades[i][1] = y_ciudad

generar_ciudades()
#lista_ciudades = [[270, 458], [722, 308], [465, 163], [172, 269], [587, 366], [817, 443], [950, 238], [649, 529], [384, 616], [1000, 600]]
print('Ciudades a recorrer: ')
print(lista_ciudades)

#Ciclo para generar la lista de listas de la poblacion-
for i in range(suma_de_mu_y_lambda):
    lista_poblacion[i] = [-1] * (ciudades + 1) #se inicializa en -1 por que el cero es parte de los indices 

def generar_poblacion_inicial(): #Funcion que nos va a generar nuestra poblacion inicial

    for i in range(poblacion):
        for j in range(ciudades):
            ci = random.randrange(ciudades)
            #print(ci)
            while ci in lista_poblacion[i]: #while que va validando que no se repitan los valores
                ci = random.randrange(ciudades)         
            lista_poblacion[i][j] = ci 
        
        lista_poblacion[i][ciudades] = lista_poblacion[i][0]
    

    print('**************** POBLAICON INICIAL ******************')
    for i in range(poblacion):
        print('h' + str(i) + '  ' + str(lista_poblacion[i]))


#Funcion que recibe un par de coordenadas y nos regresa la distancia euclidiana entre estas
def distancia_euclidiana(x1, y1, x2, y2):
    res = math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
    return res

#Funcion que calcula el fitness de la poblacion
def calcular_fitness_inicial():
    global lista_poblacion
    valor_a_guardar = 0 #Valor que nos ayudara a almacenar el promedio en la lista a graficar fitness
    for i in range(poblacion):
        fit = 0 #Variable que va a incrementar para obtener el fitness
        for j in range(ciudades): #Eeste ciclo recorre todo el conjunto de ciudades y se va almacenando en fit, es hasta ciudades-1 por que si no se sale del rango
                                            #Basicamente se calcula la distancia entre la ciudad N y N+1
            fit = fit + distancia_euclidiana( lista_ciudades[lista_poblacion[i][j]][0], lista_ciudades[lista_poblacion[i][j]][1], 
                                            lista_ciudades[lista_poblacion[i][j+1]][0], lista_ciudades[lista_poblacion[i][j+1]][1] )
        lista_fitness[i] = fit
        valor_a_guardar = valor_a_guardar + lista_fitness[i]
    
    promedio = valor_a_guardar/poblacion
    lista_graficar_fitness.append(promedio)

#Funcion para realizar la mutacion
def mutacion():
    global lista_poblacion, bandera

    #La mutacion consiste en intercambiar las posiciones de 2 ciudades en nuestro individuo
    for i in range(valor_de_mutacion):
        #print('Muta')
        tributo = random.randrange(poblacion) #Sacamos el individuo que va a ser mutado de la poblacion
        lista_poblacion[i+poblacion] = lista_poblacion[tributo].copy() #Lo copiamos en donde va a estar almacenado el individuo mutado para trabajar sobre el
        #print(tributo)

        #se sacan las 2 ciudades a intercambiar
        ciudad1 = random.randrange(ciudades)
        ciudad2 = random.randrange(ciudades)
        #print('Ciudad 1 ' + str(ciudad1))
        #print('Ciudad 2 ' + str(ciudad2))
        
        temp = lista_poblacion[i+poblacion][ciudad1] #guardamos la ciudad 1 en la variable temporal para intercambiarla
        lista_poblacion[i+poblacion][ciudad1] = lista_poblacion[i+poblacion][ciudad2] #intercambiamos la ciudad 2 con la 1
        lista_poblacion[i+poblacion][ciudad2] = temp #guardamos la ciudad 1 en donde estaba la 2

        #Entra aqui solo si han pasado (veces / 2) iteraciones
        #Basicamente se intercambian 2 posiciones del mismo individuo
        if bandera == 1:
            ciudad1 = random.randrange(ciudades)
            ciudad2 = random.randrange(ciudades)

            temp = lista_poblacion[i+poblacion][ciudad1]
            lista_poblacion[i+poblacion][ciudad1] = lista_poblacion[i+poblacion][ciudad2]
            lista_poblacion[i+poblacion][ciudad2] = temp

        if bandera == 2:
            ciudad1 = random.randrange(ciudades)
            ciudad2 = random.randrange(ciudades)

            temp = lista_poblacion[i+poblacion][ciudad1]
            lista_poblacion[i+poblacion][ciudad1] = lista_poblacion[i+poblacion][ciudad2]
            lista_poblacion[i+poblacion][ciudad2] = temp

            ciudad1 = random.randrange(ciudades)
            ciudad2 = random.randrange(ciudades)

            temp = lista_poblacion[i+poblacion][ciudad1]
            lista_poblacion[i+poblacion][ciudad1] = lista_poblacion[i+poblacion][ciudad2]
            lista_poblacion[i+poblacion][ciudad2] = temp

        
#Funcion que va a realizar la operacion de cruza, usaremos la cruza ciclica
def cruza():
    global lista_poblacion
    #print('Inicia Cruza!!!')

    #Se crean las listas de listas para poder trabajar localmente la cruza, se inicializa en -1 por que el 0 es parte de los indices
    hijo1 = [-1] * (ciudades+1)
    hijo2 = [-1] * (ciudades+1)

    for i in range(valor_de_cruza):

        #print('Cruza# ' + str(i))
        #Estas variables van a almacenar el fitness de los nuevos hijos ya que el algoritmo evolutivo solo nos permite agregar 1 hijo generado por cruza, entonces seleccionaremos el mejor hijo
        fit_hijo1=0 
        fit_hijo2=0
        #Se sacan los padres para cruzar
        tributo1 = random.randrange(poblacion)
        tributo2 = random.randrange(poblacion)
        #print('tributo1: ' + str(tributo1))
        #print('tributo2: ' + str(tributo2))

        #iniciamos proceso para hijo 1
        hijo1[0] = lista_poblacion[tributo1][0] #asignamos la primera posicion del tributo a su hijo 
        indice = lista_poblacion[tributo2].index(hijo1[0])#indice que se usara para manipular el primer hijo
        #iniciamos proceso para hijo 2
        hijo2[0] = lista_poblacion[tributo2][0] #asignamos la primera posicion del tributo a su hijo 
        indice_h2 = lista_poblacion[tributo1].index(hijo2[0])#indice que se usara para manipular el segundo hijo

        #Como nuestros hijos estan igualados a -1 nos ayudara a saber cuando ya se cumplio un ciclo
        while hijo1[indice] == -1:
            hijo1[indice] = lista_poblacion[tributo1][indice] 
            indice2 = lista_poblacion[tributo2].index(hijo1[indice])
            indice = indice2

        while hijo2[indice_h2] == -1:
            hijo2[indice_h2] = lista_poblacion[tributo2][indice_h2]
            indice_2h2 = lista_poblacion[tributo1].index(hijo2[indice_h2])
            indice_h2 = indice_2h2  

        #una vez que ya termino el ciclo solo queda asignar los valores del padre a los que no se llenaron 
        for padre in range(ciudades):
            #print('entro')
            #print(hijo1[padre])
            if hijo1[padre] == -1:
                hijo1[padre] = lista_poblacion[tributo2][padre]

            if hijo2[padre] == -1:
                hijo2[padre] = lista_poblacion[tributo1][padre]
        
        #se agrega el viaje de regreso
        hijo1[ciudades] = hijo1[0]
        hijo2[ciudades] = hijo2[0]

        #print('HIJO1: ' + str(hijo1))
        #print('HIJO2: ' + str(hijo2))

        #obtenemos el fitness de los 2 hijos para ponerlos a competir HA HA HA
        for y in range(ciudades):  
            fit_hijo1 = fit_hijo1 + distancia_euclidiana(lista_ciudades[hijo1[y]][0], lista_ciudades[hijo1[y]][1], lista_ciudades[hijo1[y+1]][0], lista_ciudades[hijo1[y+1]][1])
            fit_hijo2 = fit_hijo2 + distancia_euclidiana(lista_ciudades[hijo2[y]][0], lista_ciudades[hijo2[y]][1], lista_ciudades[hijo2[y+1]][0], lista_ciudades[hijo2[y+1]][1])

        #los ponemos a competir y asignamos el mejor a nuestros lambdas
        if fit_hijo1 <= fit_hijo2:
            lista_poblacion[poblacion+valor_de_mutacion+i] = hijo1.copy()
        else:
            lista_poblacion[poblacion+valor_de_mutacion+i] = hijo2.copy()
        #se limpia para que no tengan valores de los que se pueden ocupar
        for limpia in range(ciudades):
            hijo1[limpia] = -1
            hijo2[limpia] = -1

#funcion que calcula el fitness de los lambra nuevos
def calcular_fitness_todos():
    global lista_poblacion
    for i in range(poblacion, suma_de_mu_y_lambda):
        fit = 0
        for j in range(ciudades): #Eeste ciclo recorre todo el conjunto de ciudades y se va almacenando en fit
                                            #Basicamente se calcula la distancia entre la ciudad N y N+1
            fit = fit + distancia_euclidiana( lista_ciudades[lista_poblacion[i][j]][0], lista_ciudades[lista_poblacion[i][j]][1], 
                                            lista_ciudades[lista_poblacion[i][j+1]][0], lista_ciudades[lista_poblacion[i][j+1]][1] )
        lista_fitness[i] = fit
    lista_de_valores_min_por_corrida.append(min(lista_fitness, key= float))


#Funcion que nos da nuestros individuos seleccionado
def seleccion_elitista():
    global lista_poblacion, lista_fitness

    for i in range(poblacion):
        indice = lista_fitness.index(min(lista_fitness, key=float))
        lista_seleccionados[i] = lista_poblacion[indice].copy()
        #print(lista_seleccionados[i])
        lista_fitness[indice]= max(lista_fitness, key=float) *1000 #una vez que se escojamos al mejor, lo sacamos del rango para que no se escoja otra vez
    #print(lista_fitness)
    

#inicio del programa-------------------------------
generar_poblacion_inicial()

nosequees = 0
fig = plt.figure()
iteraciones = 0
help = 0
aiuda =0
veces = 1000#int(input('ITERACIONES:     '))
while iteraciones < veces:
    nosequees += 1
    

    if iteraciones < (veces/2):
        bandera = 0
    elif iteraciones < (veces /3):
        bandera = 2
    elif iteraciones > (veces/2):
        bandera = 1
        

    calcular_fitness_inicial()
    mutacion() #Se tiene que hacer primero la mutacion y lego la cruza para que funcionen los indices
    cruza()
  
    calcular_fitness_todos()

    if aiuda == 0: #if que entrara una sola vez
        mejor_fitness = min(lista_fitness, key=float)
        primer_mejor_fitness = mejor_fitness
        mejor_combinacion = lista_poblacion[lista_fitness.index(min(lista_fitness, key=float))].copy()
        for i in range(ciudades): #ciclo para almacenar las coordenadas de las ciudades ordenadas
            primeras_lista_x[i] = lista_ciudades[mejor_combinacion[i]][0]
            primeras_lista_y[i] = lista_ciudades[mejor_combinacion[i]][1]
        primeras_lista_x[ciudades] = lista_ciudades[mejor_combinacion[0]][0]
        primeras_lista_y[ciudades] = lista_ciudades[mejor_combinacion[0]][1]
        plt.title('Primer mejor camino encontraro con fitness: ' + str(primer_mejor_fitness))    
        plt.plot(primeras_lista_x, primeras_lista_y, 'o-', color = "red")
        plt.imshow(background)
        plt.draw()
        plt.pause(0.1)
        fig.clear()
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

    seleccion_elitista()


    #copiamos la poblacion
    for i in range(poblacion):
        for j in range(ciudades):
            lista_poblacion[i][j] = lista_seleccionados[i][j]

    #borramos los datos que existan en los indices de Lambda
    for i in range(poblacion, suma_de_mu_y_lambda):
        for j in range(ciudades):
            lista_poblacion[i][j] = -1

    for i in range(ciudades): #ciclo para almacenar las coordenadas de las ciudades ordenadas
        lista_x[i] = lista_ciudades[mejor_combinacion[i]][0]
        lista_y[i] = lista_ciudades[mejor_combinacion[i]][1]
    #le damos el valor de regreso
    lista_x[ciudades] = lista_ciudades[mejor_combinacion[0]][0]
    lista_y[ciudades] = lista_ciudades[mejor_combinacion[0]][1]

    if iteraciones == (veces/10): #if que nos grafica el mejor camino encontrado una vez que pacen (veces/4) iteraciones
        print(help + iteraciones)
        plt.title('Camino numero: ' + str(help+iteraciones)) 
        plt.plot(lista_x, lista_y, 'o-', color = "black")
        plt.imshow(background)
        plt.draw()
        plt.pause(0.2)
        fig.clear()
        

    #print(nosequees)
    iteraciones += 1

fin = time.time()
print('Tiempo transcurrido: ' + str(fin-inicio) + ' segundos')




#print('Fitnes final***********************')
#for i in range(suma_de_mu_y_lambda):
#    print('h' + str(i) + '  ' + str(lista_fitness[i]))

#print('SELECCIONADOS***********************')
#for i in range(poblacion):
#    print('h' + str(i) + '  ' + str(lista_seleccionados[i]))


#print('**************** POBLAICON AL FINALIZAR ******************')
#for i in range(suma_de_mu_y_lambda):
#    print('h' + str(i) + '  ' + str(lista_poblacion[i]))

print('se encontro en ' + str(help) + ' Iteraciones')
print('El mejor fitness encontrado fue:' + str(mejor_fitness))

print('La mejor combinadion es: ')
print(mejor_combinacion)

#plt.plot(lista_graficar_fitness)
plt.plot(lista_de_valores_min_por_corrida)
plt.plot(lista_mejor_fitness)
plt.show()

fig2 = plt.figure()

for i in range(ciudades): #ciclo para almacenar las coordenadas de las ciudades ordenadas
    lista_x[i] = lista_ciudades[mejor_combinacion[i]][0]
    lista_y[i] = lista_ciudades[mejor_combinacion[i]][1]

#le damos el valor de regreso
lista_x[ciudades] = lista_ciudades[mejor_combinacion[0]][0]
lista_y[ciudades] = lista_ciudades[mejor_combinacion[0]][1]

ax = plt.subplot(1,2,1)
ax.set_title('Primer camino encontrado con fitness: ' + str(primer_mejor_fitness))    
ax.plot(primeras_lista_x, primeras_lista_y, 'o-', color = "red")
ax.imshow(background)
ax = plt.subplot(1,2,2)
ax.set_title('MEJOR CAMINO ENCONTRADO!!! con fitness: ' + str(mejor_fitness)) 
ax.plot(lista_x, lista_y, 'o-', color = "black")
ax.imshow(background)
plt.show()

