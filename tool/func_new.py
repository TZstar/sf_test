# coding:utf-8
import pandas as pd
import numpy as np
import random


def round_func(x, ceil_val, floor_val):
    '''
    邮件精度控制函数：
    输入：
       x - 待精度处理的值
       ceil_val - 精度处理进1的定义值
       floor_val - 精度处理置0的定义值
    输出：
       x - 精度处理后的值
    '''
    if x >= 1:
        if round((x - int(x)), 2) >= ceil_val:
            x = int(x) + 1
        else:
            x = int(x)
    if 0 < x < 1:
        if x > floor_val:
            x = 1
        else:
            x = 0
    return x


def parcel_data_convert(od_path, sheet_name, parse_cols, parse_skip_num,
                cols_split, air_model_list, land_model_list, parcel_type,
                air_round_ceil, air_round_floor, land_round_ceil, land_round_floor,
                db_columns_modify, parcel_col_list,pkg_n=1):
    '''读取od表数据，进行数据预处理'''
    # 读取数据
    df_parcel = read_excel(excel_path=od_path,
                  sheet_name=sheet_name,
                  read_columns=parse_cols,
                  fill_val=0,
                  skip_footer=parse_skip_num)

    # 取列名，替换空格
    col_list = list(df_parcel.columns.str.replace(' ', '_'))

    # 重置列名
    df_parcel.columns = col_list

    # 横行变纵行
    df_parcel = pd.melt(df_parcel,
                id_vars=col_list[:cols_split],
                value_vars=col_list[cols_split:],
                var_name='desc_city_api_model',
                value_name='parcel_sum')
    
    # 重新读取desc_city_api_model列，生成DataFrame对象
    a = df_parcel['desc_city_api_model'].str.split('_')
    df_dest = pd.DataFrame(list(np.array(a)), columns=['dest_city', 'api', 'desc_model'])

    # 将目的地的city,api，model的df对象与df_parcel合并,并删除desc_city_api_model列
    df_parcel = pd.concat([df_parcel, df_dest], axis=1).drop('desc_city_api_model', axis='columns')

    # 造parcel_type列
    df_parcel['parcel_type'] = parcel_type
    
    # small_bag 和 isb 需要 parcel_sum 进行打包处理
    df_parcel['parcel_sum'] = df_parcel['parcel_sum'].apply(lambda x:x*pkg_n)

    # 空侧数据精度控制
    df_parcel_air = df_parcel.loc[df_parcel.model.isin(air_model_list), :].copy()
    df_parcel_air_parcel_sum = df_parcel_air.parcel_sum
    df_parcel_air_parcel_sum = df_parcel_air_parcel_sum.apply(lambda x: round_func(x, air_round_ceil,air_round_floor))
    df_parcel_air.loc[:,'parcel_sum'] = df_parcel_air_parcel_sum
    # 陆侧数据精度控制
    df_parcel_land = df_parcel.loc[df_parcel.model.isin(land_model_list), :].copy()
    df_parcel_land_parcel_sum = df_parcel_land.parcel_sum.apply(lambda x: round_func(x,land_round_ceil,land_round_floor))
    df_parcel_land.loc[:,'parcel_sum'] = df_parcel_land_parcel_sum
    # 合并数据
    df_parcel_total = pd.concat([df_parcel_air, df_parcel_land])
    print(df_parcel_total.shape)
    # parcel_sum 置空值列为0
    series_sum = df_parcel_total['parcel_sum'].fillna(0)

    # 打印统计处理数据之前的包裹数量
    print('处理之前，邮件总数量为：%s' % (series_sum.sum()))
    print('处理之前，包裹总数量为：%s' % (series_sum.count()))
    
    # 去除 parcel_sum 的空值行，根据 parcel_sum 值造表
    df_parcel_total = df_parcel_total.loc[df_parcel_total['parcel_sum'] != 0, :]
    # 取出 parcel_sum 的 columns/parcel_sum_list
    parcel_column_list = list(df_parcel_total.columns)
    parcel_sum_list = list(df_parcel_total['parcel_sum'].values)
    # 造新的 parcel_total_list_new
    parcel_total_list = list(np.array(df_parcel_total))
    parcel_total_list_new = []
    for i,parcel in enumerate(parcel_total_list):
        new = [parcel for i in range(int(parcel_sum_list[i]))]
        parcel_total_list_new += new
    # 转换为 df    
    df_parcel_total = pd.DataFrame(parcel_total_list_new,columns=parcel_column_list)

    # 修改列名（按照数据库）
    df_parcel_total.rename(columns=db_columns_modify, inplace=True)

    # 按数据库字段，重构columns字段
    df_parcel_total = df_parcel_total.reindex(columns=parcel_col_list)

    # 格式化时间 [2045-02-08 00:33:22], 秒数取整，增加日期
    df_parcel_total_arrive_time = df_parcel_total.loc[:,'arrive_time'].copy()
    df_parcel_total_arrive_time = df_parcel_total_arrive_time.apply(lambda x: x.strftime('%H:%M:%S'))
    df_parcel_total_arrive_time = df_parcel_total_arrive_time.apply(lambda x:"2045-02-07 "+x if int(x[0:2])>12 else "2045-02-08 "+x)
    df_parcel_total['arrive_time'] = df_parcel_total_arrive_time

    # 打印统计处理数据之前的包裹数量
    print('处理之后，包裹总数量为：%s' % df_parcel_total.shape[0])

    return df_parcel_total


def read_excel(excel_path: str = None,
           sheet_name: str = 'sheet1',
           read_columns: str = None,
           skip_footer: int = 0,
           fill_val=None):
    ''' 读取excel表 '''
    
    # 读表
    df = pd.read_excel(io=excel_path,
               sheet_name=sheet_name,
               usecols=read_columns,
               skip_footer=skip_footer)
    # 填充NULL值
    if fill_val is not None:
        df = df.fillna(fill_val)
    return df


def generator_digit(n):
    ''' 生成占位长度为n的数字，不足补0 '''
    for i in range(int('9' * n)):
        yield "{i:0>{n}}".format(i=i, n=n)  # i：输出，0：补全的字符，n:位数s
        