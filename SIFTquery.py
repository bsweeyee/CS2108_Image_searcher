import argparse
import os
import utility.util as util
import math

'''def parse_arguments():
    parser = argparse.ArgumentParser(description='generate top 16 similar images given a query')
    parser.add_argument('-q', help='path to the codebook file', required=False, default='query/alley/0001_439648413')
    args = parser.parse_args()
    return args
'''
DATABASEPATH =  "database"

def newQuery(img_path):
    img_path = "python classify.py " + img_path
    os.system(img_path)
    
    #read testdata.svm into query_array
    f_testdata = open('testdata.svm','r')
    testdata = f_testdata.readline();
    testdata = getArray(testdata)
    f_testdata.close()

    #for each line in trainingdata.svm read values into training_array
    f_trainingdata = open('trainingdata.svm','r')
    distances = []

    for line in f_trainingdata:
        trainingdata = line
        trainingdata = getArray(trainingdata)
        distances.append(euclidDist(testdata,trainingdata))
        
    f_trainingdata.close()

    #load all jpg paths into f_names
    f_names = util.get_image_ids(util.database_path)
    
    dictionary = {}
    dictionary = dict(zip(f_names, distances))
    
    return dictionary
    
def euclidDist(testset, trainingset):
    sum = 0
    for i in range(len(testset)):
        sum += (testset[i] - trainingset[i])**2
    return math.sqrt(sum)
    
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
        

def getArray(list):
    list = list.replace(':', ' ')
    list = list.split()
    list = map(float,list)
    list.remove(list[0])
    
    for value in list:
        if(isInt(value)):
            list.remove(value)
    return list
    
#enter query
"""args = parse_arguments()
newQuery(args.q)"""



