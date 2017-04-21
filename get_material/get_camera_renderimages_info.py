#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
import os, sys, csv, glob    #_thread, glob, random
#os.sys.path.append (sys.path[0])
#print(os.getcwd())

# 添加字典
def dictAdd(dictA, keyB):
    if not keyB in dictA.keys():  # 第一次遇到该镜头
        dictA[keyB] = dict()  # 在dictA字典中建立以当前变量keyB为键的空子字典
    return dictA  # 返回字典

def GCRI (projectName, projectPath, projectSettingsDict, EP, programPathMain):    #getCameraRenderimagesInfo(获得摄像机渲染序列信息)
    print ('在GCRI中')
    
    #更改主路径
    os.chdir(programPathMain)
    
    from get_info.get_cameras_motion_data import getCamerasMotionData
    
    #筛选
    def Screening (screeningObject, screeningKeysList, method):    #被筛选对象, 筛选关键字, 筛选模式 -1为排除模式/ 1为适配模式
        if type (screeningObject) is str:    #screeningObject得是字符串
            #method值为-1或1
            if method == -1:    #排除
                e = 0
                for screeningKeys in screeningKeysList:
                    if screeningKeys in screeningObject:    #排除对象
                        e = 1
                #循环结束后判定
                if e == 0:
                    return True
                elif e == 1:
                    return False
                
            if method == 1:    #适配
                e = 0
                for screeningKeys in screeningKeysList:
                    if screeningKeys in screeningObject:    #有适配
                        e = 1    #一旦遇到就判定
                        return screeningKeys
                if e == 0:    #没有找到适配
                    return False
    
    def ACRI (EP, projectSettingsDict, extList, exclusionKeysDict, camerasFrameDict, camerasMotionDataDict):   #appendCameraRenderimagesInfo(获得摄像机渲染序列信息)    #episode, Renderimages_Path, cameraKeyRange_Path, cameraKeysFolderDir, cameraFormat, cameraFps
        print('在ACRI中')
        
        #获得图像序列范围============================================
        def getImageFrameRange (imageFrameList):    #图像序列列表
            #print (imageFrameList)
            imageFrameNumList = list ()  # 创建空列表
            for imageFrameNameStr in imageFrameList:    #循环图像系列列表
                imageFrameNameStr = imageFrameNameStr.split('.')[0]  # 分片CameraNameStr，把序列帧文件的后缀名分割出去
                imageFrameNumInt = int (imageFrameNameStr.split('_')[-1])  # 提取出文件名中的帧数序号，转为整数类型
                imageFrameNumList.append(imageFrameNumInt)  # 添加进NumList列表
            first_frame = min (imageFrameNumList)  # 用min找出列表中的最小值，作为起始帧
            last_frame = max (imageFrameNumList)  # 用max找出列表中的最大值，最为结束帧
            #print (first_frame, last_frame)
            return first_frame, last_frame    #返回起始帧和结束帧
        
        
        projectDict = {'cameras':{}}    #创建空字典包含'cameras'子字典
        renderimagesInfo = [] #渲染素材信息,这里需要每个镜头有顺序所以是列表
        #keysDict = {}    #这个字典专门存放每个素材的最后一帧，用于获取每个镜头的最后帧
        Renderimages_Path = projectSettingsDict['project']['comprehensive_renderimages_path'][0].replace ('``', projectSettingsDict['project']['name'][0]) + 'EP' + EP + '\\'
        #↑↑↑↑↑渲染序列素材路径,精确到指定集数
        
        for dirName, dirs, files in os.walk(Renderimages_Path):
            if Screening (dirName, exclusionKeysDict['folder']['global'], -1):
                #print (dirName)
                if len(files) > 0 and Screening(files[0], extList, 1):    #如果文件夹里有文件和这个文件是图像文件, files是一个列表,列表中包含文件夹中的每个文件,假如是空列表也就表示这个文件夹里没有东西
                    ext = Screening(files[0], extList, 1)
                    #print (ext)
                    imageFrameNameStr = '_'.join(files[0].split('_')[0:-1])    #序列文件名,原变量名filesName
                    imageFrameList = [material for material in files if Screening(material, extList, 1)]    #提取图像序列,原变量名successionList
                    framePadding = len(imageFrameList[0].split('.')[0].split('_')[-1])    #获得序列数字位数framePadding,确定数字序列格式是001还是0001还是00001
                    cameraFolder = dirName.split('\\')[-2]    #每个镜头文件夹的名字, 如EP001_SC117_Fin_T75
                    if '_' in cameraFolder:    #一般镜头文件夹的名字里含有"_", 如EP001_SC117_Fin_T75, 没有"_"就说明不是镜头文件夹
                        cameraFolderList = cameraFolder.split('_')    #镜头文件夹名字的分片
                        episode, shot = projectSettingsDict['project']['camera_name_example'][0].split('_')
                        if episode in cameraFolderList[0] and shot in cameraFolderList[1] and not 'old' in cameraFolderList:    #排除掉不是镜头的文件夹
                            cameraName = '_'.join(cameraFolderList[:2])  # 处理镜头命名，去镜头名字的前两个部分. 一旦命名不符合规范就会跳过
    
                            materialFolder = dirName.split('\\')[-1]    #层文件夹
                            
                            projectDict['cameras'] = dictAdd(projectDict['cameras'], cameraName)    #添加镜头
                            projectDict['cameras'][cameraName] = dictAdd(projectDict['cameras'][cameraName], 'Read')    #添加Read
                            projectDict['cameras'][cameraName]['Read'] = dictAdd(projectDict['cameras'][cameraName]['Read'], cameraFolder)    #添加镜头文件夹
                            projectDict['cameras'][cameraName]['Read'][cameraFolder] = dictAdd(projectDict['cameras'][cameraName]['Read'][cameraFolder], materialFolder)
                            
                            #Root
                            projectDict['cameras'][cameraName] = dictAdd(projectDict['cameras'][cameraName], 'Root')
                            for cameraSettingsKey in projectSettingsDict.keys():
                                if cameraSettingsKey == 'Root':
                                    for roots in projectSettingsDict['Root'].keys():
                                        projectDict['cameras'][cameraName]['Root'][roots] = projectSettingsDict[cameraSettingsKey][roots][0]
                            projectDict['cameras'][cameraName]['Root']['first_frame'] = projectSettingsDict['Root']['first_frame'][0]  # nuke起始帧
                            
                            #Read
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['enable'] = 0
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['first'], \
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['last'] = getImageFrameRange (imageFrameList)  # 帧数范围
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['origfirst'], \
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['origlast'] = \
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['first'], \
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['last']  # 真实素材帧数范围
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['format'] = \
                            projectDict['cameras'][cameraName]['Root']['format']  # 素材的画幅宽高比，这里全部统一
                            '''
                            keysDict = dictAdd (keysDict, cameraName)    #keysDict字典添加镜头号
                            keysDict[cameraName] = dictAdd (keysDict[cameraName], cameraFolder)    #keysDict字典对应镜头号中添加镜头文件夹
                            keysDict[cameraName][cameraFolder][materialFolder] = projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['last']  # 把最后帧范围存进keysDict字典
                            '''
    
                            # 处理素材的路径
                            if len(imageFrameList) > 1:  #序列是有很多帧的情况
                                projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['file'] = os.path.join(dirName, imageFrameNameStr + '_%0' + str(framePadding) + 'd' + ext)
                            else:  # 单帧的情况下
                                projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['file'] = os.path.join(dirName, imageFrameList[0])
                            projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['file'] = projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['file'].replace('\\', '/')
                            # print(projectDict['cameras'][cameraName]['Read'][cameraFolder][materialFolder]['file'])
                            
                            #Write, 处理输出信息
                            projectDict['cameras'][cameraName]['Write'] = {}
                            projectDict['cameras'][cameraName]['Write']['file'] = '%sEP%s/output/%s/%s.####.%s' % (projectSettingsDict['output']['path'][0].replace ('``', projectSettingsDict['project']['name'][0]), EP, cameraName, cameraName, projectSettingsDict['output']['ext'][0])    #输出路径
                            #print (projectDict['cameras'][cameraName]['Write']['file'])
                            for writeDict in projectSettingsDict['write'].keys():
                                projectDict['cameras'][cameraName]['Write'][writeDict] = projectSettingsDict['write'][writeDict][0]    #通过从外部文档调用把Write节点中一些需要变动的属性进行更改
        #print('↓↓↓↓↓↓↓\n' + str(projectDict))
        
        #添加镜头长度
        for camerasFrameKey in camerasFrameDict.keys ():
            if camerasFrameKey in projectDict['cameras'].keys ():
                projectDict['cameras'][camerasFrameKey]['Root']['last_frame'] = camerasFrameDict[camerasFrameKey]  # nuke结束帧
                projectDict['cameras'][camerasFrameKey]['Root']['frame'] = camerasFrameDict[camerasFrameKey]  # 查看下旧版本的文件，看看是否需要+1
                
        #添加镜头运动数据
        for camerasMotionDataNameStr in camerasMotionDataDict.keys():
            if camerasMotionDataNameStr in projectDict['cameras']:
                projectDict['cameras'][camerasMotionDataNameStr]['camerasMotion'] = camerasMotionDataDict[camerasMotionDataNameStr]
                projectDict['cameras'][camerasMotionDataNameStr]['camerasMotion']['camerasMotionEnable'] = 0
            else:
                projectDict['cameras'][camerasMotionDataNameStr] = dict()
                projectDict['cameras'][camerasMotionDataNameStr]['camerasMotion'] = camerasMotionDataDict[camerasMotionDataNameStr]
                projectDict['cameras'][camerasMotionDataNameStr]['camerasMotion']['camerasMotionEnable'] = 0
                
        return projectDict
        
        
    ###########################################主##############################################################
    
    #完整EP
    EPXXX = projectSettingsDict['project']['camera_name_example'][0].split ('_')[0] + EP
    
    ####获取图片后缀列表###
    extListOpen = open('./data/imagesExt.csv', mode='r', encoding='utf-8')  # 路径外部指定
    extListCsv = csv.reader(extListOpen)
    for extListLine in extListCsv:
        extList = extListLine
    #print(extList)
    extListOpen.close()
    
    ####获得排除列表####
    exclusionKeysListOpen = open('./data/exclusionKeys.csv', mode='r', encoding='utf-8')  # 路径外部指定
    exclusionKeysListCsv = csv.reader(exclusionKeysListOpen)
    exclusionKeysDict = dict()  # 设置信息字典
    for exclusionKeysListLine in exclusionKeysListCsv:
        exclusionKeysDict = dictAdd(exclusionKeysDict, exclusionKeysListLine[0])
        exclusionKeysDict[exclusionKeysListLine[0]][exclusionKeysListLine[1]] = exclusionKeysListLine[2:]    #存到信息字典里
    #print(exclusionKeysDict)
    exclusionKeysListOpen.close()
    
    ####获得镜头长度###
    camerasFrameDict = dict ()    #镜头长度字典
    camerasFrameListOpen = open(projectSettingsDict['project']['camera_data_path'][0].replace ('``', projectSettingsDict['project']['name'][0]) + EPXXX + '\\' + EPXXX + '.csv', mode='r', encoding='utf-8')  # 路径外部指定
    camerasFrameListCsv = csv.reader(camerasFrameListOpen)
    for camerasFrameListLine in camerasFrameListCsv:
        camerasFrameDict[projectSettingsDict['project']['camera_name_example'][0].replace ('_', EP + '_') + camerasFrameListLine[0]] = camerasFrameListLine[1]
    #print(camerasFrameDict)
    camerasFrameListOpen.close()
    
    ####获得镜头运动数据####
    camerasMotionDataDict = getCamerasMotionData (projectSettingsDict, EPXXX, programPathMain)
    #print (camerasMotionDataDict)
    
    return ACRI (EP, projectSettingsDict, extList, exclusionKeysDict, camerasFrameDict, camerasMotionDataDict)