# Deploying a Machine Learning model in production on a server

## Understanding the business objective and problem

Given historical daily sales data for stores and products, we need to predict the total number of products sold at each store and item for the test set.

The [test-eda.ipynb](test-eda.ipynb) notebook shows the key insights from the training database, the necessary data processing, and the steps to take before creating a Flask API.

### Feature selection and regression model

Since the sales data follows a time series, we consider that an appropriate way to address the problem is by creating "lag features".

The regression model used was XGboost due to its high performance, both in terms of execution time and accuracy. In addition, a decision tree-based model is an interesting choice since we have a structured dataset and some categorical features.

### Validation and model persistence

We use validation on consecutive splits in time because we want to train past data to predict future data.

The persistence of the model was implemented using pickle. Both the model and the data for the additional features created were saved.

## Flask API and Docker 

To use the created model in a production environment, we implement a Flask API in the [api.py](api.py) script. 

We created the Flask API in the application directory. In this directory run the container using the command:

```
docker compose up --build
```

To make a request, you need to have access to another local terminal. As an example, to make a request we use the command:

```
curl -X POST -H "Content-Type: application/json" -d '{"shop_id": 55, "item_id": 10585}' http://0.0.0.0:5000/predict
```

In this example, the terminal should show:
```
{
  "item_id": "10585",
  "prediction": "1.0",
  "shop_id": "55"
}
```

The sales forecast is 1 unit for this product "10585" and store "shop_id" in November 2015.

## Access via a website

You can access the application in a web browser using [http://localhost:8081](http://localhost:8081) in your local machine.
In addition, we prepared a remote server in this [link](https://8007-177-12-9-119.ngrok-free.app).


### Complete project requirements:
  - flask 3.0.3
  - pandas 2.2.2
  - scikit-learn 1.4.2
  - numpy 1.26.4
  - seaborn 0.13.2
  - matplotlib 3.8.4
  - xgboost 2.1.0
