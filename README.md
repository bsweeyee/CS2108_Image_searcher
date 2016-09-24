# CS2108_Image_searcher

How to use:

1. Go into utils.py under utility folder and change the variables for database_path and query_path to where your path is

2. run "python UI_search.py" in console

3. Window should pop up and search should be able to work

Generating index files:

1. move all the generate index files out from their respective folder into the main folder

2. run the program to get the respective csv files

3. For sift, run the learn.py file by running "python learn.py -d database"

Dependencies:
numpy, scipy, tensorflow, PIL, Tkinter, cv2, glob

Credits:
Deep learning: Tensorflow and the image classification API

https://github.com/tensorflow/tensorflow/blob/master/tensorflow/g3doc/get_started/os_setup.md

Visual Words: Minimal Bag of Words implementaion 

*Can only run properly if using Linux or Windows. sift is not compatible with macOS

https://github.com/shackenberg/Minimal-Bag-of-Visual-Words-Image-Classifier

Color histogram: pyimagesearch region color histogram implementation

http://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/



