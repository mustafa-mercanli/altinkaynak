* When you call **get_try_currencies()** and **get_rate()** functions, they return currency date as string (eg; 2022-00-00T00:00:00.000Z), not timezone aware datetime object. It is because of the python version compatibility issues.