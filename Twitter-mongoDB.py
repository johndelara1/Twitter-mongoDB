#!/usr/bin/env python
# coding: utf-8

# ## Preparando a Conexão com o Twitter

# In[ ]:


# Instala o pacote tweepy
get_ipython().system('pip install tweepy')


# In[1]:


# Importando os módulos Tweepy, Datetime e Json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
import json


# Veja no manual em pdf como criar sua API no Twitter e configure as suas chaves abaixo.

# In[2]:


# Adicione aqui sua Consumer Key
consumer_key = "xxxxxxxxx"


# In[3]:


# Adicione aqui sua Consumer Secret 
consumer_secret = "xxxxxxxxx"


# In[4]:


# Adicione aqui seu Access Token
access_token = "xxxxxxxxx"


# In[5]:


# Adicione aqui seu Access Token Secret
access_token_secret = "xxxxxxxxx"


# In[6]:


# Criando as chaves de autenticação
auth = OAuthHandler(consumer_key, consumer_secret)


# In[7]:


auth.set_access_token(access_token, access_token_secret)


# In[8]:


# Criando uma classe para capturar os stream de dados do Twitter e 
# armazenar no MongoDB
class MyListener(StreamListener):
    def on_data(self, dados):
        tweet = json.loads(dados)
        created_at = tweet["created_at"]
        id_str = tweet["id_str"]
        text = tweet["text"]
        obj = {"created_at":created_at,"id_str":id_str,"text":text,}
        tweetind = col.insert_one(obj).inserted_id
        print (obj)
        return True


# In[9]:


# Criando o objeto mylistener
mylistener = MyListener()


# In[10]:


# Criando o objeto mystream
mystream = Stream(auth, listener = mylistener)


# ## Preparando a Conexão com o MongoDB

# In[11]:


# Importando do PyMongo o módulo MongoClient
from pymongo import MongoClient   


# In[12]:


# Criando a conexão ao MongoDB
client = MongoClient('localhost', 27017)


# In[13]:


# Criando o banco de dados twitterdb
db = client.twitterdb


# In[14]:


# Criando a collection "col"
col = db.tweets 


# In[15]:


# Criando uma lista de palavras chave para buscar nos Tweets
keywords = ['Big Data', 'Python', 'Data Mining', 'Data Science']


# ## Coletando os Tweets

# In[16]:


# Iniciando o filtro e gravando os tweets no MongoDB
mystream.filter(track=keywords)


# ## --> Pressione o botão Stop na barra de ferramentas para encerrar a captura dos Tweets

# ## Consultando os Dados no MongoDB

# In[17]:


mystream.disconnect()


# In[18]:


# Verificando um documento no collection
col.find_one()


# ## Análise de Dados com Pandas e Scikit-Learn

# In[19]:


# criando um dataset com dados retornados do MongoDB
dataset = [{"created_at": item["created_at"], "text": item["text"],} for item in col.find()]


# In[20]:


# Importando o módulo Pandas para trabalhar com datasets em Python
import pandas as pd


# In[21]:


# Criando um dataframe a partir do dataset 
df = pd.DataFrame(dataset)


# In[22]:


# Imprimindo o dataframe
df


# In[23]:


# Importando o módulo Scikit Learn
from sklearn.feature_extraction.text import CountVectorizer


# In[24]:


# Usando o método CountVectorizer para criar uma matriz de documentos
cv = CountVectorizer()
count_matrix = cv.fit_transform(df.text)


# In[25]:


# Contando o número de ocorrências das principais palavras em nosso dataset
word_count = pd.DataFrame(cv.get_feature_names(), columns=["word"])
word_count["count"] = count_matrix.sum(axis=0).tolist()[0]
word_count = word_count.sort_values("count", ascending=False).reset_index(drop=True)
word_count[:50]

