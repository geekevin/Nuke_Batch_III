#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
import os, sys, copy, csv
#print ('路径:' + sys.path[0])
#sys.path.append ('.')
from nuke_class.single_line import *
from nuke_class.nuke_group import *
from nuke_class.nuke_layout import *
from nuke_class.blank_line import *
#node类, 为一个不可变类
class nukeNode (object):
    print('在nukeNode中')
    def __init__ (self, nodeDict):
        self.nodeHead = nodeDict['main'][0]    #节点头,如"Read {"
        self.nodeBody = nodeDict['main'][1]    #节点主体
        self.nodeFoot = nodeDict['main'][2]    #节点底部,一般为"}"
        self.Type = nodeDict['Type']   #节点类型
        self.LayerNum = nodeDict['layerNumInt']    #节点所在层级
        self.Change = False
        if self.Type == 'Read':    #处理(获得,替换)Read类型节点的名字
            self.getLayerName ()    #layerName用来匹配素材##################
        self.getNodeName()
        self.freshenNode()    #可视化类

    #补全节点信息
    def revisionInfo (self, programPathMain):
        ReadNodeInfo = open (programPathMain + '\\node_data\\' + 'Read' + '.csv', mode='r', encoding = 'utf-8')
        ReadNodeCsv = csv.reader(ReadNodeInfo)    #读取Read节点类型模板文件的信息
        nodeAttributeKeyList = list()    #创建空列表,用来收集节点属性的的键
        for nodeAttributeLine in self.nodeBody:    #遍历节点主体
            nodeAttributeKeyList.append(nodeAttributeLine[0])    #把节点主体中属性的键收录到列表里

        for attributeLine in ReadNodeCsv:    #遍历Read节点模板信息,一行一对键值
            if not attributeLine[0] in nodeAttributeKeyList:    #假如要处理的节点中的某个属性(的键)在Read节点模板信息中找不到
                self.nodeBody.append(attributeLine)             #则添加该属性

        self.freshenNode()  # 可视化类
    
    def getNodeName (self):
        #获取节点名
        for line in self.nodeBody:    #获得节点的名字
            if line[0] == 'name':
                #print ('获得节点名字')
                self.Name = str(line[1])
                
    def getLayerName (self):
        #获取层名
        for nodeLine in self.nodeBody:    #遍历节点主体
            if nodeLine[0] == 'file':    #找到file属性这一行
                #print(nodeLine[1])
                nodeImageName = nodeLine[1].split('/')[-2]    #这里需要注意CH和CH1,BG和BG1的问题,用==还是in需要多加考虑
                #BG和BG1问题:再有若干个BG的情况下,而模板可能使用其中一个,可以分两层筛选,先用精确(==)匹配,匹配上的做一个标记.假如BG还有多的,则再进行粗的匹配
                '''
                imageSequence = nodeLine[1].split('/')[-1]    #提取出文件序列名
                nodeImageName = '_'.join(imageSequence.split('_')[:-1])    #从文件序列名中提取出需要的信息成为节点的名称
                self.layerNameStr = nodeImageName
                '''
                self.layerName = str(nodeImageName)    #替换名字
                self.materialPath = str(nodeLine[1])

    def freshenNode (self):
        #字符串化
        nodeLineList = list()    #创建空的节点列表
        #self.Str = ' ' * self.LayerNum + self.nodeHead + '\n'    #给节点头部添加缩进
        nodeLineList.append (' ' * self.LayerNum + self.nodeHead)    #给节点头部添加缩进, 并添加到列表
        for nodeAttributeTuple in self.nodeBody:    #遍历节点主体中属性
            nodeAttributeStr = ' '.join (nodeAttributeTuple)    #把每个属性的键和值用空格分隔
            #self.Str = self.Str + ' ' * (self.LayerNum + 1) + nodeAttributeStr +'\n'
            nodeLineList.append (' ' * (self.LayerNum + 1) + nodeAttributeStr)    #给节点属性添加缩进, 并添加到列表
        #self.Str = self.Str + ' ' * self.LayerNum + self.nodeFoot
        nodeLineList.append (' ' * self.LayerNum + self.nodeFoot)    #给节点底部添加缩进, 并添加到列表
        self.Str = '\n'.join (nodeLineList)    #节点列表行化且转化成字符串
    
    def __len__ (self):    #节点的长度, 一行为一个数量级
        return len(self.nodeBody)+2    #因为节点有主体(属性)和头尾组成,所以长度为主题的行数加头尾两行

    def __add__ (self, addObj):
        #+, 连接节点
        #print ('N++++')

        if type (addObj) == str:    #对方是字符串
            addStr = self.Str + '\n' + addObj    #节点字符串化后和字符串连接
            return str(addStr)    #返回的对象类型为字符串
        elif type (addObj) == list:    #对方是列表
            addStr = self.Str + '\n' + '\n'.join(addObj)    #节点字符串化后和列表字符串化后进行连接,换行分隔
            return str(addStr)    #返回的对象类型为字符串
        elif type(addObj) == type(self) or type(addObj) == steplessSingleLine or type(addObj) == classSingleLine or type(addObj) == blankLine or type(addObj) == nukeGroup:  # 相同节点类型
            addStr = self.Str + '\n' + addObj.Str  # 节点和节点字符串化后连接,中间用换行分隔
            return str(addStr)  # 返回的对象类型为字符串
        else:    #其它类型无法合成
            #print (type(addObj))
            #print (addObj)
            print ('只能输入nukeNode,steplessSingleLine,classSingleLine,字符串和列表类型的参数')

    def __radd__ (self, addObj):
        #+,连接
        #print ('NR+++')
        if type(addObj) == str:    #对方类型为字符串
            addStr = addObj + '\n' + self.Str
            return str(addStr)    #返回对象类型为字符串
        elif type(addObj) == list:    #对方类型为列表
            addStr = '\n'.join (addObj) + '\n' + self.Str    #列表字符串化和节点对象字符串化连接
            return str(addStr)    #返回对象类型为字符串
        elif type(addObj) == type(self) or type(addObj) == steplessSingleLine or type(addObj) == classSingleLine or type(addObj) == blankLine or type(addObj) == nukeGroup:    #相同节点类型
            addStr = addObj.Str + '\n' + self.Str
            return str(addStr)    #返回对象类型为字符串
        else:    #其他类型
            #print('!!!!!!!!')
            #print (type(addObj))
            #print (addObj)
            print ('只能输入nukeNode和字符串和整数类型的参数')
            #return addObj

    def __mul__ (self, mulObj):
        #*,重复,这个的参数类型仅限整数
        if type(mulObj) == int:    #判断参数是否为整数
            if mulObj == 0:    #参数为0,则变为空字符串
                mulNode = ''
            elif mulObj > 0:
                while mulObj > 0:
                    try:
                        mulNode = mulNode + '\n' + self.Str
                        mulObj -= 1
                    except:
                        mulNode = self.Str
                        mulObj -= 1
                return mulNode    #返回对象类型为字符串
            else:
                print('只能输入正整数')
        else:
            print('只能输入正整数')

    def __rmul__ (self, mulObj):    #反向,效果同mul
        return self.__mul__ (mulObj)    #调用__mul__

    '''
    def __eq__ (self, addObj):
        #==
        return pass
    '''

    def __str__ (self):
        #字符串化节点
        return self.Str

    def __repr__ (self):
        '''
        for nodeAttribute in self.nodeBody:
            if nodeAttribute[0] == 'name':
                print(nodeAttribute[1])
                return nodeAttribute[1]
        '''
        return self.Str

    # addStrAttribute, 添加节点属性,参数限定为元组
    def addStrAtt (self, attributeTuple):
        #newSelf = copy.deepcopy(self)    #深拷贝原始节点对象实例,用来进行修改
        if (type(attributeTuple) == tuple or type(attributeTuple) == list) and (len (attributeTuple) == 2):    #条件:类型为列表或元组,长度为2(一个键,一个字值)
            self.nodeBody.append (tuple([attributeTuple[0], str(attributeTuple[1])]))    #在几点主体的属性列表末尾添加新的属性
            self.freshenNode()    #字符串化
            #return self    #返回的对象类型为字符串
        else:
            print ('输入参数并非元组或列表,或者元组和列表内容并非两个值')

    def changeNode (self, changeNodeKey = True):
        self.Change = changeNodeKey

    # ReplaceNodeAttribute, 替换属性,会改变原节点
    def RepNodeAtt (self, repAttribute, repNodeClass):    #repAttribute得是两个值的元组或列表,或者是一个字典
        if self.Change == False:    #先判定节点是否已经被更改
            #newSelf = copy.deepcopy(self)
            if (type(repAttribute) == tuple or type(repAttribute) == list) and len (repAttribute):    #当repAttribute是两个值的元组或列表
                attributeNum = -1    #属性所在索引
                mateAttribute = False    #属性是否更改标识,False表示未更改
                if repAttribute[1] == 'tiff' and repNodeClass == 'Write':
                    self.RepNodeAtt(['datatype', '16 bit'], repNodeClass)
                    self.RepNodeAtt(['compression', 'none'], repNodeClass)
                    self.Change = False
                for nodeAttribute in self.nodeBody:
                    attributeNum += 1
                    if str(repAttribute[0]) == str(nodeAttribute[0]):
                        #print('====' + str(nodeAttribute[0]) + ' VS ' + str(repAttribute[0]))
                        #print (self.nodeBody[attributeNum])
                        self.nodeBody[attributeNum] = [repAttribute[0], str(repAttribute[1])]
                        self.freshenNode()    #字符串化
                        mateAttribute == True
                        return True
                if mateAttribute == False:
                    print (repAttribute)
                    print ('没有找到对应属性,无法替换')
            elif type(repAttribute) == dict:    #当repAttribute是一个字典
                for layerAttName in repAttribute.keys():
                    if repNodeClass == 'Read':
                        print ('-----------' + layerAttName)
                        if (layerAttName != 'enable') and (repAttribute['enable'] == 0):
                            #print('要添加的属性: ' + str(layerAttName) + ' | ' + str(aCameraDict[cameraInfoKey][cameraFileName][layerName][layerAttName]))
                            Changed = self.RepNodeAtt([layerAttName, repAttribute[layerAttName]],repNodeClass)
                    else:
                        Changed = self.RepNodeAtt([layerAttName, repAttribute[layerAttName]], repNodeClass)
                if Changed == True:
                    self.Change = True
            else:
                print ('输入参数并非元组或列表或者参数内容非两个值')
                
        if self.Change == True:
            print('该节点已经被更改过')

    # 删除属性
    def DelNodeAtt (self, attributeKeys):
        #newSelf = copy.deepcopy(self)
        if type(attributeKeys) == str:    #限定参数类型为字符串
            attributeNum = -1    #默认节点中属性所在的位置(第几行)
            for nodeAttribute in self.nodeBody:    #遍历属性,newSelf.nodeBody是一个节点属性组成的列表
                attributeNum += 1    #每遍历一行值加一
                mateAttributeKey = False    #匹配开关
                if nodeAttribute[0] == attributeKeys:    #根据属性的键找到对应的属性
                    mateAttributeKey = True    #根据属性键找到对应的属性
                    self.nodeBody.pop(attributeNum)    #删除该行属性
                    self.freshenNode()    #字符串化,深拷贝
                    #return self    #返回实例,但不改变原实例
            if mateAttributeKey == False:
                print ('没有找到对应属性,无法替换')
        else:
            print ('输入参数并非字符串')

    # nodeCondition,激活或关闭节点,0关闭,1激活
    def nodeCon (self, conditionKeyInt):
        keysNum = 0
        for keys in self.nodeBody:
            if keys[0] == 'name':
                keysNum = 1

        if keysNum == 1:
            if conditionKeyInt == 0 or conditionKeyInt == 1:
                #newSelf = copy.deepcopy(self)    #深拷贝
                attributeNum = -1
                if conditionKeyInt == 1:
                    for nodeAttribute in self.nodeBody:
                        attributeNum += 1
                        if nodeAttribute[0] == 'disable':
                            self.nodeBody.pop(attributeNum)

                if conditionKeyInt == 0:
                    disableHave = 0
                    for nodeAttribute in self.nodeBody:
                        attributeNum += 1
                        if nodeAttribute[0] == 'disable':
                            self.nodeBody[attributeNum] == ('disable', 'true')
                            disableHave = 1
                    if disableHave == 0:
                        self.nodeBody.append (('disable', 'true'))
                self.freshenNode()    #字符串化,深拷贝
                #return self
            else:
                print ('请输入0(关闭节点)或1(开启节点)')

        else:
            print('这并非是节点')

    def belongGroup (self, groupName):
        self.belongToGroup = groupName