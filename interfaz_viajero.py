#Iniico de la interfaz grafica para el proyecto del Viajero de Metodos Inteligencia Artificial
from os import stat
import random
import math
import matplotlib.pyplot as plt
from tkinter import * #Libreria para GUI
from tkinter import ttk #libreria para los combobox
from tkinter import filedialog #libreria para cargar archivos desde el ordenador
from tkinter.filedialog import asksaveasfile #libreria para poder guardar los mapas
from tkinter import messagebox #Libreria que nos ayuda a Enviar mensajes de error al usuario 
import threading #Libreria que nos ayuda a la corrida paso a paso
import collections #Libreria que nos ayuda con la cola
import time #libreria que nos ayuda junto con threading a la corrida paso a paso
import sys #libreria para poder cerrar el porgrama
import cv2
from PIL import Image
from PIL import ImageTk 
import imutils
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

'''
ciudades = 10
lista_ciudades = [[270, 458], [722, 308], [465, 163], [172, 269], [587, 366], [817, 443], [950, 238], [649, 529], [384, 616], [1000, 600]]
mejor_combinacion = [2, 3, 0, 8, 7, 4, 1, 6, 5, 9]
lista_x = [0] * ciudades 
lista_y = [0] * ciudades
for i in range(ciudades): #ciclo para almacenar las coordenadas de las ciudades ordenadas
    lista_x[i] = lista_ciudades[mejor_combinacion[i]][0]
    lista_y[i] = lista_ciudades[mejor_combinacion[i]][1]
'''
lista_x = []
lista_y = []

l_fitness = IntVar


val_ciudades = None
val_poblacion = None
val_lambda = None
val_iteraciones = None
val_cruza = 0.0

background = None
bandera = None
lista_fitness = []
lista_ciudades = [] 

#Valores para el algoritomo
lista_poblacion = []

