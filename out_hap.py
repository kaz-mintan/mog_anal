#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import re
import os
import okao_func

import numpy as np
import cv2

from datetime import datetime



def tmp_log(array,now):
    log_array = np.empty((1,array.shape[0]+5))
    log_array[0,:array.shape[0]]=array
    log_array[0,array.shape[0]:]=\
    np.array([now.day,now.hour,now.minute,now.second,now.microsecond])
    return log_array

width = 320*3
height = 240

print("input dirname")
inputDir = raw_input()

#inputDir  = "/home/kazumi/prog/table_design/pic/az_test/"

numbers = re.compile(r'(\d+)')

def numericalSort(value):
  parts = numbers.split(value)

  parts[1::2] = map(int, parts[1::2])
  return parts


okao_1 = okao_func.Okao()
okao_1.create_handle()
c = 0


for inputPath in sorted(glob.glob(inputDir + '*.png'), key=numericalSort):
  filename = os.path.basename(inputPath)
  frame = cv2.imread(inputPath)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  res = cv2.resize(gray,(width,height))


  a_1 = np.array(res[:,:320],dtype=np.uint8)
  a_2 = np.array(res[:,320:640],dtype=np.uint8)
  a_3 = np.array(res[:,640:],dtype=np.uint8)

  cv2.imshow("pic",np.hstack((a_1,a_2,a_3)))

  #cv2.imshow('show',frame)
  cv2.waitKey(1)
  conf = np.zeros((3,13,2000))
  hap = np.zeros((3,1,2000))
  gaze = np.zeros((3,2,2000))
  face_pt = np.zeros((3,8,2000))

  #remove this comment out if you need output confidence and happy
  for i in range(3):
    if i == 0:
      okao_1.set_frame(a_1, 3.0)
    elif i==1:
      okao_1.set_frame(a_2, 3.0)
    elif i==2:
      okao_1.set_frame(a_3, 3.0)
    count = okao_1.face_detect()
    for index in range(count):
      if index == 0:
        okao_1.get_face(0,0)
        okao_1.get_parts(0,0)

        okao_1.get_gaze(0)
        #gaze[i,0,c] = okao_1.gaze_1()
        #gaze[i,1,c] = okao_1.gaze_2()

        okao_1.get_emotion(0)

        hap[i,0,c] = okao_1.ret_emo()[1]

  print(filename,hap[0,0,c],
      hap[1,0,c],
      hap[2,0,c])

  with open('test_state.csv', 'a') as rf_handle:
      np.savetxt(rf_handle,
      #tmp_log(np.hstack((np.array([episode]),np.array([while_t]),tmp_state[:,0])),datetime.now()),fmt="%f",delimiter=",")
      tmp_log(hap[:,0,c],datetime.now()),fmt="%f",delimiter=",")

  c = c +1

#if __name__ == '__main__':
