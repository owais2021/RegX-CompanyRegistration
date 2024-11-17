from flask import Blueprint

##### Define Blueprint for views here ########
views = Blueprint('views', __name__)

##### Route for the homepage here ####
@views.route('/')
def home():
    return "****Welcome to the RegX Company Registration Platform****"