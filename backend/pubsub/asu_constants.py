#!/usr/bin/env python
SUBSCRIPTION_UNIQUE_TOKEN = 'test123'
TABLE_NAME = 'ninth-tensor-233119.cc_dataset.sensor_data'
QUERY_HOURLY = """
SELECT controller_id,TIMESTAMP (CONCAT(CAST(DATE as STRING)," ",CAST(EXTRACT(hour from t1) as string),":00:00")) as hour_number, Avg(temperature) as Average_temp,Avg(ph) as Average_ph,Avg(ec) as Average_ec
from (select controller_id,DATE(timestamp, "America/Phoenix") as DATE,DATETIME(timestamp, "America/Phoenix") as t1,temperature,ph,ec
FROM `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}'
)GROUP BY hour_number, controller_id, DATE
order by DATE desc , hour_number desc limit 24
"""
QUERY_DAILY="""
SELECT controller_id,TIMESTAMP (CONCAT(CAST(DATE as STRING)," ","00:00:00")) as hour_number, Avg(temperature) as Average_temp,Avg(ph) as Average_ph,Avg(ec) as Average_ec
from (select controller_id,DATE(timestamp, "America/Phoenix") as DATE,DATETIME(timestamp, "America/Phoenix") as t1,temperature,ph,ec
FROM `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}'
)GROUP BY hour_number, controller_id, DATE
order by DATE desc , hour_number desc limit 7
"""
QUERY_WEEKLY="""
SELECT controller_id,TIMESTAMP (CONCAT(CAST(DATE as STRING)," ","00:00:00")) as hour_number, Avg(temperature) as Average_temp,Avg(ph) as Average_ph,Avg(ec) as Average_ec
from (select controller_id,DATE(timestamp, "America/Phoenix") as DATE,DATETIME(timestamp, "America/Phoenix") as t1,temperature,ph,ec
FROM `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}'
)GROUP BY hour_number, controller_id, DATE
order by DATE desc , hour_number desc limit 7
"""
QUERY_EIGHT_WEEKLY="""
Select 
controller_id,
DATE_SUB(DATE(TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), WEEK, "America/Phoenix")), INTERVAL WeekNumber WEEK) Week,
Avg(ph) as average_ph,
Avg(ec) as average_ec,
Avg(temperature) as average_temp
from
(
    SELECT 
    controller_id,
    DATE_DIFF(DATE(timestamp, "America/Phoenix"), DATE(TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), WEEK, "America/Phoenix")), week) AS WeekNumber,
    ph,
    ec,
    temperature
    FROM `ninth-tensor-233119.cc_dataset.sensor_data`
    where controller_id='{}'
)
GROUP BY
controller_id,
WeekNumber
order by WeekNumber desc
limit 8
"""
QUERY_AVG="""
SELECT 'Ph' as column, AVG(ph) average_val
from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix")
UNION ALL
SELECT 'EC' as column, AVG(ec) average_val
from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix")
UNION ALL
SELECT 'Temperature' as column, AVG(temperature) average_val
from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix")
"""
QUERY_MAX="""
(SELECT distinct 'Temperature' as Column, DATETIME(timestamp, "America/Phoenix") as DATE, min_temp as Max_Value
from(
SELECT MAX(temperature) min_temp
from `ninth-tensor-233119.cc_dataset.sensor_data`  where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix") ) t1 inner join (SELECT * from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}') t2 on t1.min_temp=t2.temperature)
UNION ALL
(SELECT distinct 'EC' as Column, DATETIME(timestamp, "America/Phoenix") as DATE, min_ec as Min_Value
from(
SELECT MAX(ec) min_ec
from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix")) t1 inner join (SELECT * from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}') t2 on t1.min_ec=t2.ec)
UNION ALL
(SELECT distinct 'Ph' as Column, DATETIME(timestamp, "America/Phoenix") as DATE, min_ph as Min_Value
from(
SELECT MAX(ph) min_ph
from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix")) t1 inner join (SELECT * from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}') t2 on t1.min_ph=t2.ph)
"""
QUERY_MIN="""
(SELECT distinct 'Temperature' as Column, DATETIME(timestamp, "America/Phoenix") as DATE, min_temp as Min_Value
from(
SELECT MIN(temperature) min_temp
from `ninth-tensor-233119.cc_dataset.sensor_data`  where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix") ) t1 inner join (SELECT * from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}') t2 on t1.min_temp=t2.temperature)
UNION ALL
(SELECT distinct 'EC' as Column, DATETIME(timestamp, "America/Phoenix") as DATE, min_ec as Min_Value
from(
SELECT MIN(ec) min_ec
from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix")) t1 inner join (SELECT * from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}') t2 on t1.min_ec=t2.ec)
UNION ALL
(SELECT distinct 'Ph' as Column, DATETIME(timestamp, "America/Phoenix") as DATE, min_ph as Min_Value
from(
SELECT MIN(ph) min_ph
from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}' and DATETIME(timestamp, "America/Phoenix") BETWEEN DATETIME('{}', "America/Phoenix") AND DATETIME('{}', "America/Phoenix")) t1 inner join (SELECT * from `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}') t2 on t1.min_ph=t2.ph)
"""
QUERY="""
SELECT DATETIME(timestamp,"America/Phoenix"),COntroller_id,ph,ec,temperature
FROM `ninth-tensor-233119.cc_dataset.sensor_data`
WHERE controller_id='{}' AND DATETIME(timestamp,"America/Phoenix") BETWEEN DATETIME('{}',"America/Phoenix") AND DATETIME('{}',"America/Phoenix")
ORDER BY DATETIME(timestamp,"America/Phoenix") asc
"""