#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
import os, sys, copy
from nuke_class.nuke_node import nukeNode  # 导入nuke类节点
from nuke_class.nuke_group import nukeGroup  # 导入nuke组类节点
from nuke_class.single_line import steplessSingleLine  # 导入nuke无层级单行类
from nuke_class.single_line import classSingleLine  # 导入nuke无层级单行类
from nuke_class.blank_line import blankLine  # 导入nuke无层级单行类
from nuke_class.nuke_layout import nukeLayout

#遍历Nuke文件主体, 此函数每次处理一个镜头
def traversalNukeList (List, aCameraDict, cameraName):
    nodeIndex = -1
    for Paragraph in List:    #Paragraph为一个节点或组
        nodeIndex += 1
        if type(Paragraph) == nukeGroup:    #如果Paragraph是组
            traversalNukeList(Paragraph.groupBody, aCameraDict, cameraName)
            
        elif type(Paragraph) == nukeNode:    #如果Paragraph是节点
            #先限定节点为普通节点
            if Paragraph.Change == False:    #判定节点是否更改过
                if Paragraph.Type == 'Read':    #判定节点为Read节点
                    if 'Renderimages' in Paragraph.materialPath:    #判定该节点是序列素材节点
                        if 'Read' in aCameraDict.keys():    #判定这个镜头是有素材序列的
                            #print ('节点名字: ' + Paragraph.Name)
                            #print ('素材名字: ' + Paragraph.layerName)
                            #print('Read信息: ' + str(aCameraDict[cameraInfoKey]))
                            for cameraFileName in aCameraDict['Read'].keys():    #遍历镜头文件夹
                                #print (cameraFileName)
                                for layerName in aCameraDict['Read'][cameraFileName].keys():    #遍历分层素材
                                    print (layerName)
                                    if layerName == Paragraph.layerName:    #素材对应节点
                                        print ('*************' + str(aCameraDict['Read'][cameraFileName][layerName]))
                                        Paragraph.RepNodeAtt(aCameraDict['Read'][cameraFileName][layerName], 'Read')    #层中属性
                                        if Paragraph.Change == True:
                                            aCameraDict['Read'][cameraFileName][layerName]['enable'] = 1
                                        print ('改变后的节点:\n' + str(Paragraph))
                                        print ('节点改变状态: ' + str(Paragraph.Change))
                                        print(List[nodeIndex])
                        else:
                            print ('%s镜头没有序列素材' %cameraName)
                    else:
                        print('这个Read节点不是序列素材的节点')
                        
                elif Paragraph.Type == 'Root':
                    if 'Root' in aCameraDict.keys():
                        #print('Root节点: ' + str(aCameraDict[cameraInfoKey]))
                        Paragraph.RepNodeAtt(aCameraDict['Root'],'Root')
                        print('改变后的Root节点:\n' + str(Paragraph))
                    else:
                        print ('%s镜头没有Root信息' %cameraName)
                
                elif Paragraph.Type == 'Write':
                    if 'Write' in aCameraDict.keys():
                        #print('Write节点: ' + str(aCameraDict[cameraInfoKey]))
                        Paragraph.RepNodeAtt(aCameraDict['Write'], 'Write')
                        print('改变后的Write节点:\n' + str(Paragraph))
                    else:
                        print ('%s镜头没有Write信息' %cameraName)
                        '''
                        elif 'camerasMotion' in :
                            print ('/////////////' + str(aCameraDict ['camerasMotion']))
                            
                            #需要把循环素材信息字典循环放到最外面
                        '''
                else:
                    if Paragraph.Type in aCameraDict.keys():
                        Paragraph.RepNodeAtt(aCameraDict[Paragraph.Type], Paragraph.Type)
                        #print('改变后的' + cameraInfoKey + '节点:\n' + str(Paragraph))
                    else:
                        print ('%s在%s中找不到匹配' %(Paragraph.Type, cameraName))
                        
        else:
            #print ('其它类型: ' + str(Paragraph))
            a=1
        #List[nodeIndex] = Paragraph

#创建新文件
def createNewFiles (nukeList, projectDict, programPathMain):    #nuke文件代码列表, 素材字典, nuke程序主路径
    os.chdir(programPathMain)
    print ('在createNewFiles函数中')
    print (projectDict)
    for cameraKey in projectDict['cameras'].keys():    #循环字典中镜头
        newNodeList = copy.deepcopy(nukeList[1])    #防止原实例被改变
        print (cameraKey + ': ' + str(projectDict['cameras'][cameraKey]))
        traversalNukeList(newNodeList, projectDict['cameras'][cameraKey], cameraKey)

    
    
    
    
    
    
    
    
    
    

    '''
    def StrNuke (NukeList):
        lianjie = ''
        for lian in NukeList:
            if type(lianjie) is list:
                StrNuke(lian)
            else:
                lianjie = lianjie + '\n' + str(lian)
        return lianjie
    lianjie = str(nukeList[0]) + StrNuke (nukeList[1])
    print (lianjie)
    '''
    print (projectDict)