 # 造件策略说明
---
**说明：**
1. 2025版与2045版造件代码为同一套；
2. 逻辑为混包版本	
---

## 1 输入与输出条件

### 1.1 输入条件

1. 2025-OD 矩阵表：2025OD_v31.xlsx
2. 2045-OD 矩阵表：2045OD_Matrix.xlsx
3. ULD-航班 对照表：0103ULD_id.xlsx

#### 1.1.1 【表】2025OD_v31.xlsx | 2045OD_Matrix.xlsx 类同
|序号|表名 <br> Sheet Name|说明 <br> Contents|
|:--|:---|:---|
|1|Parcel pcs|每个到达航班中去往不同目的地的包裹数量 
|2|Smalls bag pcs|每个到达航班中去往不同目的地的小件包数量 |
|3|Irregular pcs|每个到达航班中去往不同目的地的不规则件数量 |
|4|NC pcs|每个到达航班中去往不同目的地的不可上线件数量|
|5|Mail bag pcs|每个到达航班中去往不同目的地的小件包数量|
|6|sorting by pcs|每个到达航班中去往不同目的地且需要分拣的总件量，即表1+2+3+4+5 |
|7|crossdock by pcs|每个到达航班中去往不同目的地且不需要分拣直接转箱的件量  |
|8|sum pcs|每个到达航班中去往不同目的地的总件量，即表6+7 |
|9|Departure Flight rule|每个出发航班中装载ULD的数量，以及每个ULD中装载的件量  |
|10|Departure Road rule|每个出发卡车中装载的件量 |

#### 1.1.2【表】0103ULD_id.xlsx
| 序号 | 字段名 | 描述 | 
| -:- | :---- | :---- | 
| 1 | ULD_id | 国际(顺丰自有飞机) | 
| 2 | flight_id | 国内 |
| 3 | property | z |  

### 1.2 输出结果：

| 序号 | 字段名 | 描述 | 类型 | 来源 |
| -:- | :---- | :------ | :---- | :---- |
| 1 |'small_id'| 票号 | varchar(10)  primary key | 【造】 |
| 2 |'parcel_id'| 包裹号 | varchar(10)  primary key | 【造】 |
| 3 |'parcel_type'| 包裹类型 | varchar(10) | pcs表名 |
| 4 |'src_type'| 始发地类型 | char(5) | 表[parcel pcs].model |
| 5 |'src_apt'| 始发地机场？ | varchar(10) | 表[parcel pcs].apt |
| 6 |'dest_type'| 到达地类型 | varchar(10) | 表[parcel pcs].wide_date.dest_model |
| 7 |'dest_apt'| 到达地机场 | varchar(10) | 表[parcel pcs].wide_date.api |
| 8 |'dest_city_code'| 到达城市编号 | varchar(10) | 表[parcel pcs].wide_date.city |
| 9 |'plate_num'| 运输工具编号 | varchar(20) | 表[parcel pcs].Flight_ID |
| 10 |'uld_num' | 航空箱编号 | varchar(20) | 【造】 |
| 11 |'arrive_time'| 到达时间 | datetime | 表[parcel pcs].landingtime |
| 12 |'send_time'| 发送时间 | datetime | # |
| 13 |'plan_disallow_tm'| ？ | # | # |
| 14 |'actual_disallow_tm'| ？ | # | # |
| 15 |'ident_des_zno'| ？ | # | # |
| 16 |'plate_priority'| ？ | # | # |
| 17 |'is_mixture'| 是否混包 | # |【造】|
| 18 |'inserted_on'| 插入时间 | datetimes | 自动生成 |
| 19 |'modified_on'| 修改时间 | datetime | 自动生成 |

#### 1.2.1 分配原则：
	
|类目|取数规则|数据源|
|:---|:---|:---|
|small<br>parcel<br>nc<br>irregular<br>mail|flight_id 行数据|Parcel pcs 表单<br>small pcs 表单<br>NC pcs 表单<br>Irregular pcs 表单<br>mail pcs 表单|
|ULD|每个航班ID对应的MHS ULD 列数据|sorting by pcs 表单|
|parcel类|small小件包，= 数量范围(16,26)，均值为20；<br> mail小件包，=数量范(90,110)，均值为100； |Small bag pcs 表单|


**注意：**
1. 到达地相同的包裹数量 = (18,28)，打包为非混包；剩余打包为混包；
2. 每 **卡车**、**飞机** 分配的包裹数量已经分配好，不会超载；
	- 空载：随机平均分配给每个ULD即可；再随机平均分配给parcel即可；
	- 陆载：随机平均分配给parcel即可；
	- 国际包同空载。

#### 1.2.2 src_type类型
| 序号 | 字段名 | 描述 | 
| -:- | :---- | :---- | 
| 1 | I | 国际(顺丰自有飞机) | 
| 2 | D | 国内 |
| 3 | INF | 国际 | 
| 4 | R | 陆侧 | 

#### 1.2.3 parcel_type类型

|序号| 分拣区域 | 类型名<br>(表格)|类型名<br>(数据库)| 描述 |
| :---- | :---- | :---- | :---- |:---- |
|1| Air/land | parcel | **small** |小件类 |
|2| Air/land | small | **parcel** |包裹类 |
|3| Air/land | irregular |irregular | 不规则件类 |
|4| Air/land | nc | nc |不能跟踪信息件类 |
|5| Air/land | mail |**isb** | 国际小件类 |

**注意：**表格中的字段和数据库中的字段不一致。

## 2 造数据

### 2.1 Parcel pcs表格处理

1. pd.melt横行变纵行
2. 包裹的精度转换
3. 拆分 desc_city_api_model 列
2. 去除 parcel_sum 的零值行
3. columns列名更改
4. arrive_time 的格式化

### 2.2 造small_id / uld_num / parcel_id

### 2.3 non_mix 非混包

### 2.4 is_mixture 判断是否混包


## 3 随机取件_1%_10%

抽样比例为1% 和 10%



