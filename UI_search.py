# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import cv2
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk
from deep_learning import Deep_Learning
import database
import os, sys

class UI_class:
    def __init__(self, master):
        self.master = master
        self.database_image_ids = database.get_image_ids()
        self.limit = 10
        topframe = Frame(self.master)
        topframe.pack()

        #Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton= Button(topframe, text=" Choose an image ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ", command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=2)
        downspace = Label(topframe).grid(row=3, columnspan=4)

        self.master.mainloop()

    def browse_query_img(self):

        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(title='Choose an Image File').name

        # process query image to feature vector
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))
        # load the query image and describe it
        query = cv2.imread(self.filename)
        self.queryfeatures = cd.describe(query)

        # show query image
        image_file = Image.open(self.filename)
        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(resized)
        image_label = Label(self.query_img_frame, image=im)
        image_label.pack()

        self.query_img_frame.mainloop()


    def show_results_imgs(self):
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()

        results = {}
        # perform the search
        # feature 1: color histogram
        # feature 2: deep learning
        hyper_parameter = [0.2, 0.8]
        
        searcher = Searcher("./color_hist.csv")
        deep_learning = Deep_Learning("./deep_learning.csv")
        
        color_hist_dict = searcher.search(self.queryfeatures)
        deep_learning_dict = deep_learning.search_deeplearning(os.path.abspath(self.filename))
        
        #combine feature vectors here in a results array
        for name in self.database_image_ids:
            results[name] = hyper_parameter[0] * color_hist_dict[name] + hyper_parameter[1] * deep_learning_dict[name]  

        #sort results and show only top 10
        results = sorted([(v, k) for (k, v) in results.items()])
        results = results[:self.limit]

        # show result pictures
        COLUMNS = 5
        image_count = 0
        image_paths = database.get_image_paths()
        for (score, resultID) in results:
            # load the result image and display it
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)
            for image in image_paths:
                if os.path.exists(image + "/" + resultID):
                    im = Image.open(image + "/" + resultID)
            
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.result_img_frame, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=r, column=c)

        self.result_img_frame.mainloop()


root = Tk()
window = UI_class(root)