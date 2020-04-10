import numpy as np

def update_time(y, m, d, h):
        
    #day
    if h == 23:
        d += 1
        h = 0
    else:
        h += 1

    #month (and year)
    if d >= 29:
        if (m in [1, 3, 5, 7, 8, 10, 12] and d == 32) or (m in [4, 6, 9, 11] and d == 31) or (m == 2 and d == 29):
            if m == 12:
                m = 1
                y += 1
            else:
                m += 1
            d = 1

    return (y, m, d, h)

#init time
y = 2019    #year
m = 7       #month
d = 15       #day
h = 0      #hour

#int len
data_len = 0

#calculate total length of data
while not(m == 8 and d == 16):
    
    time = '%d%02d%02d%02d' % (y, m, d, h)
    if h == 0:
        print(time[:-2])
    tmp_data = np.load('data_dict/' + time + '.npy')
    if len(tmp_data.shape) == 2 and tmp_data.shape[1] == 184:
        data_len += tmp_data.shape[0]
    (y, m, d, h) = update_time(y, m, d, h)

print(data_len)

#init time
y = 2019    #year
m = 7       #month
d = 15       #day
h = 0      #hour

#init data
data = np.zeros((data_len, 184))
tmp_len = 0

#get .npy data until 08/15
while not(m == 8 and d == 16):
    
    time = '%d%02d%02d%02d' % (y, m, d, h)
    tmp_data = np.load('data_dict/' + time + '.npy')
    print(time)
    if len(tmp_data.shape) == 2 and tmp_data.shape[1] == 184:
        data[tmp_len:tmp_len + tmp_data.shape[0]] = tmp_data
        tmp_len += tmp_data.shape[0]
    (y, m, d, h) = update_time(y, m, d, h)

#shuffle data
np.random.seed(9487)
np.random.shuffle(data)

#split data to train : val : test = 6 : 2 : 2
train_num = int(np.round(data_len * 6 / 10))
test_num = int(np.round(data_len * 2 / 10))
val_num = data_len - train_num - test_num
np.save('train_data', data[:train_num])
np.save('val_data', data[train_num:train_num + val_num])
np.save('test_data', data[train_num + val_num:])
