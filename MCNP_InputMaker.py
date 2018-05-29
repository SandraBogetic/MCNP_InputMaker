# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 

@author: Sandra Bogetic
"""

import pandas as pd
import random

"""
choose an input file from the same folder
"""
filename='520sph.csv'
#filename='example_file.inp'
#filename='520test.txt'

"""
this section imports the first part of the input file as a dictionary dict containing all the variables
and the second part as a text string f2
"""
def importfile(filename):
    dict={}
    txtfile=open(filename)
    txt=txtfile.read()
#    [f1, f2]=txt.split('***********************************')
    i=txt.find('Variable')
    txtfile.seek(i)
    print(txtfile.readline())
    for line in txtfile:
        if line[0]=='#':#.rstrip('\n') !='C':
           line=line.rstrip('\n').replace('# <','').replace(' =','=')
           #val, unit=line.split('>')
           variable,value=line.split('=')
           dict[variable]=value
        elif line=='C Cell Cards:': break
            
    print(dict)

    j=txt.find('C Cell Cards')
    txtfile.seek(j)
    print(txtfile.readline())       
    f2=txtfile.read()
    #print(f2)
    return dict, f2

"""
this section converts the dictionary into a dataframe containing columns for
the original values, it's type, lower and upper boundary, an (empty) column for a randomly 
selected value and unit
"""
def dict2df(dict):
    df=pd.DataFrame(index=list(dict.keys()),columns=['values','data type','lower boundary','upper boundary','random value','unit'])
    lowb=[];upb=[];dtype=[];discvals=[];units=[]
    for vals in list(dict.values()):
        vals, unit=vals.split('>')
        unit=unit.replace('  ','')
        try:
            lb=float(vals); ub=float(vals); dv=float(vals); dt='integer'
        except:
            vals=vals.replace(' ','')
            if ':' in vals:
                lb,ub = vals.split(':'); dv=vals; dt='continiuos'  
            elif ',' in vals:
                disc=vals.split(',')
                lb,ub=disc[0],disc[-1]; dt='discrete'
                dv=list(int(x) for x in  disc)   
            elif vals.isdigit() == True and vals[0] == '0':
                lb,ub=vals[0],vals[-1]; dv=list([int(lb), int(ub)]); dt='binary'
            elif vals.isdigit() == True:
                lb,ub=vals[0],vals[-1]; dv=list([int(lb), int(ub)]); dt='combinatory'
            else:
                lb='nan'; ub='nan'; dv=vals; dt='function'
        lowb.append(float(lb));upb.append(float(ub));dtype.append(dt)
        units.append(unit);discvals.append(dv)
                
    df['lower boundary']=lowb; df['upper boundary']=upb; df['data type']=dtype
    df['unit']=units ;df['values']=discvals
    return df

"""
this section assigns a random value within the possible boundaries to each variable and
replaces the variable in f2 by this randomly choosen value
"""
def changef2(df,f2):
    for f in list(df.index):
        if df.loc[f].iloc[1]=='integer':
            f2=f2.replace(f,str(df.loc[f].iloc[2]))
            df.at[f,'random value']=df.loc[f].iloc[2]
        elif df.loc[f].iloc[1]=='discrete':
            r=random.randint(0,len(df.loc[f].iloc[0])-1)
            f2=f2.replace(f,str(df.loc[f].iloc[0][r]))
            df.at[f,'random value']=df.loc[f].iloc[0][r]
        elif df.loc[f].iloc[1]=='continiuos':
            ru=random.uniform(df.loc[f].iloc[2],df.loc[f].iloc[3])
            f2=f2.replace(f,str(ru))
            df.at[f,'random value']=ru
        elif df.loc[f].iloc[1]=='binary':
            r=random.randint(0,1)
            f2=f2.replace(f,str(r))
            df.at[f,'random value']=r
        elif df.loc[f].iloc[1]=='combinatory':
            r=random.randint(0,1)
            f2=f2.replace(f,str(df.loc[f].iloc[r]))
            df.at[f,'random value']=df.loc[f].iloc[r]

    for f in list(df.index):
        if df.loc[f].iloc[1]=='function':
            fct=str(df.loc[f].iloc[0])
            for ff in list(df.index):
                fct=fct.replace(ff,str(df.loc[ff].iloc[4]))
            try:
                fct=eval(fct)
                df.at[f,'random value']=fct
            except:
                print('there is an undefined variable in the function')
            f2=f2.replace(f,str(fct))
    print(f2)
    return df, f2


dict, f2 = importfile(filename)
df=dict2df(dict)
df, f2new = changef2(df, f2)