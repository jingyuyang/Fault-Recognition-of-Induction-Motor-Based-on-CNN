# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:53:45 2018

@author: Jingyu Yang
"""

import os
import numpy as np
import time
import random

# (1)读取原始振动信号并分组
def DataProcess(originalPath,targetPath,preFix,num,m):
  """
  originalPath:原始信号所在位置；
  targetPath：数据处理后保存位置；
  postFix：信号后缀名；
  num：每种故障信号取样数；
  m：单个信号点数。
  """
  
  start = time.clock()
  print("Start processing data!")
  os.chdir(originalPath)
  fileNames = os.listdir('.')
  
  n = 0
  for fileName in fileNames:
    name = os.path.splitext(fileName)[0]
    if name.split('_')[-1] == 'a1':
      if name.split('_')[0] == preFix:
        dataFinal = np.empty((0,m))
        
        dataOriginal = np.loadtxt(fileName)
        length = dataOriginal.shape[0]
        
        for i in range(int(num/20)):
          index = random.randint(0,length-m)
          data = dataOriginal[index:index+m].reshape(1,-1)
          dataFinal = np.append(dataFinal,data,axis=0)
          
        #标准差归一化
        mean = dataFinal.mean(axis=1).reshape(-1,1)
        std = dataFinal.std(axis=1).reshape(-1,1)
        dataFinal = (dataFinal-mean)/std
        
        print('Signal:%s; Shape:%s.' %(preFix,dataFinal.shape))
        print('Writing %s data.' %(preFix))
        np.savetxt(r'%s\%s×%s_%s_%s.txt' %(targetPath,dataFinal.shape[0],dataFinal.shape[1],n,preFix))
        n += 1
  
  end = time.clock()
  duration = end - start
  print("Data processing complete! Taking time: %.2f sec.\n" %(duration))
  

#主函数
if __name__ == "__main__":
  originalPath = r"G:\杨景宇\毕设资料\驱动电机\感应电机\原始数据\Fault simulator"
  targetPath = r"E:\Spyder\CNN-Vibration signal eight classification\data\Lab原始振动信号-0"
  if not os.path.exists(targetPath):
    os.makedirs(targetPath)
  preFixes = ['nor','mun','brb','fbo','amis','pmis','br','pun1']
  num = 3000
  m = 256
  
  for preFix in preFixes:
    DataProcess(originalPath,targetPath,preFix,num,m)