# Task 
This project implements an automated Spotify bot that can create accounts, search for songs, and add them to playlists using Selenium WebDriver.

## Index:

- [Manual Testing](#manual-testing)
- [Automation testing](#automation-testing)
    - [Installation](#installation)
    - [Usage](#usage)
- [Databases](#databases)
- [Performance Testing](#performance-testing)


# Manual Testing 
A comprehensive set of test cases has been documented and can be found in this [Google Sheet](https://docs.google.com/spreadsheets/d/1X8QXgY4T5NFVV59R50O2KzHoXRJv_4D5kBmYU5Dk4M0/edit?usp=sharing).


# Automation testing 
The automation testing suite is implemented in the `main.py` file. It uses Selenium WebDriver to automate browser interactions with the Spotify web interface.

## Installation

> Before running the tests, ensure you have:
- Python 3.7 or higher installed on your system

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

## Usage

To run the tests, use the following command:

```bash
python main.py -b <browser> -s <song>
```

- `browser`: `firefox`, `edge`, `chrome`
- `song`: `song name`

### Example

```bash
python main.py -b chrome -s "Hello Adele"
```

## Screenshots

### Logs

![Logs](./automation-task/screenshots/example-logs.png).


## Recordings

![recording](./automation-task/recording/Spotify.mp4).



# Databases

You can find the query in the [sql file](./database-task/sql_queries.sql).

> Note: I named the first table as `customers` and the second table as `salesmen`.

```sql
SELECT c.cust_name, c.city AS customer_city, s.name AS salesman, s.city AS salesman_city, s.commission
FROM customers c
JOIN salesmen s ON c.salesman_id = s.salesman_id
WHERE c.city != s.city AND s.commission > 0.12;
```

# Performance Testing

Performance testing was done using `JMeter`.

You can find the report in the `performance-test` folder.

## Screenshots

### Results

![Results](./performance-testing/screenshots/results.png).

### Summary

![Summary](./performance-testing/screenshots/summary.png).



