# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import praw
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analizador = SentimentIntensityAnalyzer()

#Credenciales importantes
client_id = 'Gz4dxo0jJnDQ8w'
client_secret = 'KsTpI6KoTUFNDSYXv_6piuc2OuQZIQ'
user_agent = 'RedditAnalisisDatos'

reddit = praw.Reddit(client_id ='Gz4dxo0jJnDQ8w',
                     client_secret = 'KsTpI6KoTUFNDSYXv_6piuc2OuQZIQ',
                     user_agent = 'RedditAnalisisDatos',
                     )

def database(subr,keyword):
    sub = reddit.subreddit(subr)

    hot = sub.hot(limit = 50)

    comments = []
    for post in hot:
        post.comments.replace_more(limit=2)
        for toplevel in post.comments:
            if keyword in toplevel.body:
                comments.append(toplevel.body)
    return comments

def nube(data):
    palabras = ' '.join(data)
    nube = WordCloud(width=700, height=500, max_font_size=100, 
                     max_words= 215, min_word_length= 5,
                     colormap = 'turbo').generate(palabras)
    
    
    plt.imshow(nube, interpolation='spline16')
    plt.axis('off')
    return plt.show()

def analisis_sentimientos(data):
    positivos = 0
    negativos = 0
    neutrales = 0
    totales = 0
    for comment in data:
        sentimiento = (analizador.polarity_scores(comment))
        if sentimiento['neg'] < 0.1 :
            if sentimiento['pos']-sentimiento['neg'] > 0.05:
                positivos += 1
        if sentimiento['pos'] < 0.1:
            if sentimiento['pos']-sentimiento['neg'] <= -0.05:
                negativos += 1
        else:
            neutrales +=1
        totales += 1
    
    valores = [(positivos*100/totales), (neutrales*100/totales), (negativos*100/totales)]
            
            
    
    plt.figure(figsize = (8,8))
    fig, axes = plt.subplots(nrows=1, ncols=1)
    plt.style.use('dark_background')
    
    plt.bar(['Positivo', 'Neutro', 'Negativo'], valores, width = 0.2, color = ['green', 'blue', 'red'])
    plt.title(f'Sentimientos hacia la keyword en {len(data)} comentarios')
    plt.xlabel('Sentimiento')
    plt.ylabel('Porcentaje')
    plt.show()
#nube(comments)

analisis_sentimientos(database('politics','Trump'))
