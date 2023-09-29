from flask import Flask, jsonify, request
from user import User

app = Flask(__name__)

# Declare and initialize a single user account (with placeholder id of 1)
user = User("1")

@app.route("/add", methods=["POST"])
def add():
    """
    Add a new transaction containing payer, points, timestamp data

    Request JSON:
    {
        "payer" : str,
        "points" : int,
        "timestamp" : str
    }

    Returns:
        Status code of 200 with no response body if the transaction was added successfully.
        Otherwise, status code of 400 with error message
    """
    try:
        transaction_data = request.get_json()
        payer = transaction_data["payer"]
        points = transaction_data["points"]
        timestamp = transaction_data["timestamp"]
        user.add_transaction(payer,points,timestamp)
        return '', 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/spend", methods=["POST"])
def spend():
    """
    Spend points

    Request JSON:
    {
        "points" : int
    }

    Returns:
        dict: a list of payer names and the number of points that were subtracted (if processing was successful)
        Otherwise, status code of 400 with error message
    """
    try:
        points_data = request.get_json()
        points = points_data["points"]

        # check if the user is trying to spend more points than balance
        if points > user.get_balance():
            return jsonify({'error': 'User does not have enough points.'}), 400

        return jsonify(user.spend(points)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/balance", methods=["GET"])
def get():
    """
    Retrieve the total number of points the user has in their account with points per payer

    Returns:
        dict: a map of points the user has in their account based on the payer they were added through
    """
    return jsonify(user.get_points_balance()), 200

if __name__ == "__main__":
    app.run(debug=True,port=8000)