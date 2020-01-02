# levvim 2019
# python clean_data.py -i data/SNR_train_3p.json -o data/SNR_train_3p_clean.csv
################################################################################
import argparse
import pandas as pd
import json
from pandas.io.json import json_normalize 

# parser
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="input file")
parser.add_argument("--output", "-o", help="output file")
args = parser.parse_args()

# load in file and clean up
with open(args.input, encoding='utf-8-sig') as f_input:
        d = pd.read_json(f_input, orient='values')

## split columns that are lists of dictionaries
d_temp=pd.DataFrame(d.userOthers.values.tolist(), index=d.index)
d_temp.columns=['userOthers' + str(col) for col in d_temp.columns]
d=pd.concat([d,d_temp], axis=1).reset_index(drop=True)

d=d.filter(items=['userCurrent', 'userOthers0','userOthers1','userState']) # filter to col
d=d[~d['userOthers1'].isnull()] # remove null values for dropout (TODO appropriate for drop players later)

# split dictionary columns

## normalize 1 column
#d2=d
#d_temp = json_normalize(d['userCurrent'])
#d_temp.columns = ['userCurrent_' + str(col) for col in d_temp.columns]
#d2=pd.concat([d2,d_temp])
#print(d_temp)

## normalize all columns
d2=pd.DataFrame()
for col in d:
    print(col)
    d_col=d[col]
    d_temp=json_normalize(d[col])
    d_temp.columns = [col + '_' + str(i) for i in d_temp.columns]
    d2=pd.concat([d2,d_temp], axis=1).reset_index(drop=True)

# write to file
d2.to_csv(args.output, encoding='utf-8', index=False)
