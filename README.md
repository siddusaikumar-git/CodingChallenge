# coding challenge

```sql
DROP TABLE weatherdata;

CREATE TABLE weatherdata (
    id VARCHAR(50) PRIMARY KEY,
    stationid VARCHAR(10) NOT NULL,
    date VARCHAR(10) NOT NULL,
    year INTEGER NOT NULL,
    maxtemp INTEGER,
    mintemp INTEGER,
    precipitation INTEGER
    )
```
