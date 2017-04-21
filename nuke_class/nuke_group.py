#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
#节点类
import os, sys, copy, csv
#sys.path.append (sys.path[0])
#print (sys.path[0])
from nuke_class.single_line import *
from nuke_class.nuke_node import *
from nuke_class.nuke_layout import *
from nuke_class.blank_line import *
#{'main': groupList, 'layerNumInt':1, 'Type':'group'}

def groupVisualization (groupHead, groupBody, groupFoot, LayerNum):
    groupBodyStr = str()
    for groupBodyNode in groupBody:
        if type(groupBodyNode) == list and len(groupBodyNode) == 3: #是列表
            #print(groupBodyNode)
            groupBodyStr = groupVisualization (groupBodyNode[0], groupBodyNode[1],groupBodyNode[2])
        else:    #是节点
            #print(groupBodyNode)
            if groupBodyStr == '':
                groupBodyStr = str(groupBodyNode)
            else:
                groupBodyStr += groupBodyNode
    #print ('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n' + groupBodyStr)
    return groupHead + groupBodyStr + '\n' + ' ' * LayerNum + groupFoot

class nukeGroup (object):
    print('在nukeGroup中')
    def __init__ (self, groupDict):
        self.groupHead = groupDict['main'][0]
        self.name = groupDict['main'][0].Name
        self.groupBody = groupDict['main'][1]
        #print(self.groupBody)
        self.groupFoot = groupDict['main'][-1]
        self.Type = groupDict['Type']
        self.LayerNum = groupDict['layerNumInt']
        #print(groupVisualization (self.groupBody))
        #print (type(groupVisualization (self.groupHead, self.groupBody, self.groupFoot)))
        self.Str = groupVisualization (self.groupHead, self.groupBody, self.groupFoot, self.LayerNum)



    def __str__ (self):
        return self.Str

    def __repr__ (self):
        return self.__str__()

    def __add__ (self, addObj):
        #print ('G++++')
        #+
        if type(addObj) == str:
            addStr = self.Str + '\n' + addObj
            return addStr
        elif type(addObj) == type(self) or type(addObj) == nukeNode or type(addObj) == classSingleLine or type(addObj) == steplessSingleLine or type(addObj) == blankLine or type(addObj) == nukeLayout:
            #print ('addObj==nukeGroup')
            addStr = self.Str + '\n' + addObj.Str
            return addStr
        else:
            print ('只能输入nukeNode,nukeGroup,singleLine和字符串和整数类型的参数')

    def __radd__ (self, addObj):
        #print ('GR+++')
        #print ('((((' + addObj)
        if type(addObj) == str:
            addStr = addObj + '\n' + self.Str
            return addStr
        
        elif type(addObj) == type(self) or type(addObj) == nukeNode or type(addObj) == classSingleLine or type(addObj) == steplessSingleLine or type(addObj) == blankLine or type(addObj) == nukeLayout:
            #这一段有问题
            addStr = addObj.Str + '\n' + self.Str
            return addStr
        else:
            print ('只能输入nukeNode,nukeGroup,singleLine和字符串和整数类型的参数')
    def __len__ (self):
        return len(self.groupBody)
    
    #替换组内某个节点
    def replaceNode (self, replaceObj, Keytuple):    #replaceObj是要替换过来的组, Keytuple是一个有两个元素的元组,用来作为参照标记
        Index = -1
        for aNode in self.groupBody:
            Index += 1
            if Keytuple[1] == aNode[Keytuple[0]]:
                newSelf = self
                newSelf.groupBody[Index] = replaceObj    #为了不破坏原实例
                return newSelf
            else:
                print ('没找到对应节点')