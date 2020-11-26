# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 14:46:11 2020

@author: Personal
"""
from IPython.display import display 
import pandas as pd 
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import re
import matplotlib.pyplot as plt

# =============================================================================
# Autenticación y Acceso
# =============================================================================

consumerKey = '1J1lYFCMU7pVAnlgrNXUmMvhy'
consumerSecret = 'fXjAUgHUyZqYin1U4qb558qsOGKNV931dW9zWbtKxjyMNmx7yq'
accessToken = '1331042611776393221-PukMWpDCutVzL44URSQZL38k3zskJf'
accessTokenSecret = 'smG5zzH7UrOjWnZz5ofGjl8aN9ghRiKq5VR9c8F4cy0tK'

# Objeto de autenticación
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)     
# Determinar tokens
authenticate.set_access_token(accessToken, accessTokenSecret)     
# Objeto API para inicializar OAuth
api = tweepy.API(authenticate, wait_on_rate_limit = True)

# =============================================================================
# Extracción
# =============================================================================

class datos(object):
    
    def __init__(self, user, n=200, idiom = 'en'):
        
        self.dat = api.user_timeline(screen_name = user, count = n, 
                                lang = idiom, tweet_mode = 'extended')
        self.user = user
        
        self.n = n
        #self.dat = self.dat.translate({ord(j) : None for j in '#@\/\\+'})   
        
    def muestra(self):
        
        print('Muestra de los primeros 5 tweets extraidos de la cuenta @'+self.user+' :\n')
        for i in self.dat[:5]:
            print('- '+ i.full_text + '\n')
    
    def Visualizar(self):
        def limpiar(data):
            data = re.sub(r'#', '', data)
            data = re.sub(r'@[A-Za-z0–9]+', '', data)
            data = re.sub(r'RT[\s]+', '', data)
            data = re.sub(r'https?:\/\/\S+', '', data)
            
            return data
        
        def Subjetividad(data):
            return TextBlob(data).sentiment.subjectivity
        def Polaridad(data):
            return TextBlob(data).sentiment.polarity 
        def sentimiento(valor):
            
            if valor > 0:
              return 'Positivo'
          
            elif valor < 0:
              return 'Negativo'
          
            elif valor == 0:
              return 'Neutro' 
        
        
        df = pd.DataFrame([i.full_text for i in self.dat], columns=['Tweets'], 
                          index = [i for i in range(1,self.n+1)])
        df['Tweets'] = df['Tweets'].apply(limpiar)
        df['Subjetividad'] = df['Tweets'].apply(Subjetividad)
        df['Polaridad'] = df['Tweets'].apply(Polaridad)
        df['Sentimiento'] = df['Polaridad'].apply(sentimiento)
        
        return df

# =============================================================================
# Analisis
# =============================================================================

def nube(data):
    palabras = ' '.join([i for i in data['Tweets']])
    nube = WordCloud(width=700, height=500, max_font_size=100, 
                     max_words= 215, min_word_length= 5, colormap = 'autumn').generate(palabras)
    
    
    plt.imshow(nube, interpolation='spline16')
    plt.axis('off')
    return plt.show()


def sorteo(data):
    v = input('Seleccióne p para el listado de tweets postivos o n para los negativos, a para ambos:\n')
    sortneg = data.sort_values(by=['Polaridad'],ascending=False) 
    sortpos = data.sort_values(by=['Polaridad'])
    
    print()
    try:
        while True:
            if v == 'n':
                print('Tweets negativos:\n\n')
                j=1
                for i in range(1, sortneg.shape[0] ):
                  if( sortneg['Sentimiento'][i] == 'Negativo'):
                    print(str(j)+'. ' + sortneg['Tweets'][i] + '\n')
                    j+=1
                break
                    
                    
            elif v == 'p':
                print('Tweets positivos:\n\n')
                j=1
                for i in range(1, sortneg.shape[0] ):
                  if( sortpos['Sentimiento'][i] == 'Positivo'):
                    print(str(j)+'. ' + sortneg['Tweets'][i] + '\n')
                    j+=1
                break
            
            elif v=='a':
                print('Tweets negativos:\n\n')
                j=1
                for i in range(1, sortneg.shape[0] ):
                  if( sortneg['Sentimiento'][i] == 'Negativo'):
                    print(str(j)+'. ' + sortneg['Tweets'][i] + '\n')
                    j+=1
                
                print()
                print('Tweets positivos:\n\n')
                l=1
                for i in range(1, sortneg.shape[0] ):
                  if( sortpos['Sentimiento'][i] == 'Positivo'):
                    print(str(l)+'. ' + sortneg['Tweets'][i] + '\n')
                    l+=1
                break
    except :
        print('Por favor, inserte un carácter valido.')

def graf(data,user):      
    p = data[data.Sentimiento == 'Positivo']
    p = p['Tweets']  
    
    neg = data[data.Sentimiento == 'Negativo']
    neg = neg['Tweets']  
    
    n = data[data.Sentimiento == 'Neutro']
    n = n['Tweets']  
    
    vals = [(p.shape[0] / data.shape[0])*100, (n.shape[0] / data.shape[0])*100, 
            (neg.shape[0] / data.shape[0])*100]
    
    #plt.figure(figsize=(8,12))
    #fig, axes = plt.subplots(nrows=2, ncols=1)
    plt.style.use('dark_background')
    
    #plt.subplot(2,1,1)
    for i in range(1, data.shape[0]+1):
        if data['Sentimiento'][i] == 'Positivo':
            plt.scatter(data['Polaridad'][i], data['Subjetividad'][i], color='green', s=9.5)
            
        elif data['Sentimiento'][i] == 'Negativo':
            plt.scatter(data['Polaridad'][i], data['Subjetividad'][i], color='red', s=9.5)
            
        elif data['Sentimiento'][i] == 'Neutro':
            plt.scatter(data['Polaridad'][i], data['Subjetividad'][i], color='blue', s=9.5)
      
    plt.title('Analisis sentimental para '+ user) 
    plt.xlabel('Polaridad') 
    plt.ylabel('Subjetividad') 
    plt.show()
    
    #plt.subplot(2,1,2)
    plt.bar(['Positivo', 'Neutro', 'Negativo'], vals, width = 0.2)
    plt.title('Porcentaje del caracter de los Sentimientos')
    plt.xlabel('Sentimiento')
    plt.ylabel('Porcentaje')
    
    #fig.tight_layout(pad=1)
    plt.show()
 
# =============================================================================
# Visualización
# =============================================================================

def ver():
    user = input('Usuario a analizar: ')
    tabla = input('¿Desea ver la tabulación de los datos extraidos?\nSí es así, responda con un si:\n')
    
    print()
    try:   
        while True:
            data = datos(user)
            cuadro = data.Visualizar()
            if tabla == 'si':
                print('Visualización de los comentarios extraidos:')
                display(cuadro)            
            break
    except:
        print('Verifique que el usuario añadido sea uno valido, intentelo de nuevo.')
        
    #sorteo(cuadro)
    #print('A continuación, se le presentara el análisis esquematico de los datos recolectados.')
    #nube(cuadro)
    graf(cuadro, user)

ver()

















