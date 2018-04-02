# coding:utf-8
import pandas as pd
import numpy as np

# =================================================
def parcel_round_air(x):
    if x>=1:
        if round((x-int(x)),2)>=0.97:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x > 0.01:
            x= 1
        else:
            x= 0
    return x

def parcel_round_land(x):
    if x>=1:
        if round((x-int(x)),2)>=0.99:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x > 0.05:
            x= 1
        else:
            x= 0
    return x

# ==================================================
def small_round_air(x):
    if x>=1:
        if round((x-int(x)),2)>=0.6:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.01:
            x= 1
        else:
            x= 0
    return x

def small_round_land(x):
    if x>=1:
        if round((x-int(x)),2)>=0.55:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.3:
            x= 1
        else:
            x= 0
    return x

# ====================================================
def nc_round_air(x):
    if x>=1:
        if round((x-int(x)),2)>=0.98:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.02:
            x= 1
        else:
            x= 0
    return x

def nc_round_land(x):
    if x>=1:
        if round((x-int(x)),2)>=0.6:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.08:
            x= 1
        else:
            x= 0
    return x
# ==========================================================
def irregular_round_air(x):
    if x>=1:
        if round((x-int(x)),2)>=0.98:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.02:
            x= 1
        else:
            x= 0
    return x

def irregular_round_land(x):
    if x>=1:
        if round((x-int(x)),2)>=0.99:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.27:
            x= 1
        else:
            x= 0
    return x
# ========================================================
def mail_round_air(x):
    if x>=1:
        if round((x-int(x)),2)>=0.5:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.01:
            x= 1
        else:
            x= 0
    return x

def mail_round_land(x):
    if x>=1:
        if round((x-int(x)),2)>=0.5:
            x= int(x)+1
        else:
            x= int(x)
    if 0<x<1:
        if x> 0.4:
            x= 1
        else:
            x= 0
    return x









# 读取excel表
def read_excel(excel_path:str=None,
               sheet_name:str='sheet1',
               read_columns:str=None,
               skip_footer:int=0,
               fill_val=None):
    # 读表
    df=pd.read_excel(io=excel_path,
                sheetname=sheet_name,
                parse_cols=read_columns,
                skip_footer=skip_footer)
    # 填充NULL值
    if fill_val is not None:
        df = df.fillna(fill_val)
    return df


def generator_digit(n):
    for i in range(int('9' * n)):
        yield "{i:0>{n}}".format(i=i,n=n)  #i：输出，0：补全的字符，n:位数s