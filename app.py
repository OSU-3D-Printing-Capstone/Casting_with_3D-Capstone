from flask import Flask, render_template, request, jsonify, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    silicone_type = db.Column(db.String(100))
    print_material = db.Column(db.String(100))
    workability = db.Column(db.Integer)
    fine_detail = db.Column(db.Integer)
    mechanical_strength = db.Column(db.Integer)
    mold_reusability = db.Column(db.Integer)
    notes = db.Column(db.String(500))


@app.route("/", methods=['GET'])
def home():
    state = request.args.get('material')
    if state == "test":
        return render_template("home-guide.html")
    if state == "silicone":
        return render_template("silicone.html")
    elif state == "rubber":
        return render_template("rubber.html")
    elif state == "resin":
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
    rows = Material.query.all()
    data = [{
        'Silicone_Type': r.silicone_type,
        '3D_Print_Material': r.print_material,
        'Workability(1-5)': r.workability,
        'Fine Detail & Accuracy(1-5)': r.fine_detail,
        'Mechanical Strength(1-5)': r.mechanical_strength,
        'Mold Reusability(1-5)': r.mold_reusability,
        'Notes': r.notes
    } for r in rows]
    headers = ['Silicone_Type', '3D_Print_Material', 'Workability(1-5)',
               'Fine Detail & Accuracy(1-5)', 'Mechanical Strength(1-5)',
               'Mold Reusability(1-5)', 'Notes']
    return render_template('all_data.html', headers=headers, rows=data)


@app.route("/compare")
def compare():
    silicone_types = db.session.query(Material.silicone_type).distinct().all()
    print_materials = db.session.query(Material.print_material).distinct().all()
    return render_template('compare.html',
                           silicone_types=[s[0] for s in silicone_types],
                           print_materials=[p[0] for p in print_materials])


@app.route("/api/filter")
def api_filter():
    silicone_type = request.args.get('silicone_type', '')
    print_material = request.args.get('print_material', '')

    query = Material.query
    if silicone_type:
        query = query.filter_by(silicone_type=silicone_type)
    if print_material:
        query = query.filter_by(print_material=print_material)

    rows = query.all()
    return jsonify([{
        'Silicone_Type': r.silicone_type,
        '3D_Print_Material': r.print_material,
        'Workability(1-5)': r.workability,
        'Fine Detail & Accuracy(1-5)': r.fine_detail,
        'Mechanical Strength(1-5)': r.mechanical_strength,
        'Mold Reusability(1-5)': r.mold_reusability,
        'Notes': r.notes
    } for r in rows])


@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        entry = Material(
            silicone_type=request.form['silicone_type'],
            print_material=request.form['print_material'],
            workability=int(request.form['workability']),
            fine_detail=int(request.form['fine_detail']),
            mechanical_strength=int(request.form['mechanical_strength']),
            mold_reusability=int(request.form['mold_reusability']),
            notes=request.form['notes']
        )
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    return render_template('submit.html')


if __name__ == "__main__":
    app.run(debug=True)