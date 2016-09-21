# import the necessary packages
import os, sys
import cv2
import tkFileDialog
import utility.util as util

from Tkinter import *
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
from PIL import Image, ImageTk
from deeplearning.deep_learning import Deep_Learning

class UI_class:
    def __init__(self, master):
        self.master = master
        self.database_image_ids = util.get_image_ids()
        self.limit = 16
        topframe = Frame(self.master, padx=240)
        topframe.pack()

        #query and result img frame
        self.query_img_frame = 0
        self.result_img_frame = 0

        #checkbox variables
        self.color_var = IntVar()
        self.deep_learning_var = IntVar()

        #Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton= Button(topframe, text=" Choose an image ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ", command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=2)

        self.cbox_color = Checkbutton(topframe, text="Color histogram", variable=self.color_var, onvalue=1, offvalue=0)
        self.cbox_color.grid(row=2, column=1)
        self.cbox_color = Checkbutton(topframe, text="Deep learning", variable=self.deep_learning_var, onvalue=1, offvalue=0)
        self.cbox_color.grid(row=2, column=2)

        downspace = Label(topframe).grid(row=4, columnspan=4)

        #Feature objects
        self.color_hist = Searcher("./color_hist.csv")
        self.deep_learning = Deep_Learning("./deep_learning.csv")

        self.master.mainloop()

    def browse_query_img(self):
        if (self.query_img_frame != 0):
            self.query_img_frame.destroy()

        if (self.result_img_frame != 0):
            self.result_img_frame.destroy()

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
        if (self.result_img_frame != 0):
            self.result_img_frame.destroy()
        
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()

        results = {}
        # perform the search
        # feature 1: color histogram
        # feature 2: deep learning
        hyper_parameter = [0.2, 0.8]
        
        color_hist_dict = {}
        deep_learning_dict = {}
        
        # do dictionary extraction here
        if (self.color_var.get() == 1):
            color_hist_dict = self.color_hist.search(self.queryfeatures)
        
        if (self.deep_learning_var.get() == 1):
            deep_learning_dict = self.deep_learning.search_deeplearning(os.path.abspath(self.filename))


        #combine feature vectors here in a results array
        # if 0 should, should still be shown since it means they are exactly the same
        # if -1, then should be removed from array
        for name in self.database_image_ids:
            results[name] = -1
            if (len(color_hist_dict) > 0):
                if name in color_hist_dict:
                    if results[name] < 0:
                        results[name] = 0
                    results[name] += hyper_parameter[0] * color_hist_dict[name]
            
            if (len(deep_learning_dict) > 0):
                if name in deep_learning_dict:
                    if results[name] < 0:
                        results[name] = 0
                    results[name] += hyper_parameter[1] * deep_learning_dict[name]
            
            if results[name] == -1:
                del results[name]

        #sort results and show only top 10
        if (len(results) > 0):
            results = sorted([(v, k) for (k, v) in results.items()])
            results = results[:self.limit]

        # show result pictures
        COLUMNS = 4
        image_count = 0
        image_paths = util.get_image_paths()

       
        for (score, resultID) in results:
            # load the result image and display it
            if (score >= 0):
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