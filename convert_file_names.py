import os

path = 'C:\\Users\\student\\KU Leuven\\LUCA Oxytocine - 3D\\Zorgfiguur audio\\ADDAEXPORTAUDIOCLIPS\\80_cont'
filenames = os.listdir(path)
for filename in filenames:
    print(filename)
    os.rename(os.path.join(path,filename), os.path.join(path,filename.replace(' ', '_').lower()))
