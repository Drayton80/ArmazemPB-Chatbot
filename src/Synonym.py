import re
import os
import sys
import random
import pandas as pd

sys.path.append(os.path.abspath(os.path.join('..')))


class Synonym:
    def __init__(self, synonyms_file_path: str):
        if '.csv' in synonyms_file_path[-4:]:
            self.df = pd.read_csv(synonyms_file_path)
        else:
            self.df = self._convert_to_dataframe(synonyms_file_path, remove_strings=['\n', '©', '/', '{', '°', '&'])

    # Converte o dataset original para o formato de um dataframe 
    def _convert_to_dataframe(self, file_path: str, remove_strings=[], save_as_csv=False, csv_name='th_pt_BR') -> pd.DataFrame:        
        with open(file_path, 'r', encoding='utf-8') as file:
            synonyms = {'word': [], 'synonym category': [], 'synonym': []}
            
            word = None
            synonym_category = None
            
            for line in file:
                if 'UTF-8' in line:
                    continue

                if line.isspace():
                    word = None
                    synonym_category = None
                else:
                    if remove_strings:
                        for string in remove_strings:
                            line = re.sub(r'({0})+'.format(string), '', line)
                    
                    if not word:
                        word = line[ : line.find('|')]
                    else:
                        for synonym in line.split('|'):
                            if '(Sinônimo)' in synonym:
                                synonym_category = synonym[len('(Sinônimo)'):]
                            else:
                                synonyms['word'].append(word)
                                synonyms['synonym category'].append(synonym_category)
                                synonyms['synonym'].append(synonym)
            
            df = pd.DataFrame.from_dict(synonyms)
            
            if save_as_csv:
                df.to_csv('../data/th_pt_BR.csv', index=False)

            return df
    
    # Obtém uma lista de índices de palavras em uma frase de forma aleatória:
    def _words_index_random(self, sentence: str, number_choosed_words: int) -> list:
        sentence_words = sentence.split(' ')        
        words_index = []
        
        for _ in range(min(number_choosed_words, len(sentence_words))):
            random_index = None
            # Faz uma checagem para não obter valores de indices iguais e garante que
            # não sejam pegos um numero além da quantidade total de indices:
            while not random_index or random_index in words_index:
                random_index = random.randint(0, len(sentence_words))

            words_index.append(random_index)
        
        return words_index

    # Utiliza uma certa métrica para obter uma lista de índices de palavras em uma frase:
    def _choose_words_index(self, sentence: str, metric: str, number_choosed_words: int) -> list:
        if metric.lower() == 'random':
            return self._words_index_random(sentence, number_choosed_words)

    # Substitui uma certa porcentagem de palavras por sínonimos em uma frase:
    def switch_words_for_synonyms(self, sentence: str, choosed_words_percentage=0.4) -> str:
        # O número total de índices de palavras que serão trocadas aqui está sendo definido
        # como 25% do total de palavras na sentença:
        number_choosed_words = int(len(sentence.split(' '))*choosed_words_percentage)
        
        switch_indexes = self._choose_words_index(sentence, 'random', number_choosed_words)

        print(switch_indexes)
                   
#Synonym().convert_to_dataframe('../data/th_pt_BR.dat', remove_strings=['\n', '©', '/', '{', '°', '&'], save_as_csv=True)
#Synonym('../data/th_pt_BR.csv').switch_words_for_synonyms("teste do texto feito em diferentes níveis")