# -*- coding: utf-8 -*-
'''
Script to generate IBM TTS data
'''
import os
import numpy as np
import pandas as pd


apikey = 'Vt_SAR6Mdpk31Wioi0kZrohPceNZE77dW0rIwaBARGwH'
# url = 'https://gateway-lon.watsonplatform.net/text-to-speech/api'

path = '../data/stimuli_list/stimuli_list_english_TEST.csv'
files = list(i.split('/')[-1][:-4] for i in list(pd.read_csv(path)['file']))
# English voices
# voices = ['en-US_AllisonVoice', 'en-US_MichaelVoice', 'en-GB_KateVoice']
# Japanese voices
#voices = ['ja-JP_EmiVoice']

for i, f in enumerate(files):
	print(f)
	os.system(("./get_ibm_sst.sh"+" "+f).encode('utf-8'))