#image = None
def proyecto():
   
    def kill_inicio(): 
        win_inicio.destroy()

    def crear_viaje(ventana):
        
        #kill_inicio()
        ventana.destroy()

        def kill_crear():
            global val_ciudades, val_iteraciones, val_lambda, val_poblacion
            val_ciudades = combo_ciudades.get()
            val_poblacion = combo_poblacion.get()
            val_iteraciones = combo_iteraciones.get()
            val_lambda = combo_lambda.get()
            val_cruza = combo_cruza.get()
            win_crear.destroy()

        def regresar_menu():
            win_crear.destroy()
            proyecto()

        def mapa(): #funcion de la ventana final

            def algo_evolutivo(): #se supone que esta funcion ejecuta el algoritmo
                global val_ciudades, val_iteraciones, val_lambda, val_poblacion, lista_x, lista_y, lista_ciudades, lista_poblacion, lista_fitness

                print('hola\n aqui inicia el algoritmo evolutivo')
                inicio = time.time()
                # Este programa busca implementar una combinacion de algoritmos geneticos y estrategias evolutivas para poder resolver el
                # problema del agente viajero.
                
                bandera = 0 #bandera que nos ayuda a ayudarle a la mutacion despues de que no se encuentre un mejor fitness despues de (iteraciones/2) veces

                ciudades = int(val_ciudades) #nuero de ciudades a recorrer
                poblacion = int(val_poblacion) #miu
                individuos_nuevos = int(val_lambda) #lambda 
                suma_de_mu_y_lambda = poblacion + individuos_nuevos
                r = int(val_cruza) *0.1 #El porcentaje de lambda que se va a generar por cruza
                m = 1-r #El porcentaje de lambda que se va a generar por mutacion (r + m = 1, R es mas importante)

                #'----------------------------------------------------------
                print('Esta es la suma de la poblacion y lambda: ')
                print(suma_de_mu_y_lambda)
                print('Este es el numero de ciudades:   ')
                print(ciudades)
                print('Este es el valor de Cruza:   ')
                print(r)
                print('Este es el valor de Mutacion:   ')
                print(m)
                

                #'----------------------------------------------------------
                lista_ciudades = []
                lista_ciudades = [0] * int(ciudades) #Lista de las ciudades que vamos a recorrer
                print('LISTA CIUDADES: ')
                print(lista_ciudades)
                lista_poblacion = [0] * suma_de_mu_y_lambda #Lista para guardar la poblacion
                lista_fitness = [0] * suma_de_mu_y_lambda #lista que va a guardar los fitness de cada individuo
                lista_seleccionados = [0] * poblacion #lista que almacenara los miu seleciconados


                primeras_lista_x = [0] * ciudades 
                primeras_lista_y = [0] * ciudades
                lista_x = [0] * ciudades 
                lista_y = [0] * ciudades

                lista_graficar_fitness = [] #Lista que va a graficar el promedio del fitness 
                lista_mejor_fitness = [] #lista que va a graficar el mejor fitness encontrado y su evoluciom
                mejor_combinacion = [0] * ciudades #lista que va a almacenar la mejor combinacion encontrada
                lista_de_valores_min_por_corrida = [] #lista que va a graficar el mejor fitness encontrado en la corrida actual
                mejor_fitness = None #Valor del mejor fitness encontrado

                #Valores que nos van a almacenar las veces que se debe ejecutar un ciclo para que se almacenen Lambda nuevos
                valor_de_cruza = round(r*individuos_nuevos)
                valor_de_mutacion = round(m*individuos_nuevos)

                #Funcion de prueba para la generacion aleatoria de las ciudades de prueba
                def generar_ciudades():
                    global lista_ciudades
                    for i in range(ciudades):
                        #print('ENTRO AQUI!! ' + str(i))
                        #print(lista_ciudades[i])
                        lista_ciudades[i] = [0] * 2
                        x_ciudad = random.randint(60, 1140) #X's
                        y_ciudad = random.randint(23, 725) #Y's

                        while [x_ciudad,y_ciudad] in lista_ciudades: #este ciclo nos garantiza que no haya ciudades repetidas
                            x_ciudad = random.randint(0, 1200) #X's
                            y_ciudad = random.randint(0, 758) #Y's
                        lista_ciudades[i][0] = x_ciudad
                        lista_ciudades[i][1] = y_ciudad   

                generar_ciudades()

                print('Ciudades a recorrer: ')
                print(lista_ciudades)

                #Ciclo para generar la lista de listas de la poblacion-
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

                #Funcion que calcula el fitness de la poblacion
                def calcular_fitness_inicial():
                    global lista_poblacion, lista_ciudades, lista_fitness
                    valor_a_guardar = 0 #Valor que nos ayudara a almacenar el promedio en la lista a graficar fitness
                    for i in range(poblacion):
                        fit = 0 #Variable que va a incrementar para obtener el fitness
                        for j in range(ciudades-1): #Eeste ciclo recorre todo el conjunto de ciudades y se va almacenando en fit, es hasta ciudades-1 por que si no se sale del rango
                                                            #Basicamente se calcula la distancia entre la ciudad N y N+1
                            fit = fit + distancia_euclidiana( lista_ciudades[lista_poblacion[i][j]][0], lista_ciudades[lista_poblacion[i][j]][1], 
                                                            lista_ciudades[lista_poblacion[i][j+1]][0], lista_ciudades[lista_poblacion[i][j+1]][1] )
                        lista_fitness[i] = fit
                        valor_a_guardar = valor_a_guardar + lista_fitness[i]
                    
                    promedio = valor_a_guardar/poblacion
                    #lista_graficar_fitness.append(promedio)

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


                #Funcion que va a realizar la operacion de cruza, usaremos la cruza ciclica
                def cruza():
                    global lista_poblacion
                    #print('Inicia Cruza!!!')

                    #Se crean las listas de listas para poder trabajar localmente la cruza, se inicializa en -1 por que el 0 es parte de los indices
                    hijo1 = [-1] * ciudades
                    hijo2 = [-1] * ciudades

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
                            
                        #print('HIJO1: ' + str(hijo1))
                        #print('HIJO2: ' + str(hijo2))
                        
                        #obtenemos el fitness de los 2 hijos para ponerlos a competir HA HA HA
                        for y in range(ciudades-1):  
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
                    global lista_poblacion, lista_ciudades, lista_fitness
                    for i in range(poblacion, suma_de_mu_y_lambda):
                        fit = 0
                        for j in range(ciudades-1): #Eeste ciclo recorre todo el conjunto de ciudades y se va almacenando en fit
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
                veces = int(val_iteraciones)#int(input('ITERACIONES:     '))

                while iteraciones < veces:
                    nosequees += 1
                    

                    if iteraciones < (veces/2):
                        bandera = 0
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
                        tempo.plot(primeras_lista_x, primeras_lista_y, 'o-', color = "red")
                        canvas.draw()
                        tempo.clear()
                        background = plt.imread('mapa.jpg')
                        tempo.imshow(background)
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

                    if iteraciones == (veces/100): #if que nos grafica el mejor camino encontrado una vez que pacen (veces/4) iteraciones
                        print(help + iteraciones)
                        l_corrida.configure(text = 'Camino # : ' + str(help + iteraciones))
                        #plt.title('Camino numero: ' + str(help+iteraciones)) 
                        tempo.plot(lista_x, lista_y, 'o-', color = "black")
                        canvas.draw()
                        tempo.clear()
                        background = plt.imread('mapa.jpg')
                        tempo.imshow(background)
                        l_corrida.configure(text = 'Camino # : ' + str(help + iteraciones))
                        #plt.pause(0.2)
                        #fig.clear()
                        
                        

                    #print(nosequees)
                    iteraciones += 1
                l_fitness.configure(text = 'Primer Fitness : \n' + str("%.3f" % primer_mejor_fitness) + '\nMejor Fitness: \n' + str("%.3f" % mejor_fitness), background = '#23FF00')
                fin = time.time()
                print('Tiempo transcurrido: ' + str(fin-inicio) + ' segundos')
                times = fin - inicio
                l_corrida.configure(text = 'Camino # : ' + str(help + iteraciones) + '\n Tiempo (Sgs): ' + str("%.2f" % times))

            kill_crear()

            def regresar_menu_map(): #funcion que mata la ventana actual y regresa al menu principal
                win_mapa.destroy()
                proyecto()
            
            win_mapa = Tk()
            win_mapa.title('ejecucion del viaje')
            win_mapa.geometry('1200x800')
            win_mapa.configure(bg = '#FFFFFF')
            #302D35

            #imagen_mapa = ImageTk.PhotoImage(file='mapa.jpg')
            #img_mapa = Label(win_mapa, image = imagen_mapa)
            #img_mapa.pack(side='top', fill='both', expand='y',)

            #-----------------BOTONES-------------------
            
            b_iniciar = Button(win_mapa, text='INICIAR!', relief = 'groove', font = 'Calibri 20 bold', background = '#90E516', activebackground = 'Black', activeforeground = 'Green', command= lambda: algo_evolutivo())
            b_iniciar.place(x=970, y=110, width = 180, height = 80)
            b_cambiar = Button(win_mapa, text='CAMBIAR\nVALORES', relief = 'groove', font = 'Calibri 20 bold', background = 'Light blue', activebackground = 'Black', activeforeground = 'Green', command = lambda: crear_viaje(win_mapa))
            b_cambiar.place(x=970, y=200, width = 180, height = 100)
            b_menu = Button(win_mapa, text = 'MENU', relief = 'groove', font = 'Calibri 20 bold', bg = '#EA4F2D', command = regresar_menu_map)
            b_menu.place(x=970, y=500, width = 180, height = 100)

            #--------------LABELS--------------
            l_fitness = Label(win_mapa, text='FITNESS:', relief = 'flat', font = 'Calibri 16 bold', background = '#FF0000')
            l_fitness.place(x=970, y=310, width = 180, height = 180)
            l_corrida = Label(win_mapa, text='Camino # : ', relief = 'flat', font = 'Calibri 16 bold', background = '#19D7A0')
            l_corrida.place(x=970, y=610, width = 180, height = 100)


            '''
            img_mapa = ImageTk.PhotoImage(file='mapa.jpg')
            l_mapa = Label(win_mapa, image = img_mapa)
            l_mapa.grid(row = 0, column = 0)
            '''

            #------------------ COMO UNIR MATPLOTLIB A TKINTER!!!!!!!!!!!!!!!  
            background = plt.imread('mapa.jpg')
            fig = Figure(figsize= (9, 7), dpi=100)
            tempo = fig.add_subplot(111)
            tempo.imshow(background)
            #tempo.plot(lista_x, lista_y, 'o-', color = "red")
            
            
            canvas = FigureCanvasTkAgg(fig, master = win_mapa)
            canvas.draw()
            canvas.get_tk_widget().pack()

            #-------------------- Barra de herramientes ------------------
            toolbar = NavigationToolbar2Tk(canvas, win_mapa)
            toolbar.update()
            canvas.get_tk_widget().place(x=0, y=0)

            #win_mapa.resizable(False, False)
            win_mapa.resizable(False, False)
            win_mapa.mainloop()

        win_crear = Tk()
        win_crear.title('Genera tu viaje')
        win_crear.geometry('600x400')
        win_crear.configure(bg = '#302D35')

        #Labels para el texto de descripcion******************
        l_descripcion1 = Label(win_crear, text = 'CIUDADES A RECORRER \n En esta ventana te pedimos \n que nos indiques los siguientes valores: ', font = 'Calibri 20 bold', fg = 'white', bg = '#302D35')
        l_descripcion1.pack()

        #Estructura para pedir informacion ****************
        #info a pedir: NUMERO DE CIUDADES // POBLACION // POBLACION_NUEVA (LAMBDA) // ITERACIONES
        l_ciudades = Label(win_crear, text = 'CIUDADES', font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_ciudades.place(x = '10', y = '120', width = 120, height = 30)
        combo_ciudades = ttk.Combobox(win_crear, values = ['10', '20', '30', '40', '50', '100', '200', '300', '400', '500', '1000'], font = 'Calibri 15 bold')#Combobox para el valor de las ciudades
        combo_ciudades.place(x = '10', y = '150', width = 120, height = 30)

        l_poblacion = Label(win_crear, text = 'POBLACION', font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_poblacion.place(x = '140', y = '120', width = 150, height = 30)
        combo_poblacion = ttk.Combobox(win_crear, values = ['10', '20', '30', '40', '50', '100'], font = 'Calibri 15 bold' )#Combobox para el valor de la poblacion
        combo_poblacion.place(x = '140', y = '150', width = 150, height = 30)

        l_lambda = Label(win_crear, text='LAMBDA' , font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_lambda.place(x='300', y = '120', width = 120, height = 30)
        combo_lambda = ttk.Combobox(win_crear, values = ['10', '20', '30', '40', '50', '100'], font = 'Calibri 15 bold' )
        combo_lambda.place(x='300', y = '150', width = 120, height = 30)

        l_iteraciones = Label(win_crear, text='ITERACIONES' , font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_iteraciones.place(x='430', y = '120', width = 160, height = 30)
        combo_iteraciones = ttk.Combobox(win_crear, values = ['100', '200', '300', '400', '500', '1000', '2000', '3000', '4000', '5000', '10000'], font = 'Calibri 15 bold')
        combo_iteraciones.place(x='430', y = '150', width = 160, height = 30)

        l_cruza = Label(win_crear, text='VALOR DE CRUZA' , font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_cruza.place(x='190', y = '220', width = 205, height = 30)
        combo_cruza = ttk.Combobox(win_crear, values = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], font = 'Calibri 15 bold', state='readonly')
        combo_cruza.place(x='190', y = '250', width = 205, height = 30)

        b_regreso = Button(win_crear, text = 'REGRESAR', relief = 'groove', font = 'Calibri 20 bold', bg = '#EA4F2D', command = regresar_menu)
        b_regreso.place(x = '80', y = '320', width = 130, height = 50)

        b_crear = Button(win_crear, text = 'CONTINUAR', relief = 'groove', font = 'Calibri 20 bold', bg = 'Light green',command = mapa)
        b_crear.place(x = '380', y = '320', width = 140, height = 50)
        


        win_crear.mainloop()


    #Funcion que genera la ventana de los contacto
    def contacto():
        kill_inicio()

        def regresar_menu(): #funcion que mata la ventana actual y regresa al menu principal
            win_contacto.destroy()
            proyecto()
        

        win_contacto = Tk()
        win_contacto.title('Integrantes!')
        win_contacto.geometry('960x540')

        win_contacto.configure(bg = '#302D35')#cambiamos el fondo de la ventana

        #Creamos Frames para almacenar las etiquetas y sea mas facil colocar
        frame_face = Frame(win_contacto, relief = 'flat', bg = '#4267B2')
        frame_face.place(x = '50', y = '50', width = 350, height = 100)
        frame_whats = Frame(win_contacto, relief = 'flat', bg = '#25D366')
        frame_whats.place(x = '560', y = '50', width = 350, height = 100)
        frame_insta = Frame(win_contacto, relief = 'flat', bg = '#8a3ab9')
        frame_insta.place(x = '50', y = '250', width = 350, height = 100)
        frame_twitter = Frame(win_contacto, relief = 'flat', bg = '#1DA1F2')
        frame_twitter.place(x = '560', y = '250', width = 350, height = 100)



        name_face = Label(frame_face, text = 'Gmail:', relief = 'flat', bg = '#4267B2', font = 'Calibri 17 bold')
        name_face.pack()
        id_juanpa = Label(frame_face, text = 'juanpavelazquez123@gmail.com', relief = 'flat', bg = '#6a89c8', font = 'Calibri 17 bold' )
        id_juanpa.place(x= '15', y = '60')

        num_whats = Label(frame_whats, text = 'WHATSAPP', relief = 'flat', bg = '#25D366', font = 'Calibri 17 bold')
        num_whats.pack()
        id_rubs = Label(frame_whats, text = '+5212444480362', relief = 'flat', bg = '#52e086', font = 'Calibri 17 bold' )
        id_rubs.place(x= '90', y = '60')

        Name_vic = Label(frame_insta, text = 'INSTAGRAM', relief = 'flat', bg = '#8a3ab9', font = 'Calibri 17 bold')
        Name_vic.pack()
        id_vic = Label(frame_insta, text = 'juanpa.velazquez', relief = 'flat', bg = '#a764ce', font = 'Calibri 17 bold' )
        id_vic.place(x= '90', y = '60')

        
        Name_gio = Label(frame_twitter, text = 'Twitter', relief = 'flat', bg = '#1DA1F2', font = 'Calibri 17 bold')
        Name_gio.pack()
        id_gio = Label(frame_twitter, text = '@JuanPa3_1416', relief = 'flat', bg = '#6ec2f7', font = 'Calibri 17 bold' )
        id_gio.place(x= '90', y = '60')

        b_regreso = Button(win_contacto, text = 'RETURN', relief = 'groove', font = 'Calibri 20 bold', bg = '#DBEB75', command = regresar_menu)
        b_regreso.place(x = '330', y = '440', width = 300, height = 90)

        win_contacto.resizable(False, False)
        win_contacto.mainloop()

        #Fin contacto
        
    #Funcion que mata al programa*******************************
    def salir(): 
        sys.exit()

    # --------------------------- VENTANA PRINCIPAL -------------------------
    win_inicio = Tk()
    win_inicio.title("Problema del Viajero")
    imagen_fondo = PhotoImage(file="fondo.gif")

    w = imagen_fondo.width() # se adquiere el ancho de la imagen seleccionada
    h = imagen_fondo.height() # se adquiere el alto de la imagen seleccionada
    win_inicio.geometry('%dx%d+0+0' % (w,h)) #se aplican los valores adquiridos a la win (960x540)
    img_fondo = Label(win_inicio, image = imagen_fondo)
    img_fondo.pack(side='top', fill='both', expand='y',)

    b_generar_viaje = Button(win_inicio, text='CREAR UN VIAJE!', relief = 'groove', font = 'Calibri 20 bold', background = '#90E516', activebackground = 'Black', activeforeground = 'Green', command = lambda: crear_viaje(win_inicio))
    b_generar_viaje.place(x = 720, y = 170 , width = 250, height = 70)
    b_cargar_viaje = Button(win_inicio, text='CARGAR UN VIAJE!', relief = 'groove', font = 'Calibri 20 bold', background = '#4DE5D7', activebackground = 'Black', activeforeground = 'Green', state = 'disable')
    b_cargar_viaje.place(x = 720, y = 250 , width = 250, height = 70)
    b_contacto = Button(win_inicio, text='CONTACTO', relief = 'groove', font = 'Calibri 20 bold', background = '#7E3EBE', activebackground = 'Black', activeforeground = 'Green', command = contacto)
    b_contacto.place(x = 720, y = 330 , width = 250, height = 70)
    b_salir = Button(win_inicio, text='SALIR', relief = 'groove', font = 'Calibri 20 bold', background = '#DE3815', activebackground = 'Black', activeforeground = 'Green', command= salir)
    b_salir.place(x = 720, y = 410 , width = 250, height = 70)

    win_inicio.resizable(False, False)
    win_inicio.mainloop()

    

proyecto()