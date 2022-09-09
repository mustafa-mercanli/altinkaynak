# Altinkaynak

This package is used for fetching altinkaynak.com rates based on TRY currency.
To use it, simpy do that;
```
from altinkaynak import Altinkaynak
altin = Altinkaynak()

#Get all rates based on TRY currrency
altin.get_try_currencies()

#Or how much unit EUR cost equal to 1 unit USD 
altin.get_rate("USD","EUR")

#Or other provided rates
altin.get_rate("AFG","TRY")
```


# Changelog
* When you call **get_try_currencies()** and **get_rate()** functions, they return currency date as string (eg; 2022-00-00T00:00:00.000Z), not timezone aware datetime object. It is because of the python version compatibility issues.