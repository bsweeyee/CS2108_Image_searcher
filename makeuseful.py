f_trainingdata = open('trainingdata.svm','r')   
f_output = open('reduced.svm','w')


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
    
for line in f_trainingdata:
    trainingdata = line
    trainingdata = getArray(trainingdata)
    for i in xrange(len(trainingdata)):
        f_output.write(str(trainingdata[i]))
        f_output.write(" ")
    f_output.write('\n')
        
f_trainingdata.close()
f_output.close()