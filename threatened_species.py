from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os
 
app = Flask(__name__)
 
MONGODB_URI = 'mongodb://heroku_1cxrtrp8:cd70hc9kcckhahnsgvelevsrj4@ds149132.mlab.com:49132/heroku_1cxrtrp8'
DBS_NAME = 'heroku_1cxrtrp8'
# MONGODB_URI = os.environ.get('MONGODB_URI')
# DBS_NAME = os.environ.get('MONGO_DB_NAME', 'endangeredspecies')
COLLECTION_NAME = os.environ.get('MONGO_COLLECTION_NAME', 'species')



# MONGODB_HOST = 'localhost'
# MONGODB_PORT = 27017
# DBS_NAME = 'endangeredSpecies'
# COLLECTION_NAME = 'species'
 
 

@app.route("/")
def graph():
    return render_template("graphs.html")

 
@app.route("/endangeredSpecies/species")
def endangered_species():
    """
    A Flask view to serve the project data from
    MongoDB in JSON format.
    """
 
    # A constant that defines the record fields that we wish to retrieve.
    FIELDS = {
        '_id': False, 
        'IUCN Category': True,
        'IUCN': True,
        'Species': True,
        'Country': True, 
        'Value': True,
        'Indigenous': True
    }
 
    # Open a connection to MongoDB using a with statement such that the
    # connection will be closed as soon as we exit the with statement
    with MongoClient(MONGODB_URI) as conn:
        # Define which collection we wish to access
        collection = conn[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the the results to 55000
        projects = collection.find(projection=FIELDS, limit=55000)
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps(list(projects))
 
 
if __name__ == "__main__":
    app.run(debug=True)