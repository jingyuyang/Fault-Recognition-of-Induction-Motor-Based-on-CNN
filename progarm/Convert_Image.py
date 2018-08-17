# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 16:17:00 2018

@author: Jingyu Yang
"""

import os
import numpy as np
import sys
import time
import random
import shutil
import matplotlib.pyplot as plt

# (1) 生成图片
def convertImage(originalPath,targetPath,label):
  """
  originalPath:原始信号所在路径；
  targetPath:图片保存路径；
  label:电机标签。
  """
  start = time.clock()
  
  os.chdir(originalPath)
  fileNames = os.listdir('.')
  
  for fileName in fileNames:
    name = os.path.splitext(fileName)[0]
    postFix = name.split('_',1)[-1]
    
    if postFix == label:
      targetPath = targetPath + r'\\' + name
      if not os.path.exists(targetPath):
        os.makedirs(targetPath)
        
      data = np.loadtxt(fileName)
      
      num = data.shape[0]
      for i in range(num):
        sys.stdout.write("\rCreating %s images: %d/%d." %(label,i+1,num))
        sys.stdout.flush()
        
        plt.figure(figsize=(4,4),dpi=60)
        plt.xticks([]) #关闭x坐标刻度
        plt.yticks([]) #关闭y坐标刻度
        plt.plot(data[i,:])
        plt.savefig(r"%s\%s_%s.jpg" %(targetPath,label,i+1), bbox_inches='tight')
        plt.close('all')
        
  end = time.clock()
  duration = end - start
  print(r"\nDone. Cost: %.2f sec!\n" %(duration))



# (2)划分数据集
def selectTrTe(imagePath,trainPath,validationPath,testPath):
  fileNames = os.listdir(imagePath)
  num = len(fileNames)
  imageIndex = range(num)
  
  for i in range(2000):       #每种故障随机选取2000张图片作为训练集
    randIndex_Index = random.randint(0,len(imageIndex))
    randIndex = imageIndex[randIndex_Index]
    fileName = fileNames[randIndex]
    shutil.copyfile(os.path.join(imagePath,fileName),os.path.join(trainPath,fileName))
    del(imageIndex[randIndex_Index])
  for i in range(500):        #每种故障随机选取500张照片作为验证集
    randIndex_Index = random.randint(0,len(imageIndex))
    randIndex = imageIndex[randIndex_Index]
    fileName = fileNames[randIndex]
    shutil.copyfile(os.path.join(imagePath,fileName),os.path.join(validationPath,fileName))
    del(imageIndex[randIndex_Index])
  for i in range(500):        #余下500张图片作为测试集
    randIndex = imageIndex[i]
    fileName = fileNames[randIndex]
    shutil.copyfile(os.path.join(imagePath,fileName),os.path.join(testPath,fileName))
    
  
    

# 主函数
if __name__ == "__main__":
  
  # 1)生成图片并保存
  originalPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab原始振动信号-0"
  targetPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab原始振动信号图片数据-0"
  labels = ['0_nor','1_mun','2_brb','3_fbo','4_amis','5_pmis','6_br','7_pun1']
  
  for label in labels:
    convertImage(originalPath,targetPath,label)
    
  
  #2）划分数据集
  trainPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab数据集-0\train_16000"
  if not os.path.exists(trainPath):
    os.makedirs(trainPath)
  
  validationPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab数据集-0\validation_4000"
  if not os.path.exists(validationPath):
    os.makedirs(validationPath)
  
  testPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab数据集-0\test_4000"
  if not os.path.exists(testPath):
    os.makedirs(testPath)
    
  folderPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab原始振动信号图片数据-0"
  folderNames = os.listdir(folderPath)
  
  start = time.clock()
  print("Generating data sets!")
  
  for folderName in folderNames:
    imagePath = os.path.join(folderPath,folderName)
    selectTrTe(imagePath,trainPath,validationPath,testPath)
  
  end = time.clock()
  duration = end - start
  print("Done! Cost: %.2f." %(duration))