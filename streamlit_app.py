# -*- coding: utf-8 -*-

import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

# Funcoes

def similaridade_sentencas(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    v1 = [0] * len(all_words)
    v2 = [0] * len(all_words)
 
    # vetor da 1a sentenca
    for w in sent1:
        if w in stopwords:
            continue
        v1[all_words.index(w)] += 1
 
    # vetor da 2a sentenca
    for w in sent2:
        if w in stopwords:
            continue
        v2[all_words.index(w)] += 1
 
    return(1 - cosine_distance(v1, v2))


def matriz_similaridade(sentences, stop_words):
    M = np.zeros((len(sentences), len(sentences)))
 
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j: 
                continue 
            M[i][j] = similaridade_sentencas(sentences[i], sentences[j], stop_words)

    return M


def sumarizar_texto(text, idioma, top_n):
    if(len(text) == 0):
        return
    else:
        if(idioma == "English"):
            nltk.download("stopwords")
            stop_words = stopwords.words('english')
        else:
            nltk.download("stopwords")
            stop_words = stopwords.words('portuguese')
            
        texto_sumarizado = []
    
        sentences =  text
    
        # Gera matriz de similaridade das sentencas
        M_similaridade = matriz_similaridade(sentences, stop_words)
    
        # Faz o rank das sentencas da matriz de similaridade
        G_similaridade = nx.from_numpy_array(M_similaridade)
        scores = nx.pagerank(G_similaridade)
    
        # Ordenacao para selecionar as sentencas que tem os maiores scores
        ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)        
    
        for i in range(top_n):
          texto_sumarizado.append("".join(ranked_sentence[i][1]))
    
        st.write(" ".join(texto_sumarizado))
        

# streamlit page

with st.sidebar:
    st.markdown("""
    # Sobre o app 
    O Sumarizador de Textos permite extrair os pontos mais importantes de um texto. Aplicação de Processamento de Linguagem Natural com a utilização dos pacotes nltk e networkx.
    """)
   
    st.markdown("""
    # Como funciona
    Coloque o seu texto na área indicada, selecione o idioma e o número de sentenças que deseja no texto sumarizado e clique em Submit para sumarizar o texto.
    """)
    
    st.markdown("""         
    [Source code](https://github.com/gustavo-andrade-tavares/Sumarizador_de_textos)
    """,
    unsafe_allow_html=True,
    )
    
    st.markdown("""
    Feito por **Gustavo Andrade Tavares**
    """
    )
    
st.title('Sumarizador de texto')

k = 0
with st.form("my_form"):
    txt = st.text_area('Coloque o texto aqui (pular uma linha a cada parágrafo):', '', height = 500)
    txt = txt.replace("\n", " ")  
    L = txt.split('. ')
    for i in range(len(L)-1):
        L[i] = L[i]+"."
    idioma = st.radio(
       "Selecione o idioma do texto:",
       ('English', 'Portuguese'))
    n = st.selectbox(
       "Número de sentenças que deseja no texto resumido:",
       (2, 3, 4, 5))

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if(submitted and (len(txt) > 0)):
        k = 1

       
       
st.subheader("Texto sumarizado:")
if(k == 1):
    sumarizar_texto(L,idioma,n)
else:
    st.write("O texto sumarizado aparecerá aqui.")