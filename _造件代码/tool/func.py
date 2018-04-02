# coding:utf-8
import pandas as pd
import numpy as np

# 空侧自定义四舍五入
def myround_air(num,sheet_name:str=None):
    x=None
    if sheet_name is None:
 
        x= round(num)
        return x
    # ==================
    if sheet_name=='Parcel pcs':
        if num>=1:
            if (num-int(num))>=0.970:
                x= int(num)+1
            else:
                x= int(num)
        if 0<num<1:
            if (num-int(num))> 0.010:
                x= 1
            else:
                x= 0
        return x

    # ==================
    if sheet_name == 'Small bag pcs':
        if num >= 1:
            if (num - int(num)) >= 0.60:
                x = int(num)+1
            else:
                x = int(num)
                
        if 0 < num < 1:
            if (num - int(num)) > 0.010:
                x = 1
            else:
                x = 0
        return x
    # ==================
    if sheet_name == 'Irregular pcs':
        if num >= 1:
            if (num - int(num)) >=0.98:
                x = int(num)+1
            else:
                x = int(num)
        if 0 < num < 1:
            if (num - int(num)) > 0.2:
                x = 1
            else:
                x = 0
        return x
    # ==================
    if sheet_name == 'NC pcs':
        if num >= 1:
            if (num - int(num)) >= 0.98:
                x = int(num)+1
            else:
                x = int(num)
        if 0 < num < 1:
            if (num - int(num)) > 0.2:
                x = 1
            else:
                x = 0
        return x
    # ==================
    if sheet_name == 'Mail pc':
        if num >= 1:
            if (num - int(num)) >= 0.5:
                x = int(num)+1
            else:
                x = int(num)
        if 0 < num < 1:
            if (num - int(num)) > 0.01:
                x = 1
            else:
                x = 0
        return x


# 陆侧自定义四舍五入
def myround_land(num,sheet_name:str=None):
    x=None
    if sheet_name is None:

        x= round(num)
        return x
    # ==================
    if sheet_name=='Parcel pcs':

        if num>=1:
            if (num-int(num))>=0.990:
                x= int(num)+1
            else:
                x= int(num)
        if 0<num<1:
            if (num-int(num))> 0.050:
                x= 1
            else:
                x= 0
        return x
    # ==================
    if sheet_name == 'Small bag pcs':
        if num >= 1:
            if (num - int(num)) >= 0.55:
                x = int(num)+1
            else:
                x = int(num)
        if 0 < num < 1:
            if (num - int(num)) > 0.3:
                x = 1
            else:
                x = 0
        return x
    # ==================
    if sheet_name == 'Irregular pcs':
        if num >= 1:
            if (num - int(num)) >= 0.99:
                x = int(num)+1
            else:
                x = int(num)
        if 0 < num < 1:
            if (num - int(num)) > 0.27:
                x = 1
            else:
                x = 0
        return x
    # ==================
    if sheet_name == 'NC pcs':
        if num >= 1:
            if (num - int(num)) >= 0.6:
                x = int(num)+1
            else:
                x = int(num)
        if 0 < num < 1:
            if (num - int(num)) > 0.08:
                x = 1
            else:
                x = 0
        return x
    # ==================
    if sheet_name == 'Mail pc':
        if num >= 1:
            if (num - int(num)) >= 0.5:
                x = int(num)+1
            else:
                x = int(num)
        if 0 < num < 1:
            if (num - int(num)) > 0.4:
                x = 1
            else:
                x = 0
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