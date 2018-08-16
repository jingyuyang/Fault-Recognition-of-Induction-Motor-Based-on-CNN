# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 16:17:00 2018

@author: Jingyu Yang
"""

import os
import numpy as np
import sys
import time
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



# 主函数
if __name__ == "__main__":
  originalPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab原始振动信号-0"
  targetPath = r"E:\Spyder\CNN-Vibration-Signal-Eight-Classification\data\Lab原始振动信号图片数据-0"
  #labels = ['0_nor','1_mun','2_brb','3_fbo','4_amis','5_pmis','6_br','7_pun1']
  labels = ['7_pun1']
  
  for label in labels:
    convertImage(originalPath,targetPath,label)