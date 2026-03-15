from flask import Flask, render_template, request, jsonify
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


# Create the Flask application instance
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Define a route (homepage)
@app.route("/", methods=['GET'])
def home():
    state = request.args.get('material')
    if(state == "test"):
        return render_template("home-guide.html")
    if(state == "silicone"):
        return render_template("silicone.html")
    elif(state == "rubber"):
        return render_template("rubber.html")
    elif(state == "resin"):
        return render_template("resin.html")
    else:
        return render_template("no_material.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/process")
def process():
    return render_template("process.html")

@app.route("/all_data")
def all_data():
    database = pd.read_csv('data.csv')
    rows = database.to_dict(orient='records')
    headers = database.columns.tolist()
    return render_template('all_data.html', headers=headers, rows=rows)

@app.route("/compare")
def compare():
    database = pd.read_csv('data.csv')
    silicone_types = database['Silicone_Type'].unique().tolist()
    print_materials = database['3D_Print_Material'].unique().tolist()
    return render_template('compare.html',
                           silicone_types=silicone_types,
                           print_materials=print_materials)

@app.route("/api/filter")
def api_filter():
    silicone_type = request.args.get('silicone_type', '')
    print_material = request.args.get('print_material', '')

    database = pd.read_csv('data.csv')
    database.columns = database.columns.str.strip()

    if silicone_type:
        database = database[database['Silicone_Type'] == silicone_type]
    if print_material:
        database = database[database['3D_Print_Material'] == print_material]

    return jsonify(database.to_dict(orient='records'))


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
    