# Bike-or-nei
This is the final project for a data science bootcamp at Le Wagon Berlin. 

The project is intended as a product for the maintenance team for Oslo City Bikes - a publicly funded bicycle service in Oslo, Norway. Based on a user's date choice, the product provides a prediction of the activity at all bicycle depots, i.e. parking and taking. Based on these predictions, the logistic department of Oslo City Bikes can optimise their daily bicycle distribution to maintain their availability at every depot.

The product is based on a Recurrent Neural Network deep learning model. The model was trained on time series data of bicycle usage (approx. 6 million trips) from April 2019 to October 2022, in addition to historical weather data from the same time period. From this data, we derived 24 features: each month of the year, each day of the week, and those pertaining to the daily climate of Oslo (e.g. min and max temperature, snow, rain, etc.). To ensure accurate predictions, the product requests a five-day weather forecast, which is processed according to the model’s training data, and subsequently feed to the model. 

Here is a screenshot of the product in action:

![alt text](https://storage.googleapis.com/sweet_bucket/Screenshot%202022-12-13%20at%2016.25.10.png)


As you can see, once the date has been chosen and the ‘make prediction’ button has been clicked, the product provides the user with an expandable ‘Details’ tab and a map of Oslo. The former shows a table with the name of each station, its coordinates, and the predicted daily flow of bicycles. The map, in turn, displays the bicycle depots as circles of different colours. The red circles are stations in need of replenishing (i.e. more bicycles are taken out than parked), whereas the blue circles represent stations from which bicycles should be taken from for redistribution (i.e. more bicycles are parked than taken out). The grey stations are subject to none of the above.

Given the short production period, the product is a work in progress. For completion, the product requires an automated daily prediction schedule, and will be expanded with a route calculator to further optimise Oslo City Bike’s logistics.

The product is available online via: https://sweetpatata-bike-or-nei-app-online-deployment-test-p7kup3.streamlit.app/
