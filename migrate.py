import pandas as pd
from app import app, db, Material

with app.app_context():
    db.create_all()
    df = pd.read_csv('data.csv')
    df.columns = df.columns.str.strip()
    for _, row in df.iterrows():
        entry = Material(
            silicone_type=row['Silicone_Type'],
            print_material=row['3D_Print_Material'],
            workability=int(row['Workability(1-5)']),
            fine_detail=int(row['Fine Detail & Accuracy(1-5)']),
            mechanical_strength=int(row['Mechanical Strength(1-5)']),
            mold_reusability=int(row['Mold Reusability(1-5)']),
            notes=row['Notes']
        )
        db.session.add(entry)
    db.session.commit()
    print("Migration complete")