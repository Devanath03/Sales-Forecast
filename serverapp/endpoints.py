import logging
import os
from flask_pymongo import pymongo
from flask import jsonify, request
import pandas as pd
from flask import Flask, request, send_file
from pymongo import MongoClient
import csv
from flask import Flask, request, make_response
import io 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timedelta
from bson import ObjectId
import matplotlib
matplotlib.use('Agg')

con_string = "mongodb+srv://devanath:devanath432@cluster0.8x4ss8e.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('testdb') #('database name')

user_collection = pymongo.collection.Collection(db, 'forecast') #(<database_name>,"<collection_name>")

print("MongoDB connected Successfully...")


def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world'
        return res    
    
    @endpoints.route('/file_upload',methods=['GET','POST'])
    def file_upload():
        resp = {}
        try:
            req = request.form
            file = request.files.get('file')
            period = request.form['select'] #selected value in the option pane
            time = request.form['period']  #typed value value in the time interval
            p = pd.read_csv(io.StringIO(file.read().decode('iso-8859-1')))
            print(p)
            temp_file_path = r'D:\Angular\Sales-Forecast\src\assets\temp_file.csv'
            p.to_csv(temp_file_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
            if period=='1':
                df = pd.read_csv(temp_file_path, parse_dates=['date'])
                df.set_index('date', inplace=True)
                df = df.resample('M').sum()
                df['year'] = df.index.year
                df['month'] = df.index.month
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'month']], df['sales'], test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                    # make predictions on the testing data
                y_pred = model.predict(X_test)
                    # calculate the mean squared error and R-squared score
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                print('Mean squared error: ', mse)
                print('R-squared score: ', r2)
                n_years = int(time)
                next_years = pd.DataFrame({'year': [df.index.max().year + i for i in range(1, n_years+1)] * 12, 'month': np.tile(np.arange(1, 13), n_years)})
                next_years.set_index(pd.date_range(start='{}-01-01'.format(next_years.year.min()), periods=n_years*12, freq='M'), inplace=True)
                next_years['sales'] = model.predict(next_years[['year', 'month']])
                    # plot the predicted sales for the next 5 years
                plt.plot(df.index, df['sales'], label='Actual')
                plt.plot(next_years.index, next_years['sales'], label='Predicted')
                save_dir = r"D:\Angular\Sales-Forecast\src\assets"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                plt.xlabel('Year')
                plt.ylabel('Sales')
                plt.legend()
                plt.savefig(os.path.join(save_dir, 'predict.png'))
                plt.close()
                return time
            if period=='2':
                df = pd.read_csv(temp_file_path, parse_dates=['date'])
                df.set_index('date', inplace=True)
                df = df.resample('M').sum()
                df['year'] = df.index.year
                df['month'] = df.index.month
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'month']], df['sales'], test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                print('Mean squared error: ', mse)
                print('R-squared score: ', r2)
                n_months = int(time)
                next_months = pd.DataFrame({'year': [df.index.max().year] * n_months, 'month': np.arange(df.index.max().month+1, df.index.max().month+1+n_months)})
                next_months.set_index(pd.date_range(start=df.index.max()+pd.DateOffset(months=1), periods=n_months, freq='M'), inplace=True)
                next_months['sales'] = model.predict(next_months[['year', 'month']])
                plt.plot(df.index, df['sales'], label='Actual')
                plt.plot(next_months.index, next_months['sales'], label='Predicted')
                save_dir = r"D:\Angular\Sales-Forecast\src\assets"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                plt.xlabel('Month')
                plt.ylabel('Sales')
                plt.legend()
                plt.savefig(os.path.join(save_dir, 'predict.png'))
                plt.close()
                return time
            if period == '3':
                df = pd.read_csv(temp_file_path, parse_dates=['date'])
                df.set_index('date', inplace=True)
                df = df.resample('W').sum()
                df['year'] = df.index.year
                df['week'] = df.index.week
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'week']], df['sales'], test_size=0.2, random_state=42)

                model = LinearRegression()
                model.fit(X_train, y_train)

                n_weeks = int(time)
                next_weeks = pd.DataFrame({'year': [df.index.max().year] * n_weeks, 'week': np.arange(df.index.max().week+1, df.index.max().week+1+n_weeks)})
                next_weeks.set_index(pd.date_range(start=df.index.max()+pd.DateOffset(weeks=1), periods=n_weeks, freq='W-MON'), inplace=True)
                next_weeks['sales'] = model.predict(next_weeks[['year', 'week']])

                plt.plot(df.index, df['sales'], label='Actual')
                plt.plot(next_weeks.index, next_weeks['sales'], label='Predicted')
                plt.xlabel('Week')
                plt.ylabel('Sales')
                plt.legend()
                save_dir = r"D:\Angular\Sales-Forecast\src\assets"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                filename = 'predict.png'
                filepath = os.path.join(save_dir, filename)
                with open(filepath, 'wb') as f:
                    plt.savefig(f)
                plt.close()
                return time
            if period =='4':
                df = pd.read_csv(temp_file_path, parse_dates=['date'])
                df.set_index('date', inplace=True)
                df = df.resample('D').sum()
                df['year'] = df.index.year
                df['month'] = df.index.month
                df['day'] = df.index.day
                X_train, X_test, y_train, y_test = train_test_split(df[['year', 'month', 'day']], df['sales'], test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                n_days = int(time)
                next_days = pd.DataFrame({'year': [df.index.max().year] * n_days, 'month': [df.index.max().month] * n_days, 'day': np.arange(df.index.max().day+1, df.index.max().day+1+n_days)})
                next_days.set_index(pd.date_range(start=df.index.max()+pd.DateOffset(days=1), periods=n_days, freq='D'), inplace=True)
                next_days['sales'] = model.predict(next_days[['year', 'month', 'day']])
                plt.plot(df.index, df['sales'], label='Actual')
                plt.plot(next_days.index, next_days['sales'], label='Predicted')
                plt.xlabel('Day')
                plt.ylabel('Sales')
                plt.legend()
                save_dir = r"D:\Angular\Sales-Forecast\src\assets"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                filename = 'predict.png'
                filepath = os.path.join(save_dir, filename)
                with open(filepath, 'wb') as f:
                    plt.savefig(f)
                plt.close()
                return time
            status = {
                "statusCode":"200",
                "statusMessage":"File uploaded Successfully."
            }
            
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = {
                'username':request.form['username'],
                'password':request.form['password']
            }
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
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
        resp["status"] =status
        return resp 

    @endpoints.route('/check-user', methods=['POST'])
    def check_user():
        resp = {}
        try:
            req_body = {
            'username':request.form['username'],
            'password':request.form['password']
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