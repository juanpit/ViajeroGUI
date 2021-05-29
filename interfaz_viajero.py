#Iniico de la interfaz grafica para el proyecto del Viajero de Metodos Inteligencia Artificial
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

ciudades = 10
lista_ciudades = [[270, 458], [722, 308], [465, 163], [172, 269], [587, 366], [817, 443], [950, 238], [649, 529], [384, 616], [1000, 600]]
mejor_combinacion = [2, 3, 0, 8, 7, 4, 1, 6, 5, 9]
lista_x = [0] * ciudades 
lista_y = [0] * ciudades
for i in range(ciudades): #ciclo para almacenar las coordenadas de las ciudades ordenadas
    lista_x[i] = lista_ciudades[mejor_combinacion[i]][0]
    lista_y[i] = lista_ciudades[mejor_combinacion[i]][1]


l_fitness = IntVar



#image = None
def proyecto():


    def algo_evolutivo():
        print('hola')

    def kill_inicio(): 
        win_inicio.destroy()


    
    def crear_viaje(ventana):

        #kill_inicio()
        ventana.destroy()

        def kill_crear():
            win_crear.destroy()

        def regresar_menu():
            win_crear.destroy()
            proyecto()

        def mapa(): #funcion de la ventana final

            kill_crear()

            def regresar_menu_map(): #funcion que mata la ventana actual y regresa al menu principal
                win_mapa.destroy()
                proyecto()
            
            win_mapa = Tk()
            win_mapa.title('ejecucion del viaje')
            win_mapa.geometry('1200x800')
            win_mapa.configure(bg = '#FFFFFF')
            #302D35

            imagen_mapa = ImageTk.PhotoImage(file='mapa.jpg')
            #img_mapa = Label(win_mapa, image = imagen_mapa)
            #img_mapa.pack(side='top', fill='both', expand='y',)


            '''
            img_mapa = ImageTk.PhotoImage(file='mapa.jpg')
            l_mapa = Label(win_mapa, image = img_mapa)
            l_mapa.grid(row = 0, column = 0)
            '''

            #------------------ COMO UNIR MATPLOTLIB A TKINTER!!!!!!!!!!!!!!!  
            background = plt.imread('mapa.jpg')
            
            fig = Figure(figsize= (10, 7), dpi=100)
            temp = fig.add_subplot(111)
            temp.imshow(background)
            temp.plot(lista_x, lista_y, 'o-', color = "red")
            
            
            canvas = FigureCanvasTkAgg(fig, master = win_mapa)
            canvas.draw()
            canvas.get_tk_widget().pack()

            #-------------------- Barra de herramientes ------------------
            toolbar = NavigationToolbar2Tk(canvas, win_mapa)
            toolbar.update()
            canvas.get_tk_widget().place(x=0, y=0)

            #-----------------BOTONES-------------------
            
            b_iniciar = Button(win_mapa, text='INICIAR!', relief = 'groove', font = 'Calibri 20 bold', background = '#90E516', activebackground = 'Black', activeforeground = 'Green')
            b_iniciar.place(x=970, y=110, width = 180, height = 80)
            b_cambiar = Button(win_mapa, text='CAMBIAR\nVALORES', relief = 'groove', font = 'Calibri 20 bold', background = 'Light blue', activebackground = 'Black', activeforeground = 'Green', command = lambda: crear_viaje(win_mapa))
            b_cambiar.place(x=970, y=200, width = 180, height = 100)
            b_menu = Button(win_mapa, text = 'MENU', relief = 'groove', font = 'Calibri 20 bold', bg = '#EA4F2D', command = regresar_menu_map)
            b_menu.place(x=970, y=500, width = 180, height = 100)

            #--------------LABELS--------------
            l_fitness = Label(win_mapa, text='FITNESS:', relief = 'flat', font = 'Calibri 16 bold', background = '#F09A87')
            l_fitness.place(x=970, y=310, width = 180, height = 180)



            #win_mapa.resizable(False, False)
            win_mapa.resizable(False, False)
            win_mapa.mainloop()

        win_crear = Tk()
        win_crear.title('Genera tu viaje')
        win_crear.geometry('600x300')
        win_crear.configure(bg = '#302D35')

        #Labels para el texto de descripcion******************
        l_descripcion1 = Label(win_crear, text = 'CIUDADES A RECORRER \n En esta ventana te pedimos \n que nos indiques los siguientes valores: ', font = 'Calibri 20 bold', fg = 'white', bg = '#302D35')
        l_descripcion1.pack()

        #Estructura para pedir informacion ****************
        #info a pedir: NUMERO DE CIUDADES // POBLACION // POBLACION_NUEVA (LAMBDA) // ITERACIONES
        l_ciudades = Label(win_crear, text = 'CIUDADES', font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_ciudades.place(x = '10', y = '120', width = 120, height = 30)
        combo_ciudades = ttk.Combobox(win_crear,values = ['10', '20', '30', '40', '50', '100', '200', '300', '400', '500', '1000'], font = 'Calibri 15 bold' )#Combobox para el valor de las ciudades
        combo_ciudades.place(x = '10', y = '150', width = 120, height = 30)

        l_poblacion = Label(win_crear, text = 'POBLACION', font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_poblacion.place(x = '140', y = '120', width = 150, height = 30)
        combo_poblacion = ttk.Combobox(win_crear,values = ['10', '20', '30', '40', '50', '100'], font = 'Calibri 15 bold' )#Combobox para el valor de la poblacion
        combo_poblacion.place(x = '140', y = '150', width = 150, height = 30)

        l_lambda = Label(win_crear, text='LAMBDA' , font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_lambda.place(x='300', y = '120', width = 120, height = 30)
        combo_lambda = ttk.Combobox(win_crear,values = ['10', '20', '30', '40', '50', '100'], font = 'Calibri 15 bold' )
        combo_lambda.place(x='300', y = '150', width = 120, height = 30)

        l_iteraciones = Label(win_crear, text='ITERACIONES' , font = 'Calibri 20 bold', fg = 'white', bg = '#665C77')
        l_iteraciones.place(x='430', y = '120', width = 160, height = 30)
        combo_iteraciones = ttk.Combobox(win_crear, values = ['10', '20', '30', '40', '50', '100', '200', '300', '400', '500', '1000'], font = 'Calibri 15 bold')
        combo_iteraciones.place(x='430', y = '150', width = 160, height = 30)

        b_regreso = Button(win_crear, text = 'REGRESAR', relief = 'groove', font = 'Calibri 20 bold', bg = '#EA4F2D', command = regresar_menu)
        b_regreso.place(x = '80', y = '220', width = 130, height = 50)

        b_crear = Button(win_crear, text = 'CONTINUAR', relief = 'groove', font = 'Calibri 20 bold', bg = 'Light green',command = mapa)
        b_crear.place(x = '380', y = '220', width = 140, height = 50)
        


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



        name_face = Label(frame_face, text = 'FACEBOOK', relief = 'flat', bg = '#4267B2', font = 'Calibri 17 bold')
        name_face.pack()
        id_juanpa = Label(frame_face, text = 'Juan Pablo Velazquez', relief = 'flat', bg = '#6a89c8', font = 'Calibri 17 bold' )
        id_juanpa.place(x= '75', y = '60')

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
    b_cargar_viaje = Button(win_inicio, text='CARGAR UN VIAJE!', relief = 'groove', font = 'Calibri 20 bold', background = '#4DE5D7', activebackground = 'Black', activeforeground = 'Green')
    b_cargar_viaje.place(x = 720, y = 250 , width = 250, height = 70)
    b_contacto = Button(win_inicio, text='CONTACTO', relief = 'groove', font = 'Calibri 20 bold', background = '#7E3EBE', activebackground = 'Black', activeforeground = 'Green', command = contacto)
    b_contacto.place(x = 720, y = 330 , width = 250, height = 70)
    b_salir = Button(win_inicio, text='SALIR', relief = 'groove', font = 'Calibri 20 bold', background = '#DE3815', activebackground = 'Black', activeforeground = 'Green', command= salir)
    b_salir.place(x = 720, y = 410 , width = 250, height = 70)

    win_inicio.resizable(False, False)
    win_inicio.mainloop()

proyecto()