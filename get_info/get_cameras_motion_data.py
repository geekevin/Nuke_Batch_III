#! /user/bin/python
#-*-coding:UTF-8-*-
#pragma execution_character_set("utf-8")
import os, csv, glob
####获得镜头运动数据####
def getCamerasMotionData (projectSettingsDict, EPXXX, programPathMain):
    os.chdir (programPathMain)
    camerasMotionDataDict = dict()    #原变量名cameraKeyFileDict
    #print (projectSettingsDict['project']['camera_data_path'][0].replace ('``', projectSettingsDict['project']['name'][0]) + EPXXX + '\\Cam_val\\*.csv')
    for camerasMotionDataFileDirStr in glob.glob(projectSettingsDict['project']['camera_data_path'][0].replace ('``', projectSettingsDict['project']['name'][0]) + EPXXX + '\\Cam_val\\*.csv'):
        camerasMotionDataFileNameStr = camerasMotionDataFileDirStr.split('\\')[-1]
        if EPXXX in camerasMotionDataFileNameStr:  # 识别csv文本文档是否是镜头运动文件
            # print(cameraKeyFileNameStr)
            camerasMotionDataNameStr = camerasMotionDataFileNameStr.split('.')[0]  # 得到镜头号
            # print (cameraKeyNameStr)
            camerasMotionDataDict[camerasMotionDataNameStr] = {}  # 创建镜头号内部字典
            camerasMotionDataDict[camerasMotionDataNameStr]['Camera2'] = {}
            camerasMotionDataDict[camerasMotionDataNameStr]['TransformGeo'] = {}
            camerasMotionDataOpen = open (camerasMotionDataFileDirStr, mode='r', encoding='utf-8')
            camerasMotionDataCsv = csv.reader (camerasMotionDataOpen)
            for camerasMotionDataLineList in camerasMotionDataCsv:
                if len(camerasMotionDataLineList[1:]) == 1:
                    camerasMotionDataLineStr = camerasMotionDataLineList[0] + ' {{curve x1 %s}}' %camerasMotionDataLineList[1]
                    camerasMotionDataDict[camerasMotionDataNameStr]['Camera2'][camerasMotionDataLineList[0]] = camerasMotionDataLineStr
                elif len(camerasMotionDataLineList[1:]) == 3:
                    camerasMotionDataLineStr = camerasMotionDataLineList[0] + ' {{curve x1 %s} {curve x1 %s} {curve x1 %s}}' %(camerasMotionDataLineList[1], camerasMotionDataLineList[2], camerasMotionDataLineList[3])
                    camerasMotionDataDict[camerasMotionDataNameStr]['Camera2'][camerasMotionDataLineList[0]] = camerasMotionDataLineStr
                    TransformGeoStr = camerasMotionDataLineList[0] + ' {%s %s %s}' % (camerasMotionDataLineList[1].split(' ')[0], camerasMotionDataLineList[2].split(' ')[0], camerasMotionDataLineList[3].split(' ')[0])
                    camerasMotionDataDict[camerasMotionDataNameStr]['TransformGeo'][camerasMotionDataLineList[0]] = TransformGeoStr
    return camerasMotionDataDict