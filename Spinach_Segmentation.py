# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:11:16 2019

@author: Alex
"""

import dicom #pip install dicom
import os
import numpy as np
import matplotlib.pyplot as plt
import os
import pydicom  #pip install pydicom
from scipy import ndimage
from skimage.filters import threshold_otsu, threshold_adaptive, try_all_threshold

Make_Img_Folder=1
Thresh=17750


cwd = os.getcwd()
PathDicom = cwd+"/Spinach_DICOM/"
Path_Raw_Imgs=cwd+"/Raw_Images/"


if not os.path.isdir(Path_Raw_Imgs) and Make_Img_Folder==1:    	
    os.mkdir(Path_Raw_Imgs)

lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))

# Get ref file
Lx = int(pydicom.dcmread(lstFilesDCM[0]).Rows)
Ly = int(pydicom.dcmread(lstFilesDCM[0]).Columns)
Lz=len(lstFilesDCM)

Data_3D = np.zeros((Lx,Ly,Lz))

for count, img in enumerate(lstFilesDCM):
    dataset=pydicom.dcmread(img)
    Data_3D[:,:,count]=dataset.pixel_array
    if Make_Img_Folder==1:
        fig, ax = plt.subplots(1,2,figsize=(16,8))
        plt.subplot(121)
        plt.imshow(dataset.pixel_array)
        binary=dataset.pixel_array>Thresh
        im_filt=ndimage.median_filter(binary, 3)
        plt.subplot(122)
        plt.imshow(im_filt)
        fname=Path_Raw_Imgs+img[:-3].split('/')[-1]+'png'
        fig.savefig(fname)
        plt.close()


fig, ax = plt.subplots(1,2, figsize=(9,9))
plt.subplot(121)
plt.hist(Data_3D.flatten(),bins=6000)
plt.xlim(np.min(Data_3D),np.max(Data_3D))
plt.ylim(0,5e5)
plt.grid(True)


plt.subplot(122)
plt.hist(Data_3D.flatten(),bins=6000)
plt.xlim(16000,20000)
plt.ylim(0,15000)
plt.grid(True)
fig.savefig(cwd+'histogram.png')
plt.close()