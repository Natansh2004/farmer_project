from flask import Flask,render_template,url_for,request
import os,joblib
import pandas as pd
from pymongo import MongoClient

# pymongo is used for making connection with mongoDB using python

std_scaler = joblib.load('./models/std_scaler.lb')
kmeans_model = joblib.load('./models/kmeans_model.lb')
df = pd.read_csv('./models/filter_crops.csv')

app = Flask(__name__)

# mongodb+srv://minanatansh:DYDoAsfdzqta5ay9@natansh2004.y0fuz.mongodb.net/?retryWrites=true&w=majority&appName=Natansh2004

connection_string = 'mongodb+srv://minanatansh:DYDoAsfdzqta5ay9@natansh2004.y0fuz.mongodb.net/?retryWrites=true&w=majority&appName=Natansh2004'
client = MongoClient(connection_string)  # client == connection
# database, collection

database = client["Farmer"]    # database created (database name is 'Farmer')
collection = database["FarmerData"]  # table creation or in MongoDB it's called collection
# MongoDB is no-sql, so it do not have any tables, it has collection



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        n = int(request.form['N'])
        p = int(request.form['P'])
        k = int(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['PH'])
        rainfall = float(request.form['rainfall'])

        # we need to convert type='number' to type='text' for all those that are float

        UNSEEN_DATA = [[n,p,k,temperature,humidity,ph,rainfall]]

        transformed_data = std_scaler.transform(UNSEEN_DATA)  # scale down the data
        cluster = kmeans_model.predict(transformed_data)[0]
        suggestion_crops = list(df[df['cluster_no'] == cluster]['label'].unique())

        # inserting data 

        # In mongoDB, we pass values in the form of dictionary, not in the form of tuple like in MySQL
        data = {'N':n,'P':p,'K':k,'temperature':temperature,'humidity':humidity,'PH':ph,'rainfall':rainfall}
        data_id = collection.insert_one(data).inserted_id
        # insert 'data' inside 'collection'
        # everytime when we insert any value in mongoDB, it gives us an ID 
        print('Your data is inserted in MongoDB and your record ID is: ',data_id)

        return f'Suggested crops: {suggestion_crops}'
        

if __name__ == '__main__':
    app.run(debug=True)