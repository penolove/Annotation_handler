from random import shuffle
import glob
import os
import xml.etree.ElementTree as ET
import cv2


class annotation_object_extractor(object):
    object_dict=dict()
    def __init__(self,dirPath,jpgPath):
        self.dirPath=dirPath
        self.jpgPath=jpgPath
        target_xml_pattern=os.path.join(dirPath,"*.xml")
        fileID=glob.glob(target_xml_pattern)
        for i in fileID:
            self.updatefromXml(i)

    def updatefromXml(self,filename):
        print "current xml file is :"+  filename
        tree = ET.parse(filename)
        root = tree.getroot()
        objs = tree.findall('object')
        for i in objs:
            result=self.object_dict.get(i.find('name').text.lower().strip(),[])
            if(len(result)==0):
                self.object_dict[i.find('name').text.lower().strip()]=result
            result.append(filename)

    def showCollects(self):
        oblens=[len(i) for i in self.object_dict.values()]
        print zip(self.object_dict.keys(),oblens)

    def get_images(self,target, shape,Write2File=False,File_prefix=''): 
        print "===== writing the target imgs: "+target+" to folder AOE ====="
        if (not os.path.exists('AOE')):
            os.makedirs('AOE')
        image_count=0
        object2handle=self.object_dict.get(target,[])
        if(len(object2handle)!=0):
            object2handle=list(set(object2handle))
            for filename in object2handle:
                tree = ET.parse(filename)
                root = tree.getroot()
                objs = tree.findall('object')
                target_jpg=filename.replace(dirPath,jpgPath).replace('.xml','.jpg')
                img = cv2.imread(target_jpg)
                for i in objs:
                    if(i.find('name').text.lower().strip()==target):
                        bndbox=i.find('bndbox')
                        y= int(bndbox.find('ymin').text)
                        h= int(bndbox.find('ymax').text)-y
                        x= int(bndbox.find('xmin').text)
                        w= int(bndbox.find('xmax').text)-x
                        #print (x,y,w,h)
                        partial_img=img[y:y+h,x:x+w]
                        if(Write2File):
                            if(not os.path.exists(os.path.join('AOE',target))):
                                os.makedirs(os.path.join('AOE',target))
                            cv2.imwrite(os.path.join('AOE',target,File_prefix+str(image_count)+".jpg"),partial_img)
                            image_count+=1
                    #from IPython import embed; embed()
                    #break
        else:
            print "target : "+target +" not found"



dirPath='../Annotations'
jpgPath='../JPEGImages'
AOE=annotation_object_extractor(dirPath,jpgPath)
AOE.showCollects()
#print AOE.object_dict

# write out images
#where me,mh,so,face are the target wanna to write
#AOE.get_images("me",[],True)
#AOE.get_images("mh",[],True)
#AOE.get_images("so",[],True)
#AOE.get_images("face",[],True)

