from flask_sqlalchemy import SQLAlchemy

##### Initialize SQLAlchemy #########
db = SQLAlchemy()

#### Define the Company Model Here #########
class CompanyTest(db.Model):
    __tablename__ = 'companies'  ########## Name of the table
    
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    name = db.Column(db.String(100), nullable=False)  # Column for company name
    industry = db.Column(db.String(50))  # Column for industry
    services = db.Column(db.String(200))  # Column for services
    certifications = db.Column(db.String(100))  # Column for certifications
    

    def __repr__(self):
        return f"<CompanyTest {self.name}>"