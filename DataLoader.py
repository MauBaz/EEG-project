from os.path import isfile
import zipfile
import numpy as np
import random


# For MU device data we are examining 
hertz = 264
channels = 14 
dataset_path = './data/EP.zip'

def get_zipf():
    if not isfile(dataset_path):
        import urllib
        origin = (
            'http://www.mindbigdata.com/opendb/MindBigData-EP-v1.0.zip'
        )
        print 'Downloading data from %s' % origin
        urllib.urlretrieve(origin, dataset_path)
    return open(dataset_path, 'rb')

def getdata():
    
    f = get_zipf()
    zf = zipfile.ZipFile(f)
        
    data = zf.open('EP.txt', 'r')
    entire_dataset = []
    current_event = np.zeros(hertz * channels + 2)
    i = 0
    maxs = [-100000000 for z in range(channels)]
    mins = [100000000 for j in range(channels)]
    print ('Going through data, please be patient perhaps go make some tea it will take 5-10 mins to load up')
    for l in data:
        id, event, device, channel, code, size, data = l.split('\t')

        signals = np.array([int(val) for val in data.split(',')])
       
        current_event[1+ i*hertz:1+ i*hertz + min(len(signals), hertz)] = signals[:hertz] 
        
        
        if i == channels: # we assume all channels from an event are in sequence
            current_event[-1] = int(code)
            current_event[0] = min(len(signals), hertz)

            entire_dataset.append(current_event)
            current_event = np.zeros(hertz * channels + 2)
            i = 0

    random.seed(111) # deterministic
    random.shuffle(entire_dataset)

    entire_dataset = np.array(entire_dataset)
    print('## Sanity check')
    unique, counts = np.unique(entire_dataset[:,-1], return_counts=True)
    Countdigits = dict(zip(unique, counts))
    print('Printing unique counts of each digit')
    print(Countdigits)
    # Return train and test 
    return entire_dataset[:int(65000*0.75)], entire_dataset[int(65000*0.75):]

