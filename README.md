[![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio%20Code&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/siddusaikumar-git/CodingChallenge)

# Coding Challenge

This Repository is to generate backend API's of weather data and its statistics from Weather Data containing minimum temperature, maximum temperature and precipitation corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio from 1985-01-01 to 2014-12-31 with data stretching over 1.7 Million records, Hence the task is to query the Weather data and statistics corresponding to weather station and year.

# Pre-requisites

1. [Python v3.11](https://www.python.org/downloads/)
2. [PostgresSQL v15](https://www.postgresql.org/download/)

## Install Dependencies

```bash
    pip install -r requirements.txt
```

## Database creation in postgreSQL

create a datbase name "weather" and open the query tool to create the tables as below

## Create Tables

create tables "weatherdata" and "weatherstats" with the below queries.

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

# Execution

## Accessing APIs

Now once all the [pre-requisites](#Pre-requisites) installed, open in your favorite code editor and in the root folder, run the following command.

```bash
    python app.py
```

Now in the code you will see the app is running in development mode and able to listen to default localhost and port of Flask API [localhost link](http://localhost:5000/), you will see the link to access swagger API.
else goto link [Swagger API](http://localhost:5000/swagger)

## Unit Tests

To run unit tests, execute the following command

```bash
    python test.py
```

## Code Coverage

To run the code coverage and check the report, execute the following command

```bash
    coverage run test.py
```

```bash
    coverage report
```

```bash
    coverage html
```

Then a folder with name "htmlcov" is created, then open "index.html" to see the coverage.
