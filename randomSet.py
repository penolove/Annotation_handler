from random import shuffle
import glob

dirPath='../Annotations/'

fileID=glob.glob(dirPath+"*.xml")

x=[i.split('/')[2].replace('.xml','') for i in fileID]

shuffle(x)
trainRatio=0.95
trainSize=int(len(x)*trainRatio)

#train
f=open('Main/trainval.txt','w')
for i in x[:trainSize]:
    f.write(i+'\n')
f.close()

#test

f=open('Main/test.txt','w')
for i in x[trainSize:]:
    f.write(i+'\n')
f.close()

