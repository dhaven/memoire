import Tkinter
import Tkconstants
import tkFileDialog
from client import Client
import sys

class BasicUI(Tkinter.Frame):
    def __init__(self, parent):
        self.client = Client(sys.argv[1])

        Tkinter.Frame.__init__(self, parent, background="white")
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        Tkinter.Button(self, text='upload', command=self.askopenfile).pack(**button_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['filetypes'] = [('', '.png'), ('', '.jpeg')]
        options['initialdir'] = 'C:\\'
        options['parent'] = root
        options['title'] = 'image to upload'
        self.parent = parent
        self.parent.title("cloudImagesUploader")
        self.pack(fill=Tkinter.BOTH, expand=1)

    def askopenfile(self):
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        self.client.sendDataToServer(filename)

if __name__ == '__main__':
    root = Tkinter.Tk()
    root.geometry("350x250+300+300")
    BasicUI(root).pack()
    root.mainloop()