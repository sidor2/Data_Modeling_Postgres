# Project: Data Modeling with Postgres

## Purpose
The purpose of the project is to create a Postgres database, and an ETL pipeline.

## Background
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, the data resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

* * *

## Prerequisites for running locally
- Python 3.8
	- virtualenv, or
	- conda
- PostgresSQL database
	- localhost, or target IP
	- username and password
- Jupyter
- Pandas
- psycopg2:

	install using **pip**:
	```sh 
	(venv)$ pip install psycopg2-binary
	```
	
	install using **conda**:
	```sh
	(base)$ conda install -c anaconda psycopg2
	```

* * *

## Running locally

Connect to PostgreSQL and create the database:
```sh
$ ./create_tables.py
```

Run the ETL:
```sh
$ ./etl.py
```

Verify completion:
```
test.ipynb	# run with Jupyter
```

* * *

## Project structure

```
.
├── data
│   ├── log_data
│   │   └── ...
│   └── song_data
│       └── ...
├── sql_queries.py
├── create_tables.py
├── etl.py
├── etl.ipynb
├── README.md
└── test.ipynb

```

#### Project files

`sql_queries.py`	- Contains queries to create and drop tables. Insert data into the tables. Select query from "songplays" table.
`create_tables.py`	- Creates tables in the database.
`etl.py`			- Executes the ETL pipeline process.
`etl.ipynb`			- Used to develop the ETL process.
`README.md`			- "self"
`test.ipynb`		- Used for testing the database functionality.

#### Example output from "Songplays" table

```
 SELECT * FROM songplays LIMIT 5;
```

| songplay_id |	start_time | user_id| level | song_id |	artist_id |	session_id | location |	user_agent |
|-------------|------------|--------|-------|---------|-----------|------------|----------|------------|
|1|	2018-11-30 00:22:07.796000|	91|	free|	None|	None|	829	| Dallas-Fort Worth-Arlington, TX	|Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)|
|2|	2018-11-30 01:08:41.796000|	73|	paid|	None|	None|	1049|	Tampa-St. Petersburg-Clearwater, FL|	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"|
|3|	2018-11-30 01:12:48.796000|	73|	paid|	None|	None|	1049|	Tampa-St. Petersburg-Clearwater, FL|	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"|
|4|	2018-11-30 01:17:05.796000|	73|	paid|	None|	None|	1049|	Tampa-St. Petersburg-Clearwater, FL|	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"|
|5|	2018-11-30 01:20:56.796000|	73|	paid|	None|	None|	1049|	Tampa-St. Petersburg-Clearwater, FL|	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"|

