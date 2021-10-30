# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 14:19:57 2021

@author: orens
"""

import pandas as pd

df = pd.read_csv('yad2_moto2.csv')
# %%
# add price fix column without shekel sign
df.insert(9, 'price_fix', df['price'].apply(lambda x: x.split(' ')[0].replace(',', '')))
# %%
# remove no price
df2 = df[df['price_fix'] != 'לא']
# %%
# price_fix to int
df2['price_fix'] = df2['price_fix'].astype(int)

# fix km
# %%
# make a list of fix km columns
s = []
for bike, row in df2.iterrows():
    if (row['km'].split("'")[0] == 'קילומטראז'):
        s.append(row['km'].split("'")[1])
    else:
        s.append('no')
# %%
# insert fix km list
df2.insert(5, 'km_fix', s)
# %%
# remove no km
df3 = df2[df2['km_fix'] != 'no']
df3['km_fix'] = df3['km_fix'].astype(int)
# %%
# fix lising, licence and color
li = []
lic = []
col = []
for bike, row in df3.iterrows():
    if row['lising'].split(' ')[0] == 'מוכן' or row['lising'].split('\n')[0].split(' ')[1] == 'קודמת':
        if row['test'].split('\n')[0].split(' ')[1] == 'נוכחית':
            li.append(row['test'].split('\n')[1])
        else:
            li.append(row['color'].split('\n')[1])
    else:
        li.append(row['lising'].split('\n')[1])
    if row['color'].split('\n')[0] != 'צבע':
        col.append(row['licence'].split('\n')[1])
    else:
        col.append(row['color'].split('\n')[1])
    if row['licence'].split('\n')[0] != 'דרגת רשיון':
        if row['size'] > 500:
            lic.append('A')
        elif row['size'] < 126:
            lic.append('A2')
        else:
            lic.append('A1')
    else:
        lic.append(row['licence'].split('\n')[1].split(' ')[0])
# %%
# add lising, licence and color
df3.insert(6, 'owner', li)
df3.insert(7, 'license', lic)
df3.insert(2, 'color_fix', col)
# %%
# cities.xls is a list of all settelmens in Israel
settle = pd.read_excel('cities.xls')
yeshuv = settle['מחוז ירושלים'].replace('-', ' ')
# %%
area = []
places = pd.DataFrame()
places.insert(0, 'location', df3['location'].drop_duplicates())
# %%
#adds district to dataset
ad = False
north = 69
haifa = 494
center = 592
TA = 834
south = 854
yosh = 1113
gaza = 1241
for i, row in df3.iterrows():
    for j, row2 in settle.iterrows():
        if row['location'] == row2['מחוז ירושלים']:
            if j < 69:
                area.append('jerusalem')
                ad = True
                continue
            elif j < 494:
                area.append('north')
                ad = True
                continue
            elif j < 592:
                area.append('haifa')
                ad = True
                continue
            elif j < 843:
                area.append('center')
                ad = True
                continue
            elif j < 854:
                area.append('tel aviv')
                ad = True
                continue
            elif j < 1113:
                area.append('south')
                ad = True
                continue
            elif j < 1241:
                area.append('yosh')
                ad = True
                continue
            else:
                area.append('gaza')
                ad = True
                continue

    if row['location'] == 'תל אביב יפו':
        area.append('tel aviv')
        ad = True
    elif row['location'] == 'אשדוד':
        area.append('south')
        ad = True
    if ad == False:
        area.append('na')
    ad = False

# %%
df3.insert(12, 'district', area)
# %%
# adds region of maker, eu= Europe, am=USA, jp= Japan
eu = ['AJP', 'MV', 'אפריליה', 'ב.מ.וו', 'בטא', 'גאס-גאס', 'דוקאטי', 'הונדה', 'הוסקוורנה', 'טריומף', 'ק.ט.מ']
jp = ['גולדן', 'ימאהה', 'סוזוקי', 'קאוואסאקי']
am = ['אינדיאן', 'הרלי']
other = ['CF', 'BSE', 'בנלי', 'דיאלים', 'יוסאנג', 'סאן', 'סקיי-טים', 'קיוואי', 'קימקו', 'רויאל']
region = []
for bike, row in df3.iterrows():
    if row['maker'] in eu:
        region.append('eu')
        continue
        print("eu")
    elif row['maker'] in jp:
        region.append('jp')
        continue
    elif row['maker'] in am:
        region.append('am')
        continue
    else:
        region.append('other')
        region.append('other')
# %%
df3.insert(13, 'region', region)
# %%
df4 = df3[df3['district'] != 'na']
# %%
df4.to_csv('moto_cleaned_371.csv')








