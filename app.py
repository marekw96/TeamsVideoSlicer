from tkinter import *
from tkinter import filedialog, Image

import cv2
from PIL import Image, ImageFilter, ImageTk
from slicer import *

class App(Frame):
    def __init__(self):
        Frame.__init__(self)
        self._init_variables()
        self._init_UI()

    def _init_UI(self):
        self.master.title("Video slicer")
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        Label(self, text="Selected video:").grid(column=0, row=0, sticky=W)
        self.file_name_label = Label(self, text="")
        self.file_name_label.grid(column=1, row=0, sticky=W)
        Button(self, text="Select input file", command=self._load_file_name).grid(column=2, row=0, sticky=E)

        self.canvas = Canvas(self, width=400, height=300)
        self.canvas.grid(column=0, row=1, columnspan=2)
        #self.canvas.pack()

        Label(self, text="Start at:").grid(column=0, row=2)
        self.start_frame_entry = Entry(self, textvariable=self.start_frame)
        self.start_frame_entry.grid(column=1, row=2)


    def _change_start_frame(self, args):
        pass

    def _init_variables(self):
        self.input_file = ""
        self.start_frame = 0

    def _update_frame(self):
        if len(self.input_file) == 0:
            return

        capture = cv2.VideoCapture(self.input_file)
        if not capture.isOpened():
            raise RuntimeError("Failed to open {}".format(self.input_file))

        capture.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)
        ret, self.frame = capture.read()
        self.preview = frame_to_image(self.frame)
        self.preview = self.preview.resize((800, 600), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.preview)
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.image)

    def _load_file_name(self):
        file_name = filedialog.askopenfilename(filetypes=(("Video", "*.avi; *.mp4"), ("All files", "*.*")))
        if file_name:
            self.input_file = file_name
            self.file_name_label.config(text=self.input_file)
            self._update_frame()



if __name__ == "__main__":
    App().mainloop()