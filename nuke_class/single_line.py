#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
import os, sys, copy
#os.chdir (sys.path[0])
from nuke_class.nuke_node import *
from nuke_class.nuke_group import *
from nuke_class.nuke_layout import *
#singleLine类, 为一个不可变类,为了处理节点以外的单行
#singleLine类有两个之类steplessSingleLine, classSingleLine
class singleLine (object):
    def __init__ (self, singleLineDict):    #导入的对象是一个字典,格式为{'main': (attributeKey, attributeValue), 'layerNumInt':0, 'Type':'push'}
        self.main = singleLineDict['main']
        self.Type = singleLineDict['Type']
        self.LayerNum = singleLineDict['layerNumInt']

#无层级关系单行可能要被合并掉
#无层级关系
class steplessSingleLine (singleLine):
    print('在steplessSingleLine中')
    def __init__ (self, singleLineDict):
        singleLine.__init__ (self, singleLineDict)
        self.freshenStr()

    #添加self.Str属性的函数
    def freshenStr (self):
        if len(self.main) == 1:
            self.Str = self.main[0]
        elif len(self.main) > 1:
            self.Str = ' '.join(self.main)

    def __str__ (self):
        return self.Str

    def __repr__ (self):
        return self.__str__ ()

    def __add__ (self, addObj):
        if type(addObj) == str:
            addNode = self.Str + '\n' + addObj
            return addNode
        elif type(addObj) == type(self) or type(addObj) == nukeNode or type(addObj) == nukeGroup or type(addObj) == nukeLayout or type(addObj) == blankLine or type(addObj) == classSingleLine:
            addNode = self.Str + '\n' + addObj.Str
            return addNode
    
    def __radd__ (self, addObj):
        if type(addObj) == str:
            addNode = addObj + '\n' + self.Str
            return addNode
        elif type(addObj) == type(self) or type(addObj) == nukeNode or type(addObj) == nukeGroup or type(addObj) == nukeLayout or type(addObj) == blankLine or type(addObj) == classSingleLine:
            addNode = addObj.Str + '\n' + self.Str
            return addNode

#有层级关系
class classSingleLine (singleLine):
    print('在classSingleLine中')
    def __init__ (self, singleLineDict):
        singleLine.__init__ (self, singleLineDict)
        self.freshenStr()

    #添加self.Str属性的函数
    def freshenStr (self):
        self.Str = ' ' * self.LayerNum + ' '.join(self.main)

    def __str__ (self):
        return self.Str

    def __repr__ (self):
        return self.__str__ ()

    def __add__ (self, addObj):
        if type(addObj) == str:
            addNode = self.Str + '\n' + addObj
            return addNode
        elif type(addObj) == type(self) or type(addObj) == nukeNode or type(addObj) == nukeGroup or type(addObj) == nukeLayout or type(addObj) == blankLine or type(addObj) == steplessSingleLine:
            addNode = self.Str + '\n' + addObj.Str()
            return addNode
        else:
            print ('classSingleLine + 错误')
        
    def __radd__ (self, addObj):
        if type(addObj) == str:
            addNode = addObj + '\n' + self.Str
            return addNode
        elif type(addObj) == type(self) or type(addObj) == nukeNode or type(addObj) == nukeGroup or type(addObj) == nukeLayout or type(addObj) == blankLine or type(addObj) == steplessSingleLine:
            addNode = addObj.Str() + '\n' + self.Str
            return addNode
        else:
            print('classSingleLine + 错误')