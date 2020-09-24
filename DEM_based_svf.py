import numpy as np
import numpy.matlib
from osgeo import ogr
from osgeo import gdal
from gdalconst import *
import os,sys,time
import math

start_time = time.time()

os.chdir(r'F:\svf_cal')

driver = ogr.GetDriverByName('ESRI Shapefile')
#打开矢量
ds = driver.Open('Export_Output_2.shp',1)
if ds is None:
    print('Could not open ')
    sys.exit(1)
#获取图层
layer = ds.GetLayer()

#获取要素及要素地理位置
xValues = []
yValues = []
feature = layer.GetNextFeature()
while feature:
    geometry = feature.GetGeometryRef()
    x = geometry.GetX()
    y = geometry.GetY()
    xValues.append(x)
    yValues.append(y)
    feature = layer.GetNextFeature()

#获取所有注册类
gdal.AllRegister()
#打开栅格
path = r"F:\svf_cal\Reclass_tif21.tif"
dataset = gdal.Open(path)
if ds is None:
    print('Could not open image')
    sys.exit(1)

#获取行列、波段
rows = dataset.RasterYSize
cols = dataset.RasterXSize
bands = dataset.RasterCount
#获取放射变换信息
transform = dataset.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]
values = []
for i in range(len(xValues)):
    x = xValues[i]
    y = yValues[i]
    #获取点位所在栅格的位置
    xOffset = int((x-xOrigin)/pixelWidth)
    yOffset = int((y-yOrigin)/pixelHeight)

    #s = str(int(x)) + ' ' + str(int(y)) + ' ' + str(xOffset) + ' ' + str(yOffset) + '

radius = 501 #半径

#α = float(α)
S= 0
for α in range(0,359):
    α = math.degrees(α)
    #data = []
    m = 0
    for r in range(1,radius):#得到α角度下，最大高度值
        X = xOffset + r * np.cos(α)#点坐标
        Y = yOffset + r * np.sin(α)
        band = dataset.GetRasterBand(1)  # 取第1波段
        h = band.ReadAsArray(X, Y, 1, 1)  # 从数据的中心位置位置开始，取1行1列数据,得到高度
        D = r
        β = np.arctan((h - 1.5) / D)
        #m = data.append(β)
        #p = max(m)
        if β > m:
            m = β
        else:
            m = m
        #print(p)
        #print(h)
    s = (np.sin(m))**2
    #print(s)
    S = S + s
    #print(S)
SVF1 = 1-(1/360)*S


print(S)
print(SVF1)




