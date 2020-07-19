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
    def _words_index_random(self, sentence_words: list, number_choosed_words: int) -> list:
               
        words_index = []
        
        for _ in range(min(number_choosed_words, len(sentence_words))):
            random_index = None
            # Faz uma checagem para não obter valores de indices iguais e garante que
            # não sejam pegos um numero além da quantidade total de indices:
            while not random_index or random_index in words_index:
                random_index = random.randint(0, len(sentence_words)-1)

            words_index.append(random_index)
        
        return words_index

    # Utiliza uma certa métrica para obter uma lista de índices de palavras em uma frase:
    def _choose_words_index(self, sentence_words: str, metric: str, number_choosed_words: int) -> list:
        if metric.lower() == 'random':
            return self._words_index_random(sentence_words, number_choosed_words)

   
    def get_word_synonym(self, word: str) -> str:
        not_letter_start = ''
        not_letter_end = ''
        word_characters = list(word)
        
        # Salva caracteres que não forem letras no inicio e  
        # fim da palavra e remove esses caracteres da palavra:
        for i, character in enumerate(word_characters):           
            if character in ['.', ',', '?', '!', '/', ';', ':', '+', '-']:
                if i == 0:
                    not_letter_start = character
                elif i == len(word_characters)-1:
                    not_letter_end = character

                word_characters[i] = ''

        word_aux = "".join(word_characters)

        all_synonyms = self.df.loc[self.df['word'] == word_aux]

        if not all_synonyms.empty:
            meanings = all_synonyms['synonym category'].unique()
            # Pega o possível significado da palavra, ou seja,
            # a categoria de sinônimos certa para pegar um sinônimo dela:
            word_meaning = meanings[random.randint(0, len(meanings)-1)]
            
            word_synonyms = all_synonyms.loc[all_synonyms['synonym category'] == word_meaning]
            word_synonyms.reset_index(drop=True, inplace=True)

            word_synonym = word_synonyms.at[random.randint(0, len(word_synonyms)-1), 'synonym']
            word_synonym = not_letter_start + word_synonym + not_letter_end
        else:
            word_synonym = word

        return word_synonym

    
    # Substitui uma certa porcentagem de palavras por sínonimos em uma frase:
    def switch_words_for_synonyms(self, sentence: str, choosed_words_percentage=0.4) -> str:
        sentence_words = sentence.split(' ') 
        # O número total de índices de palavras que serão trocadas aqui está sendo definido
        # como uma parcela do total de palavras na sentença:
        number_choosed_words = int(len(sentence_words)*choosed_words_percentage)
        
        switch_indexes = self._choose_words_index(sentence_words, 'random', number_choosed_words)

        for switch_index in switch_indexes:
            sentence_words[switch_index] = self.get_word_synonym(sentence_words[switch_index])

        return " ".join(sentence_words)

                   
#Synonym().convert_to_dataframe('../data/th_pt_BR.dat', remove_strings=['\n', '©', '/', '{', '°', '&'], save_as_csv=True)
sentence = "Como buscar minha compra?"
print(sentence)
print(Synonym('../data/th_pt_BR.csv').switch_words_for_synonyms(sentence))
#Synonym('../data/th_pt_BR.csv').get_word_synonym("abastecido,")