# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km...
#   converts sez to ecef frame

# Parameters: sez coordinates
#   o_lat_deg: 
#   o_lon_deg: 
#   o_hae_km: 
#   s_km: 
#   e_km: 
#   z_km:

# Output: ecef coordinates
#   ecef_x_km:
#   ecef_y_km:
#   ecef_z_km:
#
# Written by Nick Dickson

# import Python modules
import math # math module
import sys # argv
import numpy as np #matrix math

# constants
R_E_KM = 6378.137
E_E    = 0.081819221456

## calculate demoninator
# (eccentricity, latitude in radians)
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-ecc**2.0 * math.sin(lat_rad)**2.0)

# initialize script arguments
o_lat_deg = float('nan') 
o_lon_deg = float('nan') 
o_hae_km = float('nan') 
s_km = float('nan') 
e_km = float('nan') 
z_km = float('nan') 

# parse script arguments
if len(sys.argv) == 7:
  o_lat_deg = float(sys.argv[1])
  o_lon_deg = float(sys.argv[2])
  o_hae_km = float(sys.argv[3])
  s_km = float(sys.argv[4])
  e_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
    'Usage: '\
    'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
  exit()

### script below this line ###
#Used Slides 6 for Reference
# calculate
lat_rad = o_lat_deg*2*math.pi/360
lon_rad= o_lon_deg*2*math.pi/360
denom = calc_denom(E_E, lat_rad)

#Rotations for SEZ to ECEF
sez = np.array([s_km,e_km,z_km])
Ry = np.array([[math.sin(lat_rad),0,math.cos(lat_rad)],
    [0,1,0],
    [-math.cos(lat_rad),0,math.sin(lat_rad)]])
Rz = np.array([[math.cos(lon_rad),-math.sin(lon_rad),0],
      [math.sin(lon_rad),math.cos(lon_rad),0],
      [0,0,1]])
recef_rot1 = np.dot(Ry,sez)
recef_rot2 = np.dot(Rz,recef_rot1)

#Ecef to SEZ origin
Ce = R_E_KM/denom
Se = R_E_KM*(1-E_E**2)/denom
r_x = (Ce + o_hae_km)*math.cos(lat_rad)*math.cos(lon_rad)
r_y = (Ce + o_hae_km)*math.cos(lat_rad)*math.sin(lon_rad)
r_z = (Se + o_hae_km)*math.sin(lat_rad)

ecef_x_km = r_x + recef_rot2[0]
ecef_y_km = r_y + recef_rot2[1]
ecef_z_km = r_z + recef_rot2[2]

print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)
