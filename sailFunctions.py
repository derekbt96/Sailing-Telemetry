import numpy as np
import math
import matplotlib.pyplot as plt
from datetime import datetime

class sailData():
    def __init__(self, data_file):
        dataArray = np.load(data_file)
        self.name = 'test'           # Instance variable

        self.lng = dataArray['Bow_Position_longitude']
        self.lat = dataArray['Bow_Position_latitude']
        self.date = dataArray['DateTime_UTC']
        self.Boat_Speed = dataArray['Boat_Speed_ms']*1.94384
        self.Speed_Through_Water = dataArray['Speed_Through_Water_ms']*1.94384
        self.Speed_Over_Ground = dataArray['Speed_Over_Ground_ms']*1.94384
        self.Course_Over_Ground = dataArray['Course_Over_Ground']
        self.True_Wind_Direction = dataArray['True_Wind_Direction']
        self.True_Wind_Speed = dataArray['True_Wind_Speed_ms']*1.94384
        self.True_Wind_Angle = dataArray['True_Wind_Angle']
        self.Apparent_Wind_Speed = dataArray['Apparent_Wind_Speed_ms']*1.94384
        self.Apparent_Wind_Angle = dataArray['Apparent_Wind_Angle']
        self.Velocity_Made_Good = dataArray['Velocity_Made_Good_ms']*1.94384
        self.TWA_Correction = dataArray['TWA_Correction']
        self.TWS_Correction = dataArray['TWS_Correction_ms']*1.94384
        self.depth = dataArray['Depth_m']
        self.Signed_Leeway_Angle = dataArray['Signed_Leeway_Angle']
        self.Course = dataArray['Course']
        self.Heading = dataArray['Heading']
        self.Magnetic_Variation = dataArray['Magnetic_Variation']
        self.Heel = dataArray['Heel']
        self.Trim = dataArray['Trim']
        self.Rudder_Angle = dataArray['Rudder_Angle']
        self.Sea_Temp = dataArray['Sea_TemperatureC']
        self.Tide_Set = dataArray['Tide_Set']
        self.Tide_Rate = dataArray['Tide_Rate_ms']*1.94384
        self.Barometric_Pressure = dataArray['Barometric_Pressure_Pa']
        self.Alarms = dataArray['Alarms']

        self.startIdx = 0
        self.endIdx = len(self.lat)
        self.startIdx = 825
        self.endIdx = 3340
        # self.endIdx = 9093
        self.tStart = datetime.strptime(self.date[0], "%d.%m.%Y %H:%M:%S.%f")
        self.tEnd = datetime.strptime(self.date[-1], "%d.%m.%Y %H:%M:%S.%f")
        self.i = np.arange(self.startIdx,self.endIdx)
        # self.getRacePoint()

        self.calcJ2000()
        self.earth_rad = 6378160
        self.deg2m = (math.pi/180.0)*self.earth_rad
        self.calcPos()        

        self.loadPolars()
        


    def calcJ2000(self):
        # j2k_0 = datetime.strptime('1.1.2000 12:00:00', "%d.%m.%Y %H:%M:%S")
        j2k_0 = datetime.strptime(self.date[self.startIdx], "%d.%m.%Y %H:%M:%S.%f")
        j2k = np.zeros(len(self.date))
        for k in range(len(self.date)):
            temp = datetime.strptime(self.date[k], "%d.%m.%Y %H:%M:%S.%f") - j2k_0
            j2k[k] = temp.total_seconds()
        self.time = j2k

    def calcPos(self):

        dlat = self.lat - self.lat[0]
        dlng = self.lng - self.lng[0]
        PosY = self.deg2m * math.cos(self.lat[0]* math.pi / 180.0) * dlat
        PosX = self.deg2m * dlng
        self.pos = np.array([PosX,PosY])

    def loadPolars(self):
        self.windVel = np.array([6,8,10,12,14,16,20,24])
        self.beatAngles = np.array([41.9,39.8,37.8,36.7,36.1,35.8,35.4,36.1])
        self.windAngles = np.array([52.60,175,90,110,120,135,150])
        self.gybeAngles	= np.array([143.3,146.5,149.8,151.2,150.6,173.5,142.7,141.7])

        self.boatVel = np.array([[4.05, 4.88, 5.40, 5.67, 5.82, 5.91, 6.02,  6.01],
                                 [6.08, 7.06, 7.56, 7.83, 7.99, 8.09, 8.22,  8.27],
                                 [6.36, 7.25, 7.71, 7.99, 8.19, 8.33, 8.49,  8.58],
                                 [6.53, 7.36, 7.81, 8.14, 8.42, 8.65, 8.96,  9.16],
                                 [6.67, 7.58, 8.06, 8.41, 8.67, 8.87, 9.36,  9.84],
                                 [6.56, 7.54, 8.12, 8.57, 9.02, 9.49, 10.41, 11.15],
                                 [6.33, 7.46, 8.07, 8.58, 9.10, 9.59, 10.88, 12.53],
                                 [5.69, 7.01, 7.76, 8.29, 8.83, 9.44, 11.16, 13.41],
                                 [4.82, 6.04, 7.06, 7.72, 8.12, 8.48, 9.63,  12.10],
                                 [4.17, 5.23, 6.11, 6.70, 7.03, 7.47, 8.34,  10.48]])

    def plotRace(self,arr=None):
        if arr is None:
            plt.scatter(self.pos[0,self.i],self.pos[1,self.i])
        else:
            plt.scatter(self.pos[0,self.i],self.pos[1,self.i],c=arr[self.i], cmap='viridis')            
        plt.axis('equal')
        plt.grid()
        plt.show()
        
    def getRacePoint(self):

        plt.scatter(self.pos[0,:],self.pos[1,:])
        plt.axis('equal')
        plt.grid()
        pnts = np.array(plt.ginput(2,mouse_add=3, mouse_pop=None))
        dStart = (self.pos[0,:] - pnts[0,0])**2 + (self.pos[1,:] - pnts[0,1])**2
        dEnd = (self.pos[0,:] - pnts[1,0])**2 + (self.pos[1,:] - pnts[1,1])**2

        self.startIdx = dStart.argmin()
        self.endIdx = dEnd.argmin()
        print(self.startIdx)
        print(self.endIdx)
        self.i = np.arange(self.startIdx,self.endIdx)
        # print(self.pos[:,self.startIdx])
        # print(self.pos[:,self.endIdx])

    def plotTime(self,arr,c):
        if c is not None:
            plt.scatter(self.time[self.i]/60,arr[self.i],c=c[self.i])
        else:
            plt.scatter(self.time[self.i]/60,arr[self.i])

    def plotTime_avg(self,arr,window_size,c):
        weights = np.ones(window_size) / window_size
        arr_avg = np.convolve(arr, weights, mode='valid')
        if c is None:
            plt.scatter(self.time[self.i]/60,arr_avg[self.i])
        else:
            plt.scatter(self.time[self.i]/60,arr_avg[self.i],c=c[self.i])

    def plot(self,arr1,arr2):
        plt.scatter(arr1[self.i],arr2[self.i])

    def plotUpwindPerf(self):
        x = self.Boat_Speed[self.i] * np.cos(np.abs(self.True_Wind_Angle[self.i])*np.pi/180.0)
        y = self.Boat_Speed[self.i] * np.sin(np.abs(self.True_Wind_Angle[self.i])*np.pi/180.0)
        plt.scatter(x,y)
        plt.grid()
        plt.show()