

from libpyvinyl.DiffractionData import DiffractionData
from libpyvinyl.DiffractionData.SimpleFormat import SimpleFormat

import numpy as np

arr = np.arange(9).reshape([3, 3])
distance = 10
diffraction_data = DiffractionData(arr, 10)

diffraction_data.write('test.h5', SimpleFormat)
data_from_file = DiffractionData.read('test.h5', SimpleFormat)

print(data_from_file.array)
print(data_from_file.distance)


