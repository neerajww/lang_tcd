import tkinter as tk
import sys
import time


class Pauser:
    def __init__(self, reload=False):
        root = tk.Tk()
        # root.geometry('500x100')
        frame = tk.Frame(root)
        frame.pack()
        play = tk.Button(frame, text="Play", command=self.unpause)
        play.pack(side=tk.LEFT)
        pause = tk.Button(frame, text="Pause", command=self.pause)
        pause.pack(side=tk.LEFT)
        stop = tk.Button(frame, text="Stop", fg="red", command=self.stop)
        stop.pack(side=tk.LEFT)
        # self.label = tk.Label(root, text=self.getText('pause.txt'))
        # self.label.pack()
        if reload:
            self.pause()
        root.title('Control')
        root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='icon.png'))
        root.mainloop()

    @staticmethod
    def getText(filename):
        with open(filename, 'r+') as file:
            return file.read()

    @staticmethod
    def checkPause():
        with open('pause.txt', 'r+') as file:
            text = file.read()
        while text == 'Pause':
            with open('pause.txt', 'r+') as file:
                text = file.read()
            time.sleep(0.1)
        if text == 'Stop':
                with open('pause.txt', 'w+') as file:
                    text = file.write('Pause')
                sys.exit()

    def pause(self):
        with open('pause.txt', 'w+') as file:
            file.write('Pause')

    def unpause(self):
        with open('pause.txt', 'w+') as file:
            file.write('Play')

    def stop(self):
        with open('pause.txt', 'w+') as file:
            file.write('Stop')
        sys.exit()
    
    def __exit__(self, exc_type, exc_value, traceback):
        print('Exiting')


if __name__ == '__main__':
    pauser = Pauser(reload=True)
