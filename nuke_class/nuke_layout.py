#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")

from nuke_class.nuke_node import *
from nuke_class.nuke_group import *
from nuke_class.single_line import *
from nuke_class.nuke_layout import *
from nuke_class.blank_line import *
class nukeLayout (object):
    print('在nukeLayout中')
    def __init__ (self, layout):
        self.layoutList = layout['main']
        self.Type = 'layout'  # 节点类型
        self.LayerNum = layout['layerNumInt']
        self.__str__()
        
    def __str__ (self):
        layoutSplit = list()
        for lineStr in self.layoutList:
            layoutSplit.append (' ' * self.LayerNum + lineStr)
        self.Str = ('\n' + ' '*self.LayerNum).join (layoutSplit)
        return self.Str
    
    def __repr__ (self):
        return self.Str
    
    def __add__ (self, addObj):
        if type (addObj) == str:    #相同节点类型
            addStr = self.Str + '\n' + addObj    #节点和节点字符串化后连接,中间用换行分隔
            return addStr  # 返回的对象类型为字符串
        elif type(addObj) == list:  # 相同节点类型
            addStr = self.Str + '\n' + '\n'.join(addObj)  # 节点和节点字符串化后连接,中间用换行分隔
            return addStr
        elif type (addObj) == type(self) or type(addObj) == nukeNode or type(addObj) == nukeGroup or type(addObj) == classSingleLine or type(addObj) == steplessSingleLine or type(addObj) == blankLine:    #相同节点类型
            addStr = self.Str + '\n' + addObj.Str    #节点和节点字符串化后连接,中间用换行分隔
            return addStr  # 返回的对象类型为字符串
        else:
            print ('参数不对')
        
    def __radd__ (self, addObj):
        if type (addObj) == str:    #相同节点类型
            addStr = addObj + '\n' + self.Str    #节点和节点字符串化后连接,中间用换行分隔
            return addStr  # 返回的对象类型为字符串
        elif type(addObj) == list:  # 相同节点类型
            addStr = '\n'.join(addObj) + '\n' + self.Str  # 节点和节点字符串化后连接,中间用换行分隔
            return addStr
        elif type (addObj) == type(self):    #相同节点类型
            addStr = addObj.__str__() + '\n' + self.Str    #节点和节点字符串化后连接,中间用换行分隔
            return addStr  # 返回的对象类型为字符串
    
    def getLayerNum (self, LayerNum):
        self.LayerNum = LayerNum