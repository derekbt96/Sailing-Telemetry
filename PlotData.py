
import numpy as np 
import matplotlib.pyplot as plt
import datetime
import sailFunctions

array_file = 'Sailing/2026-10-11-AYC-Fall-Series/data.npy'


sailData = sailFunctions.sailData(array_file)


# sailData.getRacePoint()

# sailData.plotRace(np.abs(sailData.True_Wind_Angle))



sailData.plotTime(sailData.True_Wind_Angle,None)
sailData.plotTime_avg(np.abs(sailData.True_Wind_Angle),61,None)
sailData.plotTime_avg(np.abs(sailData.Apparent_Wind_Angle),61,None)
plt.grid()
plt.show()


sailData.plotTime_avg(sailData.Velocity_Made_Good,31,np.sign(sailData.Apparent_Wind_Angle))
plt.grid()
plt.show()

sailData.plotTime_avg(sailData.True_Wind_Direction,31,np.sign(sailData.Apparent_Wind_Angle))
sailData.plotTime_avg(sailData.Course_Over_Ground,31,None)
plt.grid()
plt.show()

# UPWIND PERFORMANCE
# sailData.plotUpwindPerf()