from file_moover import config
import xml.etree.ElementTree as ET
from os import listdir
from os import walk,rename
from os.path import isfile, join, splitext,exists,basename
import shutil


class XML_Converter:
    tree = None
    root = None
    nodes=[]
    path=None

    def __init__(self,path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.nodes=[]
        self.path=path

    def full_convertation(path):
        conv = XML_Converter(path)
        conv.get_nodes_start()
        conv.fcs_to_es_convertion()
        conv.save()

    def get_nodes(self,node):
        for child in node:
            self.nodes.append(child)
            self.get_nodes(child)

    def get_nodes_start(self):
        self.get_nodes(self.root)

    def fcs_to_es_convertion(self):
        for node in self.nodes:
            flag=False
            for atr in node.attrib:
                if atr=='entityId':
                    print(atr)
                    print(node.attrib['entityId'])
                    node.attrib['entityId']=str(node.attrib['entityId']).replace('/asset/','')
                    print(node.attrib['entityId'])
                    flag=True
                    break
            if flag:break

        for node in self.nodes:
            for atr in node.attrib:
                if atr=='dataType':
                    if node.attrib['dataType']=='dateTime':
                        print(node.text)
                        node.text=str(node.text).replace('+0','')
                        print(node.text)

        for node in self.nodes:
            for atr in node.attrib:
                if atr=='dataType':
                    if node.attrib['dataType']=='timecode':
                        print(node.text)
                        node.text=str(node.text).replace('/(25,1)','')
                        print(node.text)

    def save(self):
        self.tree.write(self.path)

class Pair:
    xml=None
    file=None

    def __init__(self,xml,file):
        self.xml=xml
        self.file=file

    def move(self,destination):
        print(self.xml)
        xml_dest=destination+'/'+basename(self.xml)
        print(xml_dest)
        print(self.xml)
        file_dest=destination+'/'+basename(self.file)
        print(file_dest)

        eror=False
        eror|=exists(xml_dest)
        eror|=exists(file_dest)

        if not eror:
            shutil.move(self.file,file_dest)
            shutil.move(self.xml,xml_dest)
        else:
            rename(self.xml,self.file+'.eror')
            rename(self.file,self.file+'.eror')


    def print(self):
        print("pair <")
        print(self.xml)
        print(self.file)
        print('>')

class File_Mover:
    path=None
    destination=None

    def __init__(self,path,destination):
        self.path=path
        self.destination=destination

    def work_cycle(self):

        f = []
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            break
        if config.debug:print('files')
        if config.debug:print(f)

        ff = []
        for p in f:
            ff.append(self.path + '/' + str(p))

        if config.debug:print('paths')
        if config.debug:print(ff)

        f = ff

        xmls = []
        others = []

        for a in f:
            if (splitext(a)[1]) != '':
                if splitext(a)[1] == '.xml':
                    xmls.append(a)
                else:
                    others.append(a)
        if config.debug:print('xmls')
        if config.debug:print(xmls)
        if config.debug:print('others')
        if config.debug:print(others)

        pairs = []
        for xml in xmls:
            for other in others:
                if splitext(xml)[0] == splitext(other)[0]:
                    pairs.append(Pair(xml, other))
                    break
        if config.debug:print('pairs')
        if config.debug:print(pairs)
        for pair in pairs:
            pair.print()
            XML_Converter.full_convertation(pair.xml)
            pair.move(self.destination)








#path='/home/alexdark'
#
#f = []
#for (dirpath, dirnames, filenames) in walk(path):
#    f.extend(filenames)
#    break
#print(f)
#ff=[]
#for p in f:
#    ff.append(path+'/'+str(p))
#print(ff)
#f=ff
#print('+++++++++++++++++++')
#xmls=[]
#others=[]
#
#
#
#
#for a in f:
#    print(splitext(a)[0]+'^'+splitext(a)[1]+'\n')
#    if(splitext(a)[1])!='':
#        if splitext(a)[1]=='.xml':
#            xmls.append(a)
#        else:
#            others.append(a)
#print(xmls)
#print(others)
#
#
#pairs=[]
#for xml in xmls:
#    for other in others:
#        if splitext(xml)[0]==splitext(other)[0]:
#            print(xml+'  '+other)
#            pairs.append(Pair(xml,other))
#            break
#print(pairs)
#for pair in pairs:
#    pair.print()
#    pair.move('/home/alexdark/d')
#
#
#
#
##XML_Converter.full_convertation('/home/alexdark/test.xml')
#