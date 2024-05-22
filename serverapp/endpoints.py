import logging
import os
from flask_pymongo import pymongo
from flask import jsonify, request, send_file, Blueprint, Flask
import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib
matplotlib.use('Agg')
from flask_cors import CORS

con_string = "mongodb+srv://devanath:devanath432@cluster0.8x4ss8e.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_string)
db = client.get_database('testdb')
user_collection = pymongo.collection.Collection(db, 'forecast')

print("MongoDB connected Successfully...")

def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world'
        return res    

    @endpoints.route('/file_upload', methods=['POST'])
    def file_upload():
        try:
            file = request.files.get('file')
            period = request.form['select']
            time = request.form['period']
            df = pd.read_csv(io.StringIO(file.read().decode('iso-8859-1')), parse_dates=['date'], dayfirst=True)

            if period == '1':
                df.set_index('date', inplace=True)
                df = df.resample('M').sum()
                df['year'] = df.index.year
                df['month'] = df.index.month
                x_label = "Years"
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'month']], df['sales'], test_size=0.2, random_state=42)
            elif period == '2':
                df.set_index('date', inplace=True)
                df = df.resample('M').sum()
                df['year'] = df.index.year
                df['month'] = df.index.month
                x_label = "Months"
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'month']], df['sales'], test_size=0.2, random_state=42)
            elif period == '3':
                df.set_index('date', inplace=True)
                df = df.resample('W').sum()
                df['year'] = df.index.year
                df['week'] = df.index.isocalendar().week
                x_label="Weeks"
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'week']], df['sales'], test_size=0.2, random_state=42)
            elif period == '4':
                df.set_index('date', inplace=True)
                df = df.resample('D').sum()
                df['year'] = df.index.year
                df['month'] = df.index.month
                df['day'] = df.index.day
                x_label = "Days"
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'month', 'day']], df['sales'], test_size=0.2, random_state=42)
            else:
                return jsonify({"statusCode": "400", "statusMessage": "Invalid period"}), 400

            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            if period == '1':
                n_years = int(time)
                next_dates = pd.date_range(start=df.index.max() + pd.DateOffset(months=1), periods=n_years * 12, freq='M')
                next_periods = pd.DataFrame({'year': next_dates.year, 'month': next_dates.month}, index=next_dates)
            elif period == '2':
                n_months = int(time)
                next_dates = pd.date_range(start=df.index.max() + pd.DateOffset(months=1), periods=n_months, freq='M')
                next_periods = pd.DataFrame({'year': next_dates.year, 'month': next_dates.month}, index=next_dates)
            elif period == '3':
                n_weeks = int(time)
                next_dates = pd.date_range(start=df.index.max() + pd.DateOffset(weeks=1), periods=n_weeks, freq='W-MON')
                next_periods = pd.DataFrame({'year': next_dates.year, 'week': next_dates.isocalendar().week}, index=next_dates)
            elif period == '4':
                n_days = int(time)
                next_dates = pd.date_range(start=df.index.max() + pd.DateOffset(days=1), periods=n_days, freq='D')
                next_periods = pd.DataFrame({'year': next_dates.year, 'month': next_dates.month, 'day': next_dates.day}, index=next_dates)

            next_periods['sales'] = model.predict(next_periods[['year', 'month']] if period in ['1', '2'] else next_periods[['year', 'week']] if period == '3' else next_periods[['year', 'month', 'day']])
            
            plt.plot(df.index, df['sales'], label='Actual')
            plt.plot(next_periods.index, next_periods['sales'], label='Predicted')
            plt.xlabel(x_label)
            plt.ylabel('Sales')
            plt.legend()

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()

            return send_file(img, mimetype='image/png')

        except Exception as e:
            return jsonify({"statusCode": "400", "statusMessage": str(e)}), 400

    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = {
                'username': request.form['username'],
                'password': request.form['password']
            }
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp 

    @endpoints.route('/check-user', methods=['POST'])
    def check_user():
        resp = {}
        try:
            req_body = {
            'username': request.form['username'],
            'password': request.form['password']
            }
            user = user_collection.find_one(req_body)
            if user:
                status = {
                "statusCode": "200",
                "statusMessage": "User Found in the Database."
                }
                resp["data"] = True
            else:
                status = {
                "statusCode": "200",
                "statusMessage": "User Not Found in the Database."
                }
                resp["data"] = False
        
        except Exception as e:
            print(e)
            status = {
            "statusCode":"400",
            "statusMessage":str(e)
            }
            resp["data"] = False
        
        resp["status"] = status
        return resp
               
    return endpoints
