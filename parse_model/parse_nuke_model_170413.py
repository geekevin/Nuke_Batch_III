#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
import os, sys, copy
from nuke_class.nuke_node import nukeNode  # 导入nuke类节点
from nuke_class.nuke_group import nukeGroup  # 导入nuke组类节点
from nuke_class.single_line import steplessSingleLine  # 导入nuke无层级单行类
from nuke_class.single_line import classSingleLine  # 导入nuke无层级单行类
from nuke_class.blank_line import blankLine  # 导入nuke无层级单行类
#该脚本用来把Nuke工程文件分割成相应类型文件管理
#试着用递归
#如果有获取对象在列表中所在层级的方法,layerNumInt就可以省略掉了,可以更加精简数据结构
#未来把属性值的字典替换成列表元组组合
#每个节点单元(包括组)分成三份部分:头部(节点:0, 组:0), 主体(节点:1, 组:1), 底(节点:2, 组:2)

def group_node (noudeList, layerNumInt, programPathMain, belongGroupStr):    #分析模板节点和组的函数. 需要的参数: 模板代码列表(一行为一个单位), 层级, 程序位置, 所属的组的名字
    os.chdir(programPathMain)
    print('进入处理模板函数')

    groupNumInt = 0 #节点组的索引,到时要记录到字典里,因为没进一次层级都要刷新所以放在函数里
    layerNumInt += 1 #每进一次函数说明进了一个层级
    groupLineList = list() #以行为单位的代码列表
    appendInt = 0 #遇到一个组的开关
    fileList = list() #整个文件列表
    #ceshi = 0
    for lineStr in noudeList:    #循环模板代码列表
        #遇到组
        if lineStr[layerNumInt*1:] == 'Group {':    #组的
            appendInt = 1    #激活遇组开关

        ###这一段专门开始处理普通节点###[{'name':'id相关2'},{'last':'60'}]
        if appendInt == 0:    #遇组开关没有打开
            if lineStr == '':    #遇到空行
                fileList.append (blankLine({'main': lineStr, 'layerNumInt': 0, 'nodeType': 'blank_line'}))
            elif lineStr[-1] == '{':    #遇到节点类型头行
                #print ('***\n' + lineStr)
                nodeList = list ()    #单个节点内部组成的列表
                nodeDict = dict ()
                nodeDict['nodeType'] = lineStr[layerNumInt*1:].split(' ')[0]    #头一行大括号({)前面的词正好可以作为节点的类型名
                #print (nodeDict['nodeType'])
                nodeList.append (lineStr[layerNumInt*1:])    #先把节点的头部添加到当前的节点列表里
            elif lineStr[layerNumInt*1:] == '}':    #当遇到节点类型尾行
                #print (lineStr)    #正确显示是}
                nodeList.append (nodeBodyList)    #就把节点的身体列表添加到当前节点列表里, 身体列表的处理在下面的else里有
                nodeBodyList = list ()    #添加完后不忘清空节点主体列表, nodeBodyList的清空不会影响之前添加的列表
                nodeList.append (lineStr[layerNumInt*1:])    #再把节点的尾部添加到当前节点列表里
                nodeDict['main'] = copy.deepcopy(nodeList)    #把当前的节点列表深拷贝到当前节点字典里
                nodeDict['layerNumInt'] = layerNumInt    #给当前节点字典添加层级信息
                currentNodeDict = copy.deepcopy(nodeDict)    #深拷贝字典,currentNodeDict只是用来中转用的
                nukeNodeExample = nukeNode (currentNodeDict)    #创建nukeNode类的实例
                nukeNodeExample.belongGroup (belongGroupStr)    #节点的隶属
                nukeNodeExample.revisionInfo (programPathMain)    #这个方法用外部文档来补全节点的信息, 因为有一些属性在默认值的情况下会忽略(隐藏)这个属性的代码
                fileList.append (nukeNodeExample)    #把转化成的节点类添加到整个文件的列表里
                nodeList = list ()    #最后不忘清空节点列表
                nodeDict = dict ()    #最后不忘清空节点字典
                '''
                elif lineStr[0] != ' ':    #没有层级观念,始终在最外层级(层级为0). 最外层的节点头和尾还有空行层级也为0,但已经在这之前被筛选掉了,所以不用担心被包括进去
                    attributeKey = lineStr.split(' ')[0]    #把这一行的空格分隔的前部作为这个的类型名
                    attributeValue = ' '.join(lineStr.split(' ')[1:])    #后部作为值
                    fileList.append (steplessSingleLine({'main': (attributeKey, attributeValue), 'layerNumInt':0, 'nodeType':attributeKey}))
                    #print ('%s: %s' %(attributeKey, attributeValue))
                '''
                #行得通的话会把无层级单行合并到有层级单行里,因为无层级单行和最外层单行很难区分
            elif lineStr[layerNumInt*1] != ' ':    #有层级观念的独立一行,非节点. 节点头和尾也同样符合条件,但一进在这之前被筛选掉了,而节点身体还要缩进一行, 所以不用担心被包括进去
                attributeKey = lineStr[layerNumInt*1:].split(' ')[0]    #把这一行的空格分隔的前部作为这个的类型名
                attributeValue = ' '.join(lineStr[layerNumInt*1:].split(' ')[1:])    #后部作为值
                fileList.append (classSingleLine({'main': (attributeKey, attributeValue), 'layerNumInt':layerNumInt, 'nodeType':attributeKey}))
                #print ('%s: %s' %(attributeKey, attributeValue))

            else:    #其他排除掉后剩下的就是节点身体了
                attributeKey = lineStr[(layerNumInt+1)*1:].split(' ')[0]    #节点属性键
                attributeValue = ' '.join(lineStr[(layerNumInt+1)*1:].split(' ')[1:]) #节点属性值
                try:
                    nodeBodyList.append ((attributeKey, attributeValue))    #在有现成的列表情况家,节点身体列表添加属性键值对
                except:
                    nodeBodyList = list () #没有创建列表就创建列表
                    nodeBodyList.append ((attributeKey, attributeValue))   #节点身体列表添加属性键值对
                #在后面会遇到节点尾行
                #print ('%s: %s' %(attributeKey, attributeValue))



        ###这一段专门用来处理遇到组的情况###
        #判断语句的行要进行层级处理
        elif appendInt == 1:        #如果遇组开关打开
            ###这一块用来获取组的名字#####这一段以后可以提取出来成为函数
            if lineStr[layerNumInt*1:] == 'Group {':    #重新确认组头部, 用来防止组中组的产生混乱
                groupappendInt = 1 #遇到一个组头部, 开关打开

            #组的头部文件,需要添加节点函数
            if  groupappendInt == 1:    #如果在组内
                '''
                if lineStr == '':    #如果在组内遇到空行,几乎不可能遇到
                    fileList.append (blankLine({'main': lineStr, 'layerNumInt': 0, 'nodeType': 'blank_line'}))    #文件列表里添加
                '''
                if lineStr[-1] == '{':    #遇到节点头
                    #print ('***\n' + lineStr)
                    nodeList = list ()    #单个节点内部组成的列表
                    nodeDict = dict ()    #单个节点内部组成的字典
                    nodeDict['nodeType'] = lineStr[layerNumInt*1:].split(' ')[0]
                    #print (nodeDict['nodeType'])
                    nodeList.append (lineStr[layerNumInt*1:]) #节点的头部
                elif lineStr[layerNumInt*1:] == '}':    #遇到节点尾部
                    #print (lineStr)    #正确显示是}
                    nodeList.append (nodeBodyList)    #把节点的身体添加到列表里
                    nodeBodyList = list ()    #添加完后清空节点主体列表
                    nodeList.append (lineStr[layerNumInt*1:])    #添加节点的尾部
                    nodeDict['main'] = copy.deepcopy(nodeList)    #节点字典添加上面的列表
                    nodeDict['layerNumInt'] = layerNumInt    #节点字典添加所在层级
                    currentNodeDict = copy.deepcopy(nodeDict)    #临时变量,深拷贝用
                    nukeNodeExample = nukeNode (currentNodeDict)    #转化成节点类
                    nukeNodeExample.revisionInfo (programPathMain)    #补充属性
                    fileList.append (nukeNodeExample)    #往文件列表中添加组
                    nodeList = list ()    #清空列表
                    nodeDict = dict ()    #清空字典
                    groupappendInt = 0    #组内部结尾,开关关闭
                else:    #节点主体
                    attributeKey = lineStr[(layerNumInt+1)*1:].split(' ')[0]    #节点主属性名
                    attributeValue = ' '.join(lineStr[(layerNumInt+1)*1:].split(' ')[1:])    #节点主属性值
                    try:
                        nodeBodyList.append ((attributeKey, attributeValue))    #把键和值添加到节点主体列表
                    except:
                        nodeBodyList = list () #创建节点的身体列表
                        nodeBodyList.append ((attributeKey, attributeValue))    #把键和值添加到节点主体列表
                    #print ('%s: %s' %(attributeKey, attributeValue))
                '''
                try:
                    groupHeadList.append (lineStr)
                except:
                    groupHeadList = list()
                    groupHeadList.append (lineStr)
                if lineStr[layerNumInt*1:] == '}':
                    groupappendInt = 0
                '''

            #组的主体和底部
            elif groupappendInt == 0:    #如果遇到组的尾部
                if lineStr[layerNumInt*1:] == 'end_group':    #组结尾
                    groupList = list ()    #单个文件组组列表
                    groupList.append (nukeNodeExample)    #组头部
                    #currentGroupBodyList = copy.deepcopy(groupBodyList)
                    groupList.append (group_node(groupBodyList, layerNumInt, programPathMain, nukeNodeExample.nodeName)) #要把组的主体进行再处理
                    groupHeadList = list () #清空组头部列表
                    groupBodyList = list () #清空组主体列表

                    #组尾部处理
                    '''
                    try:
                        groupFootList.append(lineStr)
                    except:
                        groupFootList = list()
                        groupFootList.append(lineStr)
                    groupList.append (groupFootList)    #把组尾部添加进组列表
                    groupFootList = [] #清空组底部列表
                    '''
                    groupFootStr = lineStr[layerNumInt*1:]    #组尾部
                    groupList.append (groupFootStr)    #把组尾部添加进组列表

                    currentGroupList = copy.deepcopy(groupList)    #临时变量,为了深拷贝
                    #print(currentGroupList)
                    #nukeGroupExample = nukeGroup (currentGroupList)
                    nukeGroupExample = nukeGroup ({'main': currentGroupList, 'layerNumInt':layerNumInt, 'nodeType':'Group'})    #转化成组类型,实例中包含节点
                    #fileList.append(nukeGroupExample)
                    appendInt = 0 #一个组的结束要把遇组开关关闭
                    groupList = list () #清空组列表

                else:
                    try:
                        groupBodyList.append (lineStr)
                    except:
                        groupBodyList = list()
                        groupBodyList.append (lineStr)

    return fileList    #最后返回数据

def parseNukeModel (nukeModelStr, programPathMain):
    os.chdir(programPathMain)
    from nuke_class.nuke_layout import nukeLayout
    
    nukeModelLineList = nukeModelStr.split('\n')
    
    nukeDict = dict ()  # 整个Nuke代码文件的字典
    layerNumInt = -1  # 节点的层级,到时要记录到字典里,顶级为0级
    
    layoutEndInt = nukeModelLineList.index('</layout>')    #</layout>为标志确定nuke文件的头部和主体
    #下面用开分隔头部和主体
    layoutList = nukeModelLineList[:layoutEndInt + 2]
    nodeLineList = nukeModelLineList[layoutEndInt + 2:]
    
    layoutDict = {'main': layoutList, 'layerNumInt': 0}

    layout = nukeLayout (layoutList)
    layout.getNodeLayerNum(0)
    
    nukeList = list ()    #nuke文件整体的列表
    nukeList.append(layout)
    
    belongGroupStr = 'root'

    # print(layout)
    # nukeDict['body'] = group_node (nodeLineList, layerNumInt)    #这个节点专门处理节点段,所以先要把非节点的部分割去
    nukeList.append(group_node(nodeLineList, layerNumInt, programPathMain, belongGroupStr))
    return nukeList







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
