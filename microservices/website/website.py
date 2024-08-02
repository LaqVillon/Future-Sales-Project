import pickle
import pandas as pd
from os import getenv
from sqlalchemy import create_engine, text
from flask import Flask, request, jsonify, render_template


# Flask app
app = Flask(__name__)

# Loading the trained model
with open('models/model.pkl', 'rb') as file:
    model = pickle.load(file)

# Connecting to the database
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")
connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)


def get_features(engine, shop_id, product_id):
    with engine.connect() as con:
        result = con.execute(text("""
        SELECT * FROM features_dataset
        WHERE shop_id = :shop_id AND item_id = :item_id
        """), {'shop_id': shop_id, 'item_id': product_id})
        features = pd.DataFrame(result.fetchall())
    return features
    # In future, we can use the following line to return just the necessary columns
    # return features.drop(['shop_id', 'item_id', ''], axis=1, inplace=True)


@app.route('/')
def home():
    """
    Home page
    """
    return render_template("index.html")


@app.route("/predict", methods = ["POST"])
def predict():
    """
    Predict the sales for a given shop_id and item_id
    """
    try:
        
        # Getting the input values from the request
        input_ids = [x for x in request.form.values()]
        if any(not x.replace('.', '', 1).isdigit() for x in input_ids):
            raise KeyError('Shop ID and Item ID are integer values')
        shop_id = int(input_ids[0])
        item_id = int(input_ids[1])

        # Checking if required keys are in the request
        if not (0 <= shop_id <= 59) or not (0 <= item_id <= 22169):
            raise ValueError('Values out of range')

        # Filtering the test data for the given shop_id and item_id
        features = get_features(engine, shop_id, item_id)
        if features.empty:
            raise LookupError('There is no data to provide a prediction')
        
        # Perform the prediction
        prediction = model.predict(features)
        prediction_rounded = round(prediction[0], 0)
        return render_template("index.html", prediction_text = "The prediction is {}".format(prediction_rounded))

    except KeyError as e:
        return render_template("index.html", prediction_text = str(e)), 400

    except ValueError as e:
        return render_template("index.html", prediction_text = str(e)), 400

    except LookupError as e:
        return render_template("index.html", prediction_text = str(e)), 404

    except Exception as e:
        return render_template("index.html", prediction_text = 'An unexpected error occurred: ' + str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    