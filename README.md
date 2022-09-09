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