from flask_sqlalchemy import SQLAlchemy

##### Initialize SQLAlchemy #########
db = SQLAlchemy()

#### Define the Company Model Here #########
class CompanyTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    services = db.Column(db.String(200), nullable=True)
    certifications = db.Column(db.String(200), nullable=True)
