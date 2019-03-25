import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
SAMPLES = 3601 # Change this to 3601 for SRTM1
def read_elevation_from_file(hgt_file, lon, lat):
    with open(hgt_file, 'rb') as hgt_data:
        # Each data is 16bit signed integer(i2) - big endian(>)
        elevations = np.fromfile(hgt_data, np.dtype('>i2'), SAMPLES*SAMPLES)\
                                .reshape((SAMPLES, SAMPLES))

        lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
        lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))

        return elevations[SAMPLES - 1 - lat_row, lon_row].astype(int)

#print(read_elevation_from_file("S18W066.hgt",18,66))


elevations = np.fromfile("S18W066.hgt", np.dtype('>i2'), SAMPLES*SAMPLES)\
                                .reshape((SAMPLES, SAMPLES))

print(elevations[0][:])
fig = plt.figure(frameon=True)

plt.imshow(elevations, cmap=cm.terrain)

plt.axis('off')

cbar = plt.colorbar(shrink=0.9)

cbar.set_label('meters')

plt.savefig('plot_name2.jpg', dpi=300, bbox_inches='tight')

plt.show()
