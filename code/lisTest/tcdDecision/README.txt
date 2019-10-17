########################## 
This code does:
##########################
# - this is designed for listening test
# - reads a list (from ./data/), plays the audio files (from ./playback/STIMULI/{chineese,english}/wavFilesTest/), asks for a response on number of talkers (keypress 1 or 2), and loops
# - all the responses are stored as a .csv file (at ./recordings/{chin-,eng-,subjectID}/keys.csv)
# - needs Python 3.6 and the imported packages stated in the main code (and the subroutines)
# - the main code is listExp.py
# - to run Open the main.html in a browser. Keep the browser Then and go to terminal >python listExp.py
# - Keep the cursor on the terminal all the while the program is running. The html window is only for a proxy GUI.
# - runs on Mac system (should run on Linux also, please check), all audio files should be of 16-bit
###########################
# - Code was designed by Kiran Praveen.T (LEAP Lab, IISc)
# - Later custom modified by Neeraj Sharma (LEAP Lab, IISc and CMU)
# - Last modified by Neeraj (https://github.com/neerajww) on 16th Oct. 2019
###########################