#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
#空行类
from nuke_class.nuke_group import *
from nuke_class.nuke_node import *
from nuke_class.nuke_layout import *
from nuke_class.single_line import *
from nuke_class.blank_line import *

class blankLine (object):
    print ('在blankLine中')
    def __init__ (self, blankLineDict):
        self.main = blankLineDict ['main']
        self.LayerNum = blankLineDict ['layerNumInt']
        self.Type = blankLineDict ['Type']
        self.__str__()
    
    def __str__ (self):
        self.Str = ''
        return self.Str
    
    def __repr__ (self):
        return self.__str__()
    
    def __add__ (self, addObj):
        if type (addObj) == str:
            addStr = self.Str + '\n' + addObj
            return addStr
        elif type (addObj) == type (self) or type (addObj) == nukeGroup or type (addObj) == nukeNode or type (addObj) == classSingleLine or type (addObj) == steplessSingleLine:
            addStr = self.Str + '\n' + addObj.Str
            return addStr
        else:
            print ('blankLine ++ 错误')
    
    def __radd__ (self, addObj):
        if type (addObj) == str:
            addStr = addObj + '\n' + self.Str
        elif type (addObj) == type (self) or type (addObj) == nukeGroup or type (addObj) == nukeNode or type (addObj) == classSingleLine or type (addObj) == steplessSingleLine:
            addStr = addObj.Str + '\n' + self.Str
            return addStr
        else:
            print('blankLine R+ 错误')