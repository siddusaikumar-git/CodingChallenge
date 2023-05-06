
-- DROP TABLE weatherdata;

-- CREATE TABLE weatherdata (
--     id VARCHAR(50) PRIMARY KEY,
--     stationid VARCHAR(20) NOT NULL,
--     date VARCHAR(10) NOT NULL,
--     year INTEGER NOT NULL,
--     maxtemp INTEGER,
--     mintemp INTEGER,
--     precipitation INTEGER
--     );

-- select * from weatherdata;

-- select count(*) from weatherdata;

/* query with respect to year */
-- select row_to_json(t) as output from (select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as precipitation, year, stationid  from weatherdata where year = 1985 group by stationid, year) t;

/* query with respect to station id */
select row_to_json(t) as output from (select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as precipitation, year, stationid  from weatherdata where stationid = 'USC00110187' group by stationid, year limit 10 offset 0) t;

/* query with respect to year and station id */
-- select row_to_json(t) as output from (select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as precipitation, year, stationid  from weatherdata where stationid = 'USC00110187' and year = 1985 group by stationid, year limit 10 offset 0) t;

