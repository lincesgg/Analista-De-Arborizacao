import  cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import mahotas
from tkinter import*
import os
import os.path
from matplotlib import pyplot as plt
import colorsys


#Função para arredondar numeros reais
def arredondar(num):
    return float( '%g' % ( num ) )
#Função para facilitar a escrita nas imagem
def escreve(img, texto, cor=(255,0,0)):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, texto, (10,20), fonte, 0.5, cor, 0, cv2.LINE_AA)

#Calculando a escala
escala = cv2.imread('teste_arvore_nova.jpg')
escalay, escalax, c = escala.shape
area_real = 400
fator_de_escala = (area_real/(escalax*escalax)) # Quanto 1px² representa em m²s
print ("fator de escala e' ",fator_de_escala)
#20m=97pixels=>Área=20m*20m= 400m² =77*77=5929p²
#(400/5929)=>1p² = 0,06746500253m²


# Converter BGR em HSV
img  =  cv2 . imread ( 'teste_arvore_nova_3.png' )
print ("tamanho da imagem de escala é (Altura, Largura, Canais de cor) ",escala.shape)
print ("tamanho da image é (Altura, Largura, Canais de cor) ",img.shape)
filtro=0
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
altura, largura, canais = img.shape

#Inicializando todas as variáveis com 0 ou 255
menor_azul = 255
menor_verde = 255
menor_vermelho = 255
maior_vermelho= 0
maior_verde = 0
maior_azul = 0

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

for y in range (0, altura):
    for x in range (0, largura):
        azul = img.item(y, x, 0)
        verde  = img.item(y, x, 1)
        vermelho = img.item(y, x, 2)

        #Testando qual o maior valor das componentes Verde, Vermelho, Azul.
        if azul > maior_azul:
            maior_azul = azul
        if verde > maior_verde:
            maior_verde = verde
        if vermelho > maior_vermelho:
            maior_vermelho = vermelho
        if azul < menor_azul:
            menor_azul = azul
        if verde < menor_verde:
            menor_verde = verde
        if vermelho < menor_vermelho:
            menor_vermelho = vermelho
            
        #print("["+str(img [y]/altura)*100+"%" "["+str(x)+ ","+str(y)+"] = "+str(img [y][x]))
        print("["+str(x)+ ","+str(y)+"] = "+str(img [y][x]))
        a = np.array([img [y][x]])
        
print("O maior valor da componente R é ", maior_vermelho) 
print("O maior valor da componente G é ", maior_verde)
print("O maior valor da componente B é ", maior_azul)
print("O menor valor da componente R é ", menor_vermelho) 
print("O menor valor da componente G é ", menor_verde)
print("O menor valor da componente B é ", menor_azul)
print(f'(({menor_azul}, {menor_verde}, {menor_vermelho}), ({maior_azul}, {maior_verde}, {maior_vermelho}))')

# PARAMETRIZAÇÃO
r = maior_vermelho/255
g = maior_verde/255
b = maior_azul/255
h, s, v = colorsys.rgb_to_hsv(r, g, b)
h = h*180 # Não deveria ser 360?
s = s*255
v = v*255
print("O maior valor da componente H é ", h)
print("O maior valor da componente S é ", s)
print("O maior valor da componente V é ", v)
r = menor_vermelho/255
g = menor_verde/255
b = menor_azul/255
h, s, v = colorsys.rgb_to_hsv(r, g, b)
h = h*180
s = s*255
v = v*255
print("O menor valor da componente H é ", h) 
print("O menor valor da componente S é ", s)
print("O menor valor da componente V é ", v)

