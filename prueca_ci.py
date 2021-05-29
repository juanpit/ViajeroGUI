
lista_poblacion = [
    [1,5,3,0,2,4], [0,2,1,3,5,4]
]

hijo1 = [-1] * 6
hijo2 = [-1] * 6

tributo1 = 0
tributo2 = 1
#iniciamos proceso para hijo 1 y 2
hijo1[0] = lista_poblacion[tributo1][0]
indice = lista_poblacion[tributo2].index(hijo1[0]) #indice que se usara para mutar el primer hijo
#hijo 2
hijo2[0] = lista_poblacion[tributo2][0]
indice_h2 = lista_poblacion[tributo1].index(hijo2[0])#indice que se usara para mutar el segundo hijo

for j in range(1):

    #mientras que no se repita un valor
    while hijo1[indice] == -1:
        hijo1[indice] = lista_poblacion[tributo1][indice]
        indice2 = lista_poblacion[tributo2].index(hijo1[indice])
        indice = indice2
    
    while hijo2[indice_h2] == -1:
        hijo2[indice_h2] = lista_poblacion[tributo2][indice_h2]
        indice_2h2 = lista_poblacion[tributo1].index(hijo2[indice_h2])
        indice_h2 = indice_2h2

    for padre in range(6):
        #print('entro')
        #print(hijo1[padre])
        if hijo1[padre] == -1:
            hijo1[padre] = lista_poblacion[tributo2][padre]

        if hijo2[padre] == -1:
            hijo2[padre] = lista_poblacion[tributo1][padre]
    

print(hijo1)
print(hijo2)
