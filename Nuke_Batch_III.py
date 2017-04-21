#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
import os, sys
programPathMain = sys.path[0]   #锁定程序的主路径
#print ('主目录:' + programPathMain)
os.chdir (programPathMain)
#print (sys.path[0])
from parse_model.parse_nuke_model import *
from get_material.get_camera_renderimages_info import *
from create_new_file import *

projectPath = r'D:\Projects\Nuke_Batch_III'  # 临时路径
projectName = 'PT_TV'  # 临时项目名称
EP = '001'


####获取设置信息####
projectSettingsListOpen = open('./data/project_settings/%s_Settings.csv' % projectName, mode='r', encoding='utf-8')  # 路径外部指定
projectSettingsListCsv = csv.reader(projectSettingsListOpen)
projectSettingsDict = dict()  # 设置信息字典
for projectSettingsListLine in projectSettingsListCsv:
    projectSettingsDict = dictAdd(projectSettingsDict, projectSettingsListLine[0])
    projectSettingsDict[projectSettingsListLine[0]][projectSettingsListLine[1]] = projectSettingsListLine[2:]  # 存到信息字典里
# print(projectSettingsDict)
projectSettingsListOpen.close()



with open (projectPath + '\\e019_mod_gamesa_108-109,112-119,172-192.nk', mode='r', encoding='utf-8') as testRead:
    testStr = testRead.read()
    

nukeList = parseNukeModel (testStr, programPathMain)

projectDict = GCRI(projectName, projectPath, projectSettingsDict, EP, programPathMain)

createNewFiles (nukeList, projectDict, programPathMain)


'''
因为自定义类之间的加法还有问题,所以如果要连接组合,先转成字符串
'''