import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join('..')))


class Names:    
    def __init__(self):
        self._common_mistake_names = ['nao', 'de', 'mail', 'dia', 'dias', 'ira', 'branco', 'vale', 'analise', 'ultima', 'irei', 'sido', 'bom', 'ir', 'ce', 'nada', 'seu', 'domicilio', 'demora', 'sabia', 'ao']
    
    def process_names_dataset(self, dataset_path: str, ignore=[], save_as_csv=True):
        df = pd.read_csv(dataset_path)
        processed_dataset = {'names': []}

        for _, row in df.iterrows():
            if isinstance(row['alternative_names'], str):
                for name in row['alternative_names'].split(sep="|"):
                    if not name.lower() in ignore:
                        processed_dataset['names'].append(name.lower())

            if not row['first_name'].lower() in ignore:
                processed_dataset['names'].append(row['first_name'].lower())

            if not row['group_name'].lower() in ignore:
                processed_dataset['names'].append(row['group_name'].lower())
        
        processed_df = pd.DataFrame.from_dict(processed_dataset)

        if save_as_csv:
            processed_df.to_csv('../data/processed_names.csv', index=False)

        return processed_df

    def change_nouns_data(self, df_sentences: pd.DataFrame, df_names:pd.DataFrame, change_word=""):
        # Cria-se uma cópia do data frame para não alterar ele diretamente:
        df_aux = df_sentences.copy()
        names = df_names['names'].tolist()
        
        for index_row, row in df_aux.iterrows():
            # Separa a frase em uma lista de palavras:
            sentence_words = row['frases'].split(' ')
            # Muda todos os nomes que estejam presentes na frase:
            for index_word, word in enumerate(sentence_words):
                if word.lower() in names:
                    print(sentence_words[index_word])
                    sentence_words[index_word] = change_word         
            
            # Remove qualquer palavra vazia que tenha ficado na lista de palavras:
            # OBS.: remove-se do final para o inicio para que uma remoção não impacte no índice das remoções subsequentes:
            reverse_index = len(sentence_words) - 1
            for word in sorted(sentence_words, reverse=True):
                if word == '':
                    sentence_words.pop(reverse_index)
                # decremento do índice:
                reverse_index -= 1

            #print(" ".join(sentence_words))
            # É substituido a frase alterada no data frame
            df_aux.at[index_row, 'frases'] = " ".join(sentence_words)
        
        return df_aux

    # Substitui os nomes próprios por uma palavra definida usando o spacy:
    def change_nouns_spacy(self, df: pd.DataFrame, change_word=""):
        # Cria-se uma cópia do data frame para não alterar ele diretamente:
        df_aux = df.copy()
        # Instancia um objeto de Natural Language Processing do Spacy
        # com o pacote de pt_core_news_lg
        # OBS.: para utilizar esse pacote é necessário possuir a versão do Spacy 2.3.0 
        #       ou superior e fazer o download dele através do comando:
        #       python -m spacy download pt_core_news_lg
        nlp = spacy.load('pt_core_news_lg')
        
        for index_row, row in df_aux.iterrows():
            # Separa a frase em uma lista de palavras:
            sentence_words = row['frases'].split(' ')
            # Limpa as palavras que são um marcador entre <>
            for index_word, word in enumerate(sentence_words):
                if len(word) > 1 and word[0] == "<" and word[-1] == ">":
                    sentence_words.pop(index_word)
            # Une-se novamente a lista de palavras em uma frase
            sentence = " ".join(sentence_words)

            # Extrai as classe gramaticais das palavras e separa o texto:
            doc = nlp(sentence)
            # Cria-se uma nova lista para armazenar as palavras:
            sentence_words = []
            # Substitui todos os nomes próprios checando sua classe gramatical:
            for token in doc:
                if token.pos_ == "PROPN":
                    print(token.orth_)
                    word = change_word
                else:
                    word = token.orth_
                # Ingnora caso a palavra esteja vazia para não gerar espaços duplos:
                if not word == "":
                    # Salva as palavras na lista:
                    sentence_words.append(word)
            
            # É substituido a frase alterada no data frame
            df_aux.at[index_row, 'frases'] = " ".join(sentence_words)
        
        return df_aux

#Names().process_names_dataset('../data/nomes_proprios.csv', ignore=Names()._common_mistake_names)
#Names().change_nouns_data(pd.read_csv("../NLP/base_chatbot.csv"), pd.read_csv('../data/processed_names.csv'))