import pandas as pd
import numpy as np
import os

def update_time(y, m, d, hh, mm):
        
    #minute (and hour)
    if mm == 55:
        hh += 1
        mm = 0
    else:
        mm += 5

    #day
    if hh == 24:
        d += 1
        hh = 0

    #month (and year)
    if d >= 29:
        if (m in [1, 3, 5, 7, 8, 10, 12] and d == 32) or (m in [4, 6, 9, 11] and d == 31) or (m == 2 and d == 29):
            if m == 12:
                m = 1
                y += 1
            else:
                m += 1
            d = 1

    return (y, m, d, hh, mm)

#check directory csv and xml
if not os.path.isdir('data_dict'):
    os.mkdir('data_dict')

#init time
y = 2019    #year
m = 1       #month
d = 1       #day
hh = 0      #hour
mm = 0      #minute
time_range = 60 #60 = 5hours = 60(5 minutes)

#init data
data = []
dicts = []

#transer first 60 csv data to dictionary {routeid: [level, value, traveltime]}
for i in range(60):
    path = 'csv/%d%02d%02d%02d%02d.csv' % (y, m, d, hh, mm)
    with open(path, 'r') as csv_file:
        tmp_dict = {}
        for line in csv_file:
            if 'routeid' not in line:
                row = line.split(',')
                tmp_dict[row[0]] = [float(row[1]), float(row[2]), float(row[3].replace('\n', ''))]
        dicts.append(tmp_dict)
    (y, m, d, hh, mm) = update_time(y, m, d, hh, mm)

#init predict time(30 minute later)
predict_y = y
predict_m = m
predict_d = d
predict_hh = hh
predict_mm = mm

for i in range(6):
    (predict_y, predict_m, predict_d, predict_hh, predict_mm) = update_time(predict_y, predict_m, predict_d, predict_hh, predict_mm)

#start merging
while not (m == 8 and d == 16):
    
    #transer current csv data to dictionary {routeid: [level, value, traveltime]}
    print('processing time range end at %d%02d%02d%02d%02d' % (y, m, d, hh, mm))
    try:

        path = 'csv/%d%02d%02d%02d%02d.csv' % (y, m, d, hh, mm)
        with open(path, 'r') as csv_file:
            tmp_dict = {}
            for line in csv_file:
                if 'routeid' not in line:
                    row = line.split(',')
                    tmp_dict[row[0]] = [float(row[1]), float(row[2]), float(row[3].replace('\n', ''))]
            dicts.append(tmp_dict)

    except:
        
        tmp_dict = {}
        for routeid in dicts[0]:
            tmp_dict[routeid] = [-99, -99, -99]
        dicts.append(tmp_dict)
    
    #transer predict csv data to dictionary {routeid: [level, value, traveltime]}
    try:

        path = 'csv/%d%02d%02d%02d%02d.csv' % (predict_y, predict_m, predict_d, predict_hh, predict_mm) 
        with open(path, 'r') as csv_file:
            predict_dict = {}
            for line in csv_file:
                if 'routeid' not in line:
                    row = line.split(',')
                    predict_dict[row[0]] = [float(row[1]), float(row[2]), float(row[3].replace('\n', ''))]
    
    except:

        with open('error_merging_csv_file.txt', 'a') as f:
            f.write('%d%02d%02d%02d%02d.csv\n' % (y, m, d, hh, mm))
        predict_dict = {}
        for routeid in dicts[0]:
            predict_dict[routeid] = [-99, -99, -99]

    
    #collecting data
    for routeid in dicts[0]:
        tmp_data = []
        for tmp_dict in dicts:
            if (routeid in tmp_dict) and (-99 not in tmp_dict[routeid]):    #-99 means no data
                tmp_data.extend(tmp_dict[routeid])
            else:
                break

        if routeid not in predict_dict:
            predict_dict[routeid] = [-99, -99, -99]
        
        if predict_dict[routeid][1] != -99: #-99 means no data
            tmp_data.append(predict_dict[routeid][1])

        if len(tmp_data) == 184:    #184 = 60 * 3(5 hours data) + 3(current data) + 1(predict value)
            data.append(tmp_data)
        else:
            with open('error_end_time_dict.txt', 'a') as f:
                f.write('%d%02d%02d%02d%02d,' % (y, m, d, hh, mm) + routeid + ',' + str(len(tmp_data)) + '\n')
            
    #save data during one hour
    if mm == 55:
        data = np.array(data)
        np.save('data_dict/%d%02d%02d%02d' % (y, m, d, hh), data)
        data = []

    #delete useless data
    del dicts[0]

    #updata time
    (y, m, d, hh, mm) = update_time(y, m, d, hh, mm)
    (predict_y, predict_m, predict_d, predict_hh, predict_mm) = update_time(predict_y, predict_m, predict_d, predict_hh, predict_mm)
