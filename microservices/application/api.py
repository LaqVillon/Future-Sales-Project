import pickle
import pandas as pd
from os import getenv
from sqlalchemy import create_engine, text
from flask import Flask, request, jsonify, render_template


# Flask app
flask_app = Flask(__name__)

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


@flask_app.route("/predict", methods=["POST"])
def predict():
    """
    Predict the sales for a given shop_id and item_id
    """
    try:
        # Checking if required keys are in the request
        if 'shop_id' not in request.json or 'item_id' not in request.json:
            raise KeyError('shop_id and item_id are required')

        # Getting and validating shop_id and item_id
        shop_id = int(request.json['shop_id'])
        item_id = int(request.json['item_id'])
        if not (0 <= shop_id <= 59) or not (0 <= item_id <= 22169):
            raise ValueError('Value out of range')

        # Filtering the test data for the given shop_id and item_id
        features = get_features(engine, shop_id, item_id)
        if features.empty:
            raise LookupError('There is no data to provide a prediction')
        # Perform the prediction
        prediction = model.predict(features)
        prediction_rounded = round(prediction[0], 0)
        
        # Prepare the response
        result = {
            'prediction': str(prediction_rounded),
            'shop_id': str(shop_id),
            'item_id': str(item_id),
        }
        return jsonify(result)

    except KeyError as e:
        return jsonify({'error': str(e)}), 400

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    except LookupError as e:
        return jsonify({'error': str(e)}), 404

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500


if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', debug=True)
