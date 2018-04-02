# 查询总数据量  ## 965426
SELECT COUNT(*)
FROM `i_od_parcel_2025v31_plus_mix`;

# 查询 smll 的数量  ## 474697
SELECT COUNT(*)
FROM `i_od_parcel_2025v31_plus_mix`
WHERE parcel_type = 'small';

# 查询 parcel 的数量  ## 418937
SELECT COUNT(*)
FROM `i_od_parcel_2025v31_plus_mix`
WHERE parcel_type = 'parcel';

# 查询 irregular 的数量  ## 21752
SELECT COUNT(*)
FROM `i_od_parcel_2025v31_plus_mix`
WHERE parcel_type = 'irregular';

# 查询 nc 的数量  ## 421
SELECT COUNT(*)
FROM `i_od_parcel_2025v31_plus_mix`
WHERE parcel_type = 'nc';


# 查询 isb 的数量  ## 49619
SELECT COUNT(*)
FROM `i_od_parcel_2025v31_plus_mix`
WHERE parcel_type = 'isb';
