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

def screen_node (nodecollectList, layerNumInt, programPathMain):    #分析模板节点和组的函数. 需要的参数: 模板代码列表(一行为一个单位), 层级, 程序位置, 所属的组的名字
    print('进入处理模板函数')
    #print (nodecollectList)

    groupNumInt = 0 #节点组的索引,到时要记录到字典里,因为没进一次层级都要刷新所以放在函数里
    layerNumInt += 1 #每进一次函数说明进了一个层级
    appendInt = 0  # 关闭遇组开关
    print ('第 %d 层' %layerNumInt)
    collectList = list() #以行为单位的代码列表
    #ceshi = 0
    #print('循环nodecollectList:' + str(layerNumInt))
    for lineStr in nodecollectList:    #循环模板代码列表
        #print ('!!')
        #print (lineStr)
        #遇到组
        if lineStr[layerNumInt*1:] == 'Group {':    #组的
            appendInt = 1    #激活遇组开关

        ###这一段专门开始处理普通节点###[{'name':'id相关2'},{'last':'60'}]
        if appendInt == 0:    #遇组开关没有打开
            if lineStr == '':    #遇到空行
                collectList.append (lineStr)
            elif lineStr[-1] == '{':    #遇到节点类型头行
                #print ('***\n' + lineStr)
                nodeList = list ()    #单个节点内部组成的列表
                nodeDict = dict ()
                nodeList.append (lineStr)    #先把节点的头部添加到当前的节点列表里
            elif lineStr[layerNumInt*1:] == '}':    #当遇到节点类型尾行
                #print (lineStr)    #正确显示是}
                nodeList.append (lineStr)    #再把节点的尾部添加到当前节点列表里
                collectList.append (nodeList)    #把转化成的节点类添加到整个文件的列表里
                nodeList = list ()    #最后不忘清空节点列表
            elif lineStr[0] != ' ' or lineStr.split(' ')[0] == 'push':    #没有层级观念,始终在最外层级(层级为0). 最外层的节点头和尾还有空行层级也为0,但已经在这之前被筛选掉了,所以不用担心被包括进去
                collectList.append (lineStr)
                #print ('%s: %s' %(attributeKey, attributeValue))
                #行得通的话会把无层级单行合并到有层级单行里,因为无层级单行和最外层单行很难区分
            elif lineStr[layerNumInt*1] != ' ':    #有层级观念的独立一行,非节点. 节点头和尾也同样符合条件,但一进在这之前被筛选掉了,而节点身体还要缩进一行, 所以不用担心被包括进去
                print('有层级单行: ' + lineStr)
                collectList.append (lineStr)
                #print ('%s: %s' %(attributeKey, attributeValue))

            else:    #其他排除掉后剩下的就是节点身体了
                nodeList.append (lineStr)    #在有现成的列表情况家,节点身体列表添加属性键值对
                #在后面会遇到节点尾行
                #print ('%s: %s' %(attributeKey, attributeValue))



        ###这一段专门用来处理遇到组的情况###
        #判断语句的行要进行层级处理
        elif appendInt == 1:        #如果遇组开关打开
            ###这一块用来获取组的名字#####这一段以后可以提取出来成为函数
            if lineStr[layerNumInt*1:] == 'Group {':    #重新确认组头部, 用来防止组中组的产生混乱
                groupappendInt = 1 #遇到一个组头部, 开关打开
                

            #组的头部文件,需要添加节点函数
            if  groupappendInt == 1:    #遇到组头部第一行,开关激活
                
                
                #专门处理节点头
                '''
                if lineStr == '':    #如果在组内遇到空行,几乎不可能遇到
                    collectList.append (blankLine({'main': lineStr, 'layerNumInt': 0, 'Type': 'blank_line'}))    #文件列表里添加
                '''
                if lineStr[-1] == '{':    #遇到节点头
                    #print ('***\n' + lineStr)
                    nodeList = list ()    #单个节点内部组成的列表
                    #print (nodeDict['Type'])
                    nodeList.append (lineStr) #添加节点的头部, Group {
                    nodeBodyList = list()  # 创建节点的身体列表
                    
                elif lineStr[layerNumInt*1:] == '}':    #遇到节点尾部
                    #print (lineStr)    #正确显示是}
                    nodeList.append (nodeBodyList)    #把节点的身体添加到列表里
                    nodeBodyList = list ()    #添加完后清空节点主体列表
                    nodeList.append (lineStr)    #添加节点的尾部
                    #print (nukeNodeExample.name)
                    groupBodyList = list()    #创建组主体列表
                    groupappendInt = 0    #组内部结尾, 开关关闭
                    
                else:    #节点主体, inputs 0 name Group1 xpos -349 ypos -309
                    nodeBodyList.append (lineStr)    #把键和值添加到节点主体列表
                #以上处理组头部
                
            #组的主体和底部
            elif groupappendInt == 0:    #如果遇到组的尾部
                if lineStr[layerNumInt*1:] == 'end_group':    #组结尾
                    groupList = list ()    #单个文件组组列表
                    groupList.append (nodeList)    #组头部
                    #currentGroupBodyList = copy.deepcopy(groupBodyList)
                    #print ('组主体:\n' + str(groupBodyList))
                    currentGroupNodeList = screen_node(groupBodyList, layerNumInt, programPathMain)    #递归函数, 要把组的主体进行再处理,返回的是节点类型的大列表,最后一个参数是组名
                    #返回的是一个带已经转好类的列表
                    #print (currentGroupNodeList)
                    groupList.append (currentGroupNodeList)    #添加组主体列表(行为单位)
                    groupHeadList = list ()    #清空组头部列表
                    groupBodyList = list ()    #清空组主体列表

                    #组尾部处理
                    groupList.append (lineStr)    #把组尾部添加进组列表
                    #groupList列表的结构由 头部(节点列), 主体(各种节点 组 类组成的列表) 和 尾部字符串 组成的

                    #print(currentGroupList)
                    #nukeGroupExample = nukeGroup (currentGroupList)
                    #print('当前组完全体:\n' + nukeGroupExample)
                    collectList.append(groupList)
                    appendInt = 0 #一个组的结束要把遇组开关关闭
                    groupList = list () #清空组列表

                else:
                    #print('!!!!!!!!')
                    groupBodyList.append (lineStr)    #其他都是组主体
                    print ('%%%' + lineStr)
                    if (layerNumInt > 0) and ('组1中_组1' in lineStr):
                        print ('???:' + lineStr)

    return collectList    #最后返回数据

def parseNukeModel (nukeModelStr, programPathMain):
    os.chdir(programPathMain)
    from nuke_class.nuke_layout import nukeLayout
    
    nukeModelcollectList = nukeModelStr.split('\n')
    
    nukeDict = dict ()  # 整个Nuke代码文件的字典
    layerNumInt = -1  # 节点的层级,到时要记录到字典里,顶级为0级
    
    layoutEndInt = nukeModelcollectList.index('</layout>')    #</layout>为标志确定nuke文件的头部和主体
    #下面用开分隔头部和主体
    layoutList = nukeModelcollectList[:layoutEndInt + 2]
    nodecollectList = nukeModelcollectList[layoutEndInt + 2:]
    
    layoutDict = {'main': layoutList, 'layerNumInt': 0}

    layout = nukeLayout (layoutDict)
    layout.getLayerNum(0)
    
    nukeList = list ()    #nuke文件整体的列表
    nukeList.append(layout)
    
    belongGroupStr = 'root'

    # print(layout)
    # nukeDict['body'] = screen_node (nodecollectList, layerNumInt)    #这个节点专门处理节点段,所以先要把非节点的部分割去
    nukeList.append(screen_node(nodecollectList, layerNumInt, programPathMain))
    #print (nukeList)
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
