import numpy as np
import time
from functions.imChange import imChange
import sounddevice as sd
from functions import walkman
from getch import getch


def playFile(truth, subject, sender=None):
    dictn = {'rest1': 0.5, 'delay': 1.5, 'listen': 1.5}
    t = list()
    t.append(time.time())

    # Load file
    data, fs = walkman.load(truth['path'])
    print('Starting trial {0:s}...'.format(truth['path']))

    # Playing file
    t.append(time.time())  # append time when starts playing
    print('Playing')
    walkman.play(data, fs)

    imChange('keypress')
    print('Keypress...')
    # append time when stops playing
    t.append(time.time())  
    # monitor keypress
    keypress = ord(getch())-ord(str(1))+1
    while keypress > 2: 
        keypress = ord(getch())-ord(str(1))+1
        print(keypress)
    # append time when key is pressed       
    t.append(time.time())  
    # write to file
    with open('recordings/{0:s}/keys.csv'.format(subject), 'a+') as file:
        file.write('{0:d},{1:s},{2:d},{3:s},{4:s},{5:5.2f},{6:5.3f},{7:5.3f}\n'.format(truth['prompt'],
                                                    truth['path'], truth['npkr'], str(keypress), truth['trial'], t[1]-t[0], t[2]-t[0], t[3]-t[0]))
    # give feedback
    if keypress == truth['npkr']:
        imChange('correct')
        score = 1
    else:
        imChange('wrong')
        score = 0
    time.sleep(1)
    imChange('blank')  # trial ends
    return score