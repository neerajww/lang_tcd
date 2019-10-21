import numpy as np
import time, os, sys
from functions.imChange import imChange
from functions.playFile import playFile
from functions import walkman
from functions.xls2list import xls2list
from functions.takeBreak import takeBreak
import scipy.io as sio
import pandas as pd
from functions.sendTrigger import Sender
from functions.pauser import Pauser
from getch import getch

csv_path = './data/stimuli_list/'

def isTrial():
    if len(sys.argv) > 1:
        if any(x == 'trial' for x in sys.argv[1:]):
            return True
    return False

imChange('blank')
# if open_site: # may be needed for linux os
#     os.system('xdg-open main.html')
os.system('clear')

print('Enter stimuli category (chin/eng): ')
stim_category = '{0:s}'.format(input())
if stim_category == 'chin':
    train_csv_filename = 'stimuli_list_chinese_TRAIN.csv'
    test_csv_filename = 'stimuli_list_chinese_TEST.csv'
elif stim_category == 'eng':
    train_csv_filename = 'stimuli_list_english_TRAIN.csv'
    test_csv_filename = 'stimuli_list_english_TEST.csv'
else:
    print('Check stimilus category!')
    print(1/0)

# Read CSV file using pandas
df = pd.read_csv(csv_path + train_csv_filename)
prompts = df.values
train_stimuli_list = list()
for i in range(len(prompts)):
    train_stimuli_list.append(prompts[i, :])

df = pd.read_csv(csv_path + test_csv_filename)
prompts = df.values
test_stimuli_list = list()
for i in range(len(prompts)):
    test_stimuli_list.append(prompts[i, :])

print('Enter Subject-ID (integer): ')
subject = stim_category+'_'+'S{0:s}'.format(input())
outfolder = 'recordings/{0:s}'.format(subject)
os.system('mkdir -p {0:s}'.format(outfolder))
os.system('rm -rf {0:s}'.format(outfolder)) # removes any existing directory with same subject name
os.system('mkdir -p {0:s}'.format(outfolder)) # creates a new directory

index = 0

print('Please check to see puase.txt that contains Play and not Pause.\nReady...press enter here')
input()
#os.system('python functions/pauser.py &')
#Pauser.checkPause()

start_time = time.time()

print('Press any key to continue...')
imChange('start')
getch()
print('Training session started.')
ntrain = len(train_stimuli_list) # nunber of training stimuli to play
indices_playback = np.random.choice(len(train_stimuli_list), ntrain, False)

# training session begins
imChange('training')
time.sleep(2)
imChange('avoidBlinking')
time.sleep(2)
block_size = 10
block_score = 0

for i in range(len(indices_playback)):
    time.sleep(1.5)
    imChange('fixation')
    Pauser.checkPause()
    print('Prompt no. : {0:d}'.format(i))
    index = indices_playback[i]
    prompt_no = int(train_stimuli_list[index][0])
    n_spkrs = int(train_stimuli_list[index][2])
    filepath = train_stimuli_list[index][1]

    truth = {'prompt': prompt_no, 'path': filepath, 'npkr': n_spkrs, 'trial': 'TRAIN'}
#    trial_score = playFile(truth, subject, sender) # use for WLAN setup
    trial_score = playFile(truth, subject)

    if (i+1) % block_size == 0:  # provide a break
        imChange('break')
        time.sleep(2)
        imChange('resume')
        print('Keypress...')
        keypress = 1
        # check for keypress = 9
        while keypress != 9: 
            keypress = ord(getch())-ord(str(1))+1
        print(keypress)
    
        imChange('avoidBlinking')

# break
imChange('break')
time.sleep(2)
imChange('resume')
print('Keypress...')
keypress = 1
while keypress != 9: 
    keypress = ord(getch())-ord(str(1))+1
print(keypress)
imChange('avoidBlinking')
#while int(float(keypress)) != 9:
#    keypress = getch()
#imChange('avoidBlinking')
print('Testing session started.')
time.sleep(2)
imChange('testing')
time.sleep(2)

ntest = len(test_stimuli_list) # nunber of test stimuli to play
indices_playback = np.random.choice(len(test_stimuli_list), ntest, False)
for i in range(len(indices_playback)):
    time.sleep(1.5)
    imChange('fixation')
    Pauser.checkPause()
    print('Prompt no. : {0:d}'.format(i))
    index = indices_playback[i]
    prompt_no = int(test_stimuli_list[index][0])
    n_spkrs = int(test_stimuli_list[index][2])
    filepath = test_stimuli_list[index][1]  # check in hp

    truth = {'prompt': prompt_no, 'path': filepath, 'npkr': n_spkrs, 'trial': 'TEST'}
#    trial_score = playFile(truth, subject, sender) # use for WLAN setup
    trial_score = playFile(truth, subject)
    block_score = block_score + trial_score

    if (i+1) % block_size == 0:  # provide a break
        imChange('break')
        time.sleep(1.5)

        if block_score == 0:
            imChange('score_0_10')
        if block_score == 1:
            imChange('score_1_10')
        if block_score == 2:
            imChange('score_2_10')
        if block_score == 3:
            imChange('score_3_10')
        if block_score == 4:
            imChange('score_4_10')
        if block_score == 5:
            imChange('score_5_10')
        if block_score == 6:
            imChange('score_6_10')
        if block_score == 7:
            imChange('score_7_10')
        if block_score == 8:
            imChange('score_8_10')
        if block_score == 9:
            imChange('score_9_10')
        if block_score == 10:
            imChange('score_10_10')

        block_score = 0
        time.sleep(1.5)
        imChange('resume')
        print('Keypress...')
        keypress = 1
        while keypress != 9: 
            keypress = ord(getch())-ord(str(1))+1
        imChange('avoidBlinking')

imChange('thankyou')
print('Test complete.')
time.sleep(2)
