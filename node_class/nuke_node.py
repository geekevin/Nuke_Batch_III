#node类
class nukeNode (object):
    def __init__ (self, nodeDict):
        self.nodeHead = nodeDict['main'][0]
        self.nodeBody = nodeDict['main'][1]
        self.nodeFoot = nodeDict['main'][2]
        self.nodeType = nodeDict['nodeType']
        self.nodeLayerNum = nodeDict['layerNumInt']

    def __len__ (self):
        return len(self.nodeBody)+2

    def __str__ (self):
        nodeStr = ' ' * self.nodeLayerNum + self.nodeHead + '\n'
        for nodeAttributeTuple in self.nodeBody:
            nodeAttributeStr = ' '.join (nodeAttributeTuple)
            nodeStr = nodeStr + ' ' * (self.nodeLayerNum + 1) + nodeAttributeStr +'\n'
        nodeStr = nodeStr + ' ' * self.nodeLayerNum + self.nodeFoot
        return nodeStr

    def __repr__ (self):
        '''
        for nodeAttribute in self.nodeBody:
            if nodeAttribute[0] == 'name':
                print(nodeAttribute[1])
                return nodeAttribute[1]
        '''
        return self.__str__()

    def AddNodeAtt (self, attributeTuple): #AddNodeAttribute
        if type(attributeTuple) == tuple:
            self.nodeBody.append (attributeTuple)
        else:
            print ('输入参数并非元组')

    def RepNodeAtt (self, attributeTuple): #ReplaceNodeAttribute
        if type(attributeTuple) == tuple:
            attributeNum = -1
            for nodeAttribute in self.nodeBody:
                attributeNum += 1
                if attributeTuple[0] == nodeAttribute[0]:
                    self.nodeBody[attributeNum] = attributeTuple
        else:
            print ('输入参数并非元组')

    def DelNodeAtt (self, attributeKeys):
        if attributeKeys.isstring():
            attributeNum = -1
            for nodeAttribute in self.nodeBody:
                attributeNum += 1
                if attributeTuple[0] == attributeKeys:
                    self.nodeBody.pop(attributeNum)
        else:
            print ('输入参数并非字符串')