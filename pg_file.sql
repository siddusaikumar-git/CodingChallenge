/* weatherdata table */

-- DROP TABLE weatherdata;

-- CREATE TABLE weatherdata (
--     stationid VARCHAR(20) NOT NULL,
--     date DATE NOT NULL,
--     year INTEGER NOT NULL,
--     maxtemp INTEGER,
--     mintemp INTEGER,
--     precipitation INTEGER
--     );

/* weatherstats table */

DROP TABLE weatherstats;

CREATE TABLE weatherstats (
    stationid VARCHAR(20) NOT NULL,
    year INTEGER NOT NULL,
    avgmaxtemp REAL,
    avgmintemp REAL,
    totalprecipitation REAL
    );

INSERT INTO weatherstats (stationid, year, avgmaxtemp, avgmintemp, totalprecipitation) 
SELECT 'USC00114442', 2000, 17.66, 4.86, 92
WHERE NOT EXISTS ( 
	SELECT stationid FROM weatherstats WHERE stationid = 'USC00114442' and year = 2000 and avgmaxtemp = 17.66 and avgmintemp = 4.86 and totalprecipitation = 92);


select * from weatherstats;

-- select * from weatherdata;

-- select count(*) from weatherdata;

/* query with respect to year */
-- select row_to_json(t) as output from (select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as precipitation, year, stationid  from weatherdata where year = 1985 group by stationid, year) t;

/* query with respect to station id */
-- select row_to_json(o) as output from (select (select count(*) OVER() from weatherdata where stationid = 'USC00111436' group by stationid, year order by year, stationid limit 1) as total_count, json_agg(to_json(t)) as results from (select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as total_precipitation, year, stationid  from weatherdata where year = 1985 group by stationid, year order by year, stationid limit 10 offset 10) as t) as o;

-- select row_to_json(o) as output from (select (select count(*) OVER() from weatherdata where stationid = 'USC00111436' group by stationid, year order by year, stationid limit 1) as total_count, json_agg(to_json(t)) as results from (select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as total_precipitation, year, stationid  from weatherdata where year = 1985 group by stationid, year order by year, stationid limit 10 offset 10) as t) as o;

-- select row_to_json(o) as output from (select (select count(*) from weatherdata where year = 1985) as total_count, json_agg(to_json(t)) as results from (select ROUND(maxtemp/10, 2) as maxtemp, ROUND(mintemp/10, 2) as mintemp, ROUND(precipitation/100, 2) as precipitation, date, year, stationid  from weatherdata where year = 1985 order by year, stationid limit 10 offset 0) as t) as o;


-- select * from weatherdata;
