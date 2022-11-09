
# Currency Viewer

This application graphs a series of exchange rate of the BRL, EUR and JPY currencies based on dollar and stores it in a database for future requests.

Everything is developed on Django and it uses a highcharts graph to visualize the rates.

The source data is collected from:
```
https://www.vatcomply.com/documentation 
```

When a date range is requested to API, the data is stored in the database.

This application has 100% tests coverage.

It also has an API endpoint callable by:
```
 /api/v1/
```

## How to run