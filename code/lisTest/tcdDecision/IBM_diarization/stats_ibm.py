import json
import os

files = os.listdir('./eng_output_jsons/')
miss = fa = hit = 0
for i,file in enumerate(files):
	with open('./eng_output_jsons/'+file, "r") as fp:
		data = json.load(fp)
		pred = len(set([i['speaker'] for i in data['speaker_labels']]))
		true = int(file[-6])
		if pred<true:
			miss+=1
		elif true==2 and pred==2:
			hit+=1
		elif true==1 and pred>1:
			fa+=1
	print(i)
print('Hit: ',hit,'Miss: ',miss,'FA: ',fa)
