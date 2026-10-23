
import numpy as np 
import datetime
from pathlib import Path
import sailFunctions

log_folder = 'Sailing/2026-10-11-AYC-Fall-Series'


folder_path = Path(log_folder)

# Filter to get only files
files = list(folder_path.glob("*.csv"))

data = None

for file_name in files:
    print(file_name)
    if data is None:
        data = np.genfromtxt(file_name, delimiter=',', dtype=None, names=True)
        print(np.genfromtxt(file_name, delimiter=',', dtype=None, names=True))
    else:
        temp = np.genfromtxt(file_name, delimiter=',', dtype=None, names=True)  
        data = np.append(data, temp, axis=0)

del_idx = np.isnan(data['Course'])

print(data.shape)
data = np.delete(data, del_idx, axis=0)
print(data.shape)


array_file = log_folder+'/data_array.npy'
np.save(array_file,data)

# sailData = sailFunctions.sailData(array_file)

# sail_file = log_folder+'/sailFile.npy'
# np.save(sail_file,sailData)

