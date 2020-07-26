import numpy as np
import pandas as pd
import scipy
import sklearn

import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from tqdm import tqdm

from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from collections import defaultdict

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def remove_words(text):
	text = text.strip()
	text = text.lower()
	text = text.split()

	for t in range(len(text)):
		if len(text[t]) == 1 or hasNumbers(text[t]):
			text[t] = text[t].replace(text[t], '')

	text = ' '.join(text)
	text = ' '.join(text.split())

	return text

def clean_text(text):
    ps = PorterStemmer()

    text = text.strip()
    #text = text.lower()
    text = re.sub('[^a-zA-Záâãàéêíóôõúç<>]', ' ', text)   
    unwanted_words = ['lo']

    text = text.split()

    tags = ['<PEDIDO>', '<CPF>', '<NUMERO>', '<SITE>']

    for t in range(len(text)):
        if len(text[t]) == 1 or hasNumbers(text[t]) or text[t] in unwanted_words or text[t] in set(stopwords.words('portuguese')):
            text[t] = text[t].replace(text[t], '')  
        #else:
        #    text[t] = ps.stem(text[t])

    text = ' '.join(text)
    text = ' '.join(text.split())

    '''ps = PorterStemmer()
    text = [ps.stem(word) for word in text.split() if not word in set(stopwords.words('portuguese'))]

    text = ' '.join(text)'''

    return text

def stemming(text):   
    ps = PorterStemmer()
    text = [ps.stem(word) for word in text.split() if not word in set(stopwords.words('portuguese'))]

    text = ' '.join(text)


    return text


def organiza_des(df_entrada, df_entrada_unique, col_nome):
    '''
    Organiza as descrições presentes no DataFrame de compras

    Args:
        df_entrada: Dataframe de entrada
        col_nome: Coluna que será organizada

    Retorna:
        Um DataFrame de descrições, organizadas de tal forma que seja razoável clusterizar.

    '''

    print("Organiza Descrições...")

    unwanted_words = ['g', 'G', 'kg', 'KG', 'ml', 'mL', 'ML', 'Ml']

    # - Cria um DataFrame
    #df_entrada = pd.DataFrame(df_entrada[col_nome].unique(), columns = {col_nome})

    #**Tokenization: Cada entrada de corpo de texto será quebrada num set de palavras**
    #df_entrada[col_nome] = [word_tokenize(entry) for entry in df_entrada[col_nome]]

    # - Transforma em lower case, pois python é sensível a variação de tamanho e stopword é definido em lower case
    df_entrada[col_nome] = [entry.lower() for entry in df_entrada[col_nome]]

    # - Recupera lista de stopwords em Português
    palavras_para = set(stopwords.words('portuguese') + list(punctuation))
    
    # - Conta frequência das palavras para remover aquelas que aparecem apenas uma vez
    frequency = defaultdict(int)
    for index, row in tqdm(df_entrada_unique.iterrows()):
        # - Separa as palavras da frase para percorrer
        frase = (row['descricao']).split()
        for palavra in frase:
            frequency[palavra] += 1

    # - Remove Stopwords e palavras com frequência = 1

    word_set = set()
    for index, row in tqdm(df_entrada.iterrows()):
        # - Separa as palavras da frase para percorrer
        frase = (row[col_nome]).split()
        for palavra in frase:
        # - Varre a frase procurando stopwords
            word_set.add(palavra)   
            if (palavra in palavras_para) or (hasNumbers(palavra)) or (palavra in unwanted_words):
                # - Remove a stopword
                frase.remove(palavra)
                # - Atualiza a row.descrição
                row[col_nome] = ' '.join(frase)

            if frequency[palavra] == 1:
                try:
                    # - Remove a palavra com frequência = 1
                    frase.remove(palavra)
                    # - Atualiza a row.descrição
                    row[col_nome] = ' '.join(frase)
                except:
                    # - Except para quando uma palavra que aparece apenas uma vez já tinha sido removida por ser um stop word
                    pass
            if (len(palavra) == 1):
                try:
                    # - Remove a palavra com frequência = 1
                    frase.remove(palavra)
                    # - Atualiza a row.descrição
                    row[col_nome] = ' '.join(frase)
                except:
                    # - Except para quando uma palavra que aparece apenas uma vez já tinha sido removida por ser um stop word
                    pass

    # - Remove todos os números presentes nas descrições
    df_entrada[col_nome] = df_entrada[col_nome].str.replace('\d+', '')

    # - Remove 'ml' e 'kg' presente nas descrições
    df_entrada[col_nome] = df_entrada.descricao.str.replace('ml' , '')
    df_entrada[col_nome] = df_entrada.descricao.str.replace('kg' , '')
    df_entrada[col_nome] = df_entrada.descricao.str.replace(' g' , '')

    return df_entrada, word_set