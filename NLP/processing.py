from os import listdir
from os.path import isfile, join
from functools import reduce
from tqdm import tqdm
import re
from clean_text import clean_text, organiza_des, remove_words

path = "Dialogs/"
output_path = "Dialogs_PP/"

files = [f for f in listdir(path) if isfile(join(path, f))]

for f in tqdm(files):
	with open(path+f, 'r', encoding='utf-8') as f:
		lines = f.read().split('\n')

	aux = []
	aux2 = []

	tags = ["<b>", "</b>", "Ex.:"]

	is_html = False
	html_index = {'start': [], "end": []}

	'''for l in lines:
		print(l)'''

	for i in range(len(lines)):
		#lines[i] = re.sub('[^A-Za-z0-9]+', '', lines[i])
		if is_html:
			if "</style>" in lines[i]:
				is_html = False
				html_index['end'].append(i)
			else:
				continue

		if '<div style=' in lines[i]:
			is_html = True
			html_index['start'].append(i)

		lines[i] = re.sub('[()]', '', lines[i])		

		text = reduce(lambda a, b: a.replace(b, ''), tags, lines[i])
		text = text.lower()

		for ch in ['á','â','ã','à','Á','Â','Ã','À']:
			if ch in text:
				text = text.replace(ch, 'a')
		for ch in ['é','ê', 'É', 'Ê']:
			if ch in text:
				text = text.replace(ch, 'e')
		for ch in ['í', 'Í']:
			if ch in text:
				text = text.replace(ch, 'i')
		for ch in ['ó','ô','õ', 'Ó', 'Ô', 'Õ']:
			if ch in text:
				text = text.replace(ch, 'o')
		for ch in ['ú', 'Ú']:
			if ch in text:
				text = text.replace(ch, 'u')
		for ch in ['ç', 'Ç']:
			if ch in text:
				text = text.replace(ch, 'c')
		
		text = text.split()
		text = text[2:]
		for j in range(len(text)):
			result_pedido = re.search("o[0-9]+", text[j])
			result_cpf = re.match(r'[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$', text[j])
			result_number = re.search("[0-9]+", text[j])
			result_site = re.match("\Ahttp", text[j])
			#text[j] = re.sub('[^A-Za-z0-9]+', '', text[j])

			if result_pedido:
				text[j] = "<PEDIDO>"
			elif result_cpf:
				text[j] = "<CPF>"
			elif result_number:
				text[j] = "<NUMERO>"
			elif result_site:
				text[j] = "<SITE>"
			'''elif len(text[j]) <= 2 and not re.match(r'[A-Za-z0-9]+', text[j]):
				text[j] = ""
			'''

		lines[i] = " ".join(text)
		lines[i] = " ".join(lines[i].split())


		if "target=" in lines[i]:
			text = lines[i].split()
			index = None
			for word in text:
				if "target=" in word:
					index = text.index(word)

			text = ' '.join(text[:index])
			lines[i] = text


	if html_index['start'] and html_index['end']:
		start = html_index['start'][0]
		end = html_index['end'][0]+1
		for i in range(len(html_index['start'])):
			lines = lines[:start] + lines[end:]
			if i < (len(html_index['start']) - 1):
				start = html_index['start'][i + 1] - ((sum(html_index['end'][:i+1])+1) - sum(html_index['start'][:i+1]))
				end = html_index['end'][i + 1] - ((sum(html_index['end'][:i+1])+1) - sum(html_index['start'][:i+1]))

	for j in range(len(lines)):
		lines[j] = clean_text(lines[j])

	'''print('PROCESSADO:', '\n')
	for l in lines:
		print(l)'''

	'''for text in lines:
		print(text, type(text))'''

	if '.txt' in f.name[8:]:
		with open(output_path+'pp_'+f.name[8:], 'w', encoding='utf-8') as f:
			for item in lines:
				f.write(str(item) + "\n")
	else:
		with open(output_path+'pp_'+f.name[8:]+'.txt', 'w', encoding='utf-8') as f:
			for item in lines:
				f.write(str(item) + "\n")


			