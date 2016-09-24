# import the necessary packages
import os, sys
import cv2
import tkFileDialog
import utility.util as util
import math
import SIFTquery as sift

from Tkinter import *
from colorhistogram.colordescriptor import ColorDescriptor
from colorhistogram.searcher import Searcher
from PIL import Image, ImageTk
from deeplearning.deep_learning import Deep_Learning
from texttags.text_tags import TextTags

class UI_class:
    def __init__(self, master):
        self.master = master
        self.database_image_ids = util.get_image_ids(util.database_path)
        self.limit = 16
        topframe = Frame(self.master, padx=240)
        topframe.pack()

        #query and result img frame
        self.query_img_frame = 0
        self.result_img_frame = 0

        #checkbox variables
        self.color_var = IntVar()
        self.deep_learning_var = IntVar()
        self.visual_words_var = IntVar()
        self.text_tags_var = IntVar()

        #hyper parameter variables
        self.color_parameter = StringVar()
        self.deep_learning_parameter = StringVar()
        self.visual_words_parameter = StringVar()
        self.text_tags_parameter = StringVar()

        #Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton= Button(topframe, text=" Choose an image ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=2)
        self.cbutton = Button(topframe, text=" Search ", command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=3)

        #CheckBoxes
        self.cbox_color = Checkbutton(topframe, text="Color histogram", variable=self.color_var, onvalue=1, offvalue=0)
        self.cbox_color.grid(row=2, column=1)
        self.cbox_deep_learning = Checkbutton(topframe, text="Deep learning", variable=self.deep_learning_var, onvalue=1, offvalue=0)
        self.cbox_deep_learning.grid(row=2, column=2)
        self.cbox_visual_words = Checkbutton(topframe, text="Visual Words", variable=self.visual_words_var, onvalue=1, offvalue=0)
        self.cbox_visual_words.grid(row=2, column=3)
        self.cbox_text_tags = Checkbutton(topframe, text="Text tags", variable=self.text_tags_var, onvalue=1, offvalue=0)
        self.cbox_text_tags.grid(row=2, column=4)

        #Parameter labels
        self.pbox_color = Entry(topframe, textvariable=self.color_parameter, width=10)
        self.pbox_color.grid(row=3, column=1)
        self.pbox_deep_learning = Entry(topframe, textvariable=self.deep_learning_parameter, width=10)
        self.pbox_deep_learning.grid(row=3, column=2)
        self.pbox_visual_words = Entry(topframe, textvariable=self.visual_words_parameter, width=10)
        self.pbox_visual_words.grid(row=3, column=3)
        self.pbox_text_tags = Entry(topframe, textvariable=self.text_tags_parameter, width=10)
        self.pbox_text_tags.grid(row=3, column=4)

        downspace = Label(topframe).grid(row=5, columnspan=4)

        #Feature objects
        self.color_hist = Searcher("./color_hist.csv")
        self.deep_learning = Deep_Learning("./deep_learning.csv")
        self.text_tag = TextTags("./tag_text_database.csv", "./tag_text_query.csv")

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

        # find query tags
        query_tags = []
        if self.text_tag.return_query_tags(self.filename):
            query_tags = self.text_tag.return_query_tags(os.path.abspath(self.filename))

        # show query image
        image_file = Image.open(self.filename)
        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(resized)
        image_label = Label(self.query_img_frame, image=im)

        # show query tags
        if query_tags:
            image_tags = Label(self.query_img_frame, text="This image has query tags!")
            image_tags.pack()
        else:
            image_tags = Label(self.query_img_frame, text="This image has no query tags!\n\n Selecting text tags search will not result in a search in text tags")
            image_tags.pack()

        image_label.pack()


        self.query_img_frame.mainloop()

    def show_results_imgs(self):
        if (self.result_img_frame != 0):
            self.result_img_frame.destroy()
        
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()

        results = self.get_search_results()

        # show result pictures
        COLUMNS = 4
        image_count = 0
        image_paths = util.get_image_group_paths(util.database_path)
       
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

    def check_hyper_parameters(self):
        # perform the search
        # feature 1: color histogram
        # feature 2: deep learning
        # feature 3: text tag
        # feature 4: visual words
        self.hyper_parameter = [0.1, 0.6, 0.1, 0.2]

        if self.color_parameter.get():
            color_param = float(self.color_parameter.get())
        if self.deep_learning_parameter.get():
            deep_learning_param = float(self.deep_learning_parameter.get())
        if self.text_tags_parameter.get():
            text_tag_param = float(self.text_tags_parameter.get())

        if (self.color_parameter.get() and self.deep_learning_parameter.get() and self.text_tags_parameter.get() and self.visual_words_parameter.get()):
            if (math.fabs(1 - (color_param + deep_learning_param + text_tag_param + visual_words_param)) < 0.0000001):
                self.hyper_parameter[0] = color_param
                self.hyper_parameter[1] = deep_learning_param
                self.hyper_parameter[2] = text_tag_param
                self.hyper_parameter[3] = visual_words_param      

    def get_search_results(self):
        results = {}
       
        color_hist_dict = {}
        deep_learning_dict = {}
        text_tags_dict = {}
        visual_words_dict = {}

        self.check_hyper_parameters()
        
        # do dictionary extraction here
        if (self.color_var.get() == 1):
             # process query image to feature vector
            # initialize the image descriptor
            cd = ColorDescriptor((8, 12, 3))
            # load the query image and describe it
            query = cv2.imread(self.filename)
            self.queryfeatures = cd.describe(query)
            color_hist_dict = self.color_hist.search(self.queryfeatures)
        
        if (self.deep_learning_var.get() == 1):
            deep_learning_dict = self.deep_learning.search_deeplearning(os.path.abspath(self.filename))

        # checkbox must be checked and there must be query tags before search is done
        if (self.text_tags_var.get() == 1 and self.text_tag.return_query_tags(self.filename)):
            text_tags_dict = self.text_tag.tags_search(self.filename)

        # run visual words
        if (self.visual_words_var.get() == 1):
            visual_words_dict = sift.newQuery(os.path.abspath(self.filename))

        #combine feature vectors here in a results array
        # if 0 should, should still be shown since it means they are exactly the same
        # if -1, then should be removed from array
        for name in self.database_image_ids:
            results[name] = -1
            if color_hist_dict:
                if results[name] < 0:
                    results[name] = 0
                results[name] += self.hyper_parameter[0] * color_hist_dict[name]
            if deep_learning_dict:
                if results[name] < 0:
                    results[name] = 0
                results[name] += self.hyper_parameter[1] * deep_learning_dict[name]
            if text_tags_dict:
                if results[name] < 0:
                    results[name] = 0
                results[name] += self.hyper_parameter[2] * text_tags_dict[name]
            if visual_words_dict:
                if results[name] < 0:
                    results[name] = 0
                results[name] += self.hyper_parameter[3] * visual_words_dict[name]


        #sort results and show only top 16
        if (len(results) > 0):
            results = sorted([(v, k) for (k, v) in results.items()])
            results = results[:self.limit]
        
        # makes sure that any element which do not have a valid score is removed from results
        for element in results:
            if element[0] < 0:
                results.remove(element)

        return results

    # return image results from search
    def get_image_search_results(self, file_path, color_var=0, deep_learning_var=0, text_tags_var=0, visual_words_var=0):
        self.filename = file_path
        self.color_var.set(color_var)
        self.deep_learning_var.set(deep_learning_var)
        self.text_tags_var.set(text_tags_var)
        self.visual_words_var.set(visual_words_var)
        return self.get_search_results()
        

root = Tk()
window = UI_class(root)