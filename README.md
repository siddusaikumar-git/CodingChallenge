# coding challenge

This Repository is to generate backend API's of weather data and its statistics from Weather Data containing minimum temperature, maximum temperature and precipitation corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio from 1985-01-01 to 2014-12-31 with data stretching over 1.7 Million records, Hence the task is to query the Weather data and statistics corresponding to weather station and year.

## Pre-requisites

1. [Python v3.11](https://www.python.org/downloads/)
2. [PostgresSQL v15](https://www.postgresql.org/download/)

```sql
/* weatherdata table */

DROP TABLE weatherdata;

CREATE TABLE weatherdata (
    stationid VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    year INTEGER NOT NULL,
    maxtemp INTEGER,
    mintemp INTEGER,
    precipitation INTEGER
    );

/* weatherstats table */

DROP TABLE weatherstats;

CREATE TABLE weatherstats (
    stationid VARCHAR(20) NOT NULL,
    year INTEGER NOT NULL,
    avgmaxtemp REAL,
    avgmintemp REAL,
    totalprecipitation REAL
    );
```
