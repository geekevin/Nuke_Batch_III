#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
#该脚本用来把Nuke工程文件分割成相应类型文件管理
#试着用递归
#如果有获取对象在列表中所在层级的方法,layerNumInt就可以省略掉了,可以更加精简数据结构
#未来把属性值的字典替换成列表元组组合
#每个节点单元(包括组)分成三份部分:头部(节点:0, 组:0), 主体(节点:1, 组:1), 底(节点:2, 组:2)
import os, sys
sys.path.append ('\\'.join(sys.path[0].split('\\')[:-1]+['node_class']))
#os.chdir ('\\'.join(sys.path[0].split('\\')[:-1]+['node_class']))
from nuke_node import nukeNode
def group_node (noudeList, layerNumInt):
    groupNumInt = 0 #节点组的索引,到时要记录到字典里,因为没进一次层级都要刷新所以放在函数里
    layerNumInt += 1 #每每进一次函数说明进了一个层级
    groupLineList = list() #以行为单位的代码列表
    appendInt = 0 #遇到一个组的开关
    fileList = list() #整个文件列表
    ceshi = 0
    for lineStr in noudeList:
        #遇到组
        if lineStr[layerNumInt*1:] == 'Group {':
            appendInt = 1

        ###这一段专门开始处理普通节点###[{'name':'id相关2'},{'last':'60'}]
        if appendInt == 0:
            if lineStr == '':
                fileList.append ({'main': lineStr, 'layerNumInt': 0, 'nodeType': 'null'})
            elif lineStr[-1] == '{':
                nodeList = list() #单个节点内部组成的列表
                nodeDict = dict()
                nodeDict['nodeType'] = lineStr[layerNumInt*1:].split(' ')[1]
                nodeList.append (lineStr[layerNumInt*1:]) #节点的头部
            elif lineStr[layerNumInt*1:] == '}':
                #print (lineStr) #正确显示是}
                nodeList.append (nodeBodyList) #节点的身体
                nodeBodyList = [] #清空节点主体列表
                nodeList.append (lineStr[layerNumInt*1:]) #节点的尾部
                nodeDict['main'] = nodeList
                nodeDict['layerNumInt'] = layerNumInt
                fileList.append (nukeNode(nodeDict))
                nodeList = []
            elif lineStr[0] != ' ': #没有层级观念,始终在最外层级
                attributeKey = lineStr.split(' ')[0]
                attributeValue = ' '.join(lineStr.split(' ')[1:])
                fileList.append ({'main': {attributeKey: attributeValue}, 'layerNumInt':0, 'nodeType':'push'})
                #print ('%s: %s' %(attributeKey, attributeValue))
            elif lineStr[layerNumInt*1] != ' ': #有层级观念的独立一行,非节点
                attributeKey = lineStr[layerNumInt*1:].split(' ')[0]
                attributeValue = ' '.join(lineStr[layerNumInt*1:].split(' ')[1:])
                fileList.append ({'main': {attributeKey: attributeValue}, 'layerNumInt':layerNumInt, 'nodeType':'set'})
                #print ('%s: %s' %(attributeKey, attributeValue))
            else:
                #已解决(问题:push $N4792ed00的存在和set N349d8400 [stack 0]的存在
                attributeKey = lineStr[(layerNumInt+1)*1:].split(' ')[0]
                attributeValue = ' '.join(lineStr[(layerNumInt+1)*1:].split(' ')[1:])
                try:
                    nodeBodyList.append ((attributeKey, attributeValue))
                except:
                    nodeBodyList = [] #节点的身体
                    nodeBodyList.append ((attributeKey, attributeValue))
                #print ('%s: %s' %(attributeKey, attributeValue))

        ###这一段专门用来处理遇到组的情况###
        #判断语句的行要进行层级处理
        elif appendInt == 1:
            ###这一块用来获取组的名字#####这一段以后可以提取出来成为函数
            if lineStr[layerNumInt*1:] == 'Group {':
                groupappendInt = 1 #遇到一个组内部的开关

            #组的头部文件
            if  groupappendInt == 1:
                try:
                    groupHeadList.append (lineStr)
                except:
                    groupHeadList = list()
                    groupHeadList.append (lineStr)
                if lineStr[layerNumInt*1:] == '}':
                    groupappendInt = 0
            #组的主体和底部
            elif groupappendInt == 0:
                if lineStr[layerNumInt*1:] == 'end_group':
                    groupList = list() #单个文件组组列表
                    groupList.append (groupHeadList)
                    groupList.append (group_node(groupBodyList, layerNumInt)) #要把组的主体进行再处理
                    groupHeadList = [] #清空组头部列表
                    groupBodyList = [] #清空组主体列表

                    try:
                        groupFootList.append(lineStr)
                    except:
                        groupFootList = list()
                        groupFootList.append(lineStr)
                    groupList.append (groupFootList)
                    groupFootList = [] #清空组底部列表
                    fileList.append({'main': groupList, 'layerNumInt':1, 'nodeType':'group'})
                    appendInt = 0 #一个组的结束要把遇组开关关闭
                    groupList = [] #清空组列表

                else:
                    try:
                        groupBodyList.append(lineStr)
                    except:
                        groupBodyList = list()
                        groupBodyList.append(lineStr)

    return fileList #最后返回数据







with open ('C:\\Users\\Yimi-Kevin\\Desktop\\e019_mod_gamesa_108-109,112-119,172-192.nk', mode='r', encoding='utf-8') as testRead:
    testStr = testRead.read()
testLineList = testStr.split('\n')

nukeDict = dict() #整个Nuke代码文件的字典
layerNumInt = -1 #节点的层级,到时要记录到字典里

layoutEndInt = testLineList.index('</layout>')
layout = testLineList[:layoutEndInt+2]
nodeLineList = testLineList[layoutEndInt+2:]

layoutList = list()
layoutList = [{'main': layout, 'layerNumInt': 0}]

nukeList = list()
nukeList.append (layoutList)

#print(layout)

#nukeDict['body'] = group_node (nodeLineList, layerNumInt)    #这个节点专门处理节点段,所以先要把非节点的部分割去
nukeList.append (group_node (nodeLineList, layerNumInt))
print(nukeList)


'''
规则
头:0
主体:1
底:2
'''
'''
示例:
print (nukeList[1][14]['main'][1][0]['main'][1][1])
整个数据列表中的节点群(为nukeList列表第二(索引1))中的第十五(nukeList[1]中索引14)个对象为组,在这个组里的主体(键'main')中的节点群(组中的索引1)中第二个节点(节点群中索引1)的主体(键'main')中身体(索引1)的第二行(索引1)
'''
