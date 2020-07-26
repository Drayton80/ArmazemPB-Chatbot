import pandas as pd

from os import listdir
from os.path import isfile, join
from functools import reduce
from tqdm import tqdm
import re

path = "Dialogs_PP/"

files = [f for f in listdir(path) if isfile(join(path, f))]

df_total = pd.DataFrame()

found = False

for f in tqdm(files):
	with open(path+f, 'r', encoding='utf-8') as f:
		lines = f.read().split('\n')


	for l in lines:
		#print(l)
		if 'background-color' in l:
			print(f.name)
			found = True
			break
	#break

	if found:
		break

	df = pd.DataFrame(lines)

	df.columns = ['frases']

	df_total = pd.concat([df_total, df]).reset_index(drop=True)

	#print(type(df[df['frases'].str.contains('background-color: rgba238, 238, 238, 0.925;">"')]))

	if not df[df['frases'].str.contains('background-color: rgba238, 238, 238, 0.925;">"')].empty:
		print(f)
		break


indexes_todrop = []

for i in range(len(df_total)):
	if (df_total['frases'].iloc[i] == "" or df_total['frases'].iloc[i] == "voce escolheu <div style" or df_total['frases'].iloc[i] == "rel stylesheet" 
	or df_total['frases'].iloc[i] == "sans extrabold helvetica sans serif" or df_total['frases'].iloc[i] == "script mt cursive"):
		indexes_todrop.append(i)
	if df_total['frases'].iloc[i] == "<span style color":
		df_total.at[i, 'frases'] = df_total['frases'].iloc[i].replace("<span style color", '')
			
df_total.drop(indexes_todrop, inplace = True)

print(df_total.head(10))

#df_total.to_csv('base_chatbot.csv', encoding = 'utf-8')