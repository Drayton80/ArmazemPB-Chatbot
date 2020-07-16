import re
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join('..')))



class Synonym: 
    # Converte o dataset original para o formato de um dataframe 
    def convert_to_dataframe(self, file_path: str, remove_strings=[], save_as_csv=False, csv_name='th_pt_BR') -> pd.DataFrame:        
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

                    
#Synonym().convert_to_dataframe('../data/th_pt_BR.dat', remove_strings=['\n', '©', '/', '{', '°', '&'], save_as_csv=True)
