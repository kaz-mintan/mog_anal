#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import numpy as np

from matplotlib import pyplot as plt

imu_min_col = 6
imu_sec_col = 7
imu_usec_col = 8

hrt_min_col = 4
hrt_sec_col = 5
hrt_usec_col = 6

dir_name = os.listdir("../new_exp")
files = os.listdir("../new_exp/"+dir_name[0])

ad_path = sorted(glob.glob("../new_exp/"+dir_name[0]+"/ad*.csv"))
split_list = np.array(ad_path)
split_time = np.zeros((6,len(ad_path)))


#==========
im_path = glob.glob("../new_exp/"+dir_name[0]+"/imu*.csv")
imu = np.loadtxt(im_path[0],delimiter=",")

imu_sep_row=np.zeros(len(ad_path)+2)
imu_sep_row[0] = 0
imu_sep_row[-1] = imu.shape[0]

#==========
hrt = np.loadtxt("../heart_out.csv",delimiter=",")

hrt_sep_row=np.zeros(len(ad_path)+2)
hrt_sep_row[0] = 0
hrt_sep_row[-1] = hrt.shape[0]
#==========

for i in range(len(ad_path)):

    split_time[0,i]= split_list[i][35:39]
    split_time[1,i]= split_list[i][39:41]
    split_time[2,i]= split_list[i][41:43]
    split_time[3,i]= split_list[i][44:46]
    split_time[4,i]= split_list[i][46:48]
    split_time[5,i]= split_list[i][48:50]

    for row in range(imu.shape[0]):
        imu_min = imu[row,imu_min_col]
        imu_sec= imu[row,imu_sec_col]
        imu_usec = imu[row,imu_usec_col]

        if  imu_min == split_time[4,i]:
            if imu_sec == split_time[5,i]:
                if imu_usec > 0 and imu_usec < 1000:
                    imu_sep_row[i+1] = row

    for row in range(hrt.shape[0]):
        hrt_min= hrt[row,hrt_min_col]
        hrt_sec= hrt[row,hrt_sec_col]
        hrt_usec = hrt[row,hrt_usec_col]

        if  hrt_min == split_time[4,i]:
            if hrt_sec == split_time[5,i]:
                if hrt_usec > 0 and hrt_usec < 500000:
                    hrt_sep_row[i+1] = row
                    print row



for i in range(len(ad_path)):
    imu_filename = "imu_sep_" + str(i) + ".csv"
    hrt_filename = "hrt_sep_" + str(i) + ".csv"
    np.savetxt(imu_filename,imu[int(imu_sep_row[i]):int(imu_sep_row[i+1]),:],delimiter=",")
    np.savetxt(hrt_filename,hrt[int(hrt_sep_row[i]):int(hrt_sep_row[i+1]),:],delimiter=",")

    plt.subplot(411)
    plt.ylabel("ax")
    plt.plot(imu[int(imu_sep_row[i]):int(imu_sep_row[i+1]),0])

    plt.subplot(412)
    plt.ylabel("ay")
    plt.plot(imu[int(imu_sep_row[i]):int(imu_sep_row[i+1]),1])

    plt.subplot(413)
    plt.plot(hrt[int(hrt_sep_row[i]):int(hrt_sep_row[i+1]),0])
    plt.ylim(0,1024)
    plt.ylabel("pressure of grip")

    plt.subplot(414)
    plt.plot(hrt[int(hrt_sep_row[i]):int(hrt_sep_row[i+1]),1])
    plt.ylim(0,1024)
    plt.ylabel("heart beat")
    plt.show()
