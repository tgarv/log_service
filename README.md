# LogRocket Log Service
This is a quick demo of a service to store log information and query that information for a given time period.

## How to Run
This project is built using Flask, a lightweight Python web server framework. To run:
1. Install Virtualenv (optional, but recommended):
    - `$ pip install virtualenv`
2. Create a new virtualenv:
    - `$ virtualenv venv`
3. Start virtualenv:
    - `$ source venv/bin/activate`
4. Clone this repo and `cd` into it
5. Install requirements:
    - `$ pip install -r requirements.txt`
6. Start the app:
    - `$ python flask_app/app.py`

## Notes
This project uses [Interval Trees](https://en.wikipedia.org/wiki/Interval_tree) to efficiently query logs over a given time range. This gives an `O(log(n) + m)` query time, where `n` is the total number of intervals stored and `m` is the number of results returned by the range query.

Next steps for this project would involve persisting the data to a database and implementing a caching layer to reuse previous queries.