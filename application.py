
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify,Response
from flask_cors import CORS,cross_origin
import pandas as pd
from pycaret.regression import *
import sqlite3
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use("TkAgg")
plt.switch_backend('agg')
import scipy.stats
import numpy as np
import os
import shutil
import sys
from flask_caching import Cache
import base64
from io import BytesIO

# appending a path
# sys.path.append(r'C:\Users\bhandary\OneDrive - Faurecia\personal\ML - mentor-mentee\Used Cars\final used cars\Flask_')
# from Flask_ import flask_cache_bust


# cache=Cache(config={'CACHE_TYPE':'SimpleCache'})
application = Flask(__name__) # initializing a flask app
# cache.init_app(application)

# application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# flask_cache_bust.init_cache_busting(application)z

@application.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():


    df=pd.read_csv('cars.csv')
    model_name=df[df['manufacturer_name']=='Subaru']['model_name'].unique()
    manufacturer_name = df['manufacturer_name'].unique()
    color = df['color'].unique()
    engine_fuel = df['engine_fuel'].unique()
    engine_type = df['engine_type'].unique()
    body_type= df['body_type'].unique()

    return render_template('index.html', model_name=model_name,manufacturer_name=manufacturer_name,color=color,engine_fuel=engine_fuel,engine_type=engine_type,body_type=body_type,)
    # return render_template("index.html")

@application.route('/predict', methods=['POST', 'GET']) # route to show the predictions in a web UI
# @cache.cached(timeout=1)
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            manufacturer_name = (request.form['manufacturer_name'])
            model_name = (request.form['model_name'])
            transmission = (request.form['transmission'])
            # color = (request.form['color'])
            odometer_value=float(request.form['odometer_value'])
            year_produced = float(request.form['year_produced'])
            engine_fuel = (request.form['engine_fuel'])
            # engine_has_gas = (request.form['engine_has_gas'])
            # engine_type = (request.form['engine_type'])
            engine_capacity = float(request.form['engine_capacity'])
            body_type = (request.form['body_type'])
            # has_warranty = (request.form['has_warranty'])
            # state = (request.form['state'])
            drivetrain = (request.form['drivetrain'])
            # is_exchangeable = (request.form['is_exchangeable'])
            # location_region = (request.form['location_region'])
            number_of_photos = float(request.form['number_of_photos'])
            # up_counter = float(request.form['up_counter'])
            # feature_0 = (request.form['feature_0'])
            feature_1 = bool(request.form['feature_1'])
            feature_2 = bool(request.form['feature_2'])
            feature_3 = bool(request.form['feature_3'])
            feature_4 = bool(request.form['feature_4'])
            # feature_5 = (request.form['feature_5'])
            feature_6 = bool(request.form['feature_6'])
            feature_7 = bool(request.form['feature_7'])
            feature_8 = bool(request.form['feature_8'])
            # feature_9 = (request.form['feature_8'])
            # duration_listed = float(request.form['duration_listed'])

            conn = sqlite3.connect('input.db')
            column_names={'manufacturer':'varchar','model':'varchar','transmission':'varchar','odometer':'Integer','year_prod':'Integer','fuel':'varchar','engine_capacity_in_L':'Integer','body_types':'varchar','drive_train':'varchar','num_of_photos':'Integer','feat_1':'Boolean','feat_2':'Boolean','feat_3':'Boolean','feat_4':'Boolean','feat_6':'Boolean','feat_7':'Boolean','feat_8':'Boolean'}
            c = conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table' AND name = 'user_inputs'")
            if c.fetchone()[0] == 1:
                conn.close()
            else:

                for key in column_names.keys():
                    type = column_names[key]

                    # in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table
                    try:
                        # cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                        conn.execute(
                            'ALTER TABLE user_inputs ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                     dataType=type))
                    except:
                        conn.execute('CREATE TABLE  user_inputs ({column_name} {dataType})'.format(column_name=key,
                                                                                                     dataType=type))
            values=[manufacturer_name,model_name,transmission, odometer_value, year_produced, engine_fuel,engine_capacity, body_type, drivetrain, number_of_photos, feature_1, feature_2,feature_3, feature_4, feature_6, feature_7, feature_8]
            # values = ['manufacturer_name','model_name','transmission', 'odometer_value', 'year_produced', 'engine_fuel','engine_capacity', 'body_type', 'drivetrain', 'number_of_photos', 'feature_1', 'feature_2','feature_3', 'feature_4', 'feature_6', 'feature_7', 'feature_8']
            conn = sqlite3.connect('input.db')
            c = conn.cursor()
            insert_stmt = "INSERT INTO user_inputs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            conn.execute(insert_stmt, values)
            conn.commit()
            # c.execute('INSERT INTO user_inputs VALUES (manufacturer_name,model_name,transmission, odometer_value, year_produced, engine_fuel,engine_capacity, body_type, drivetrain, number_of_photos, feature_1, feature_2,feature_3, feature_4, feature_6, feature_7, feature_8)')
            # conn.execute("INSERT INTO user_inputs (manufacturer,model,transmission,odometer,year_prod,fuel,engine_capacity_in_L,body_types,drive_train,num_of_photos,feat_1,feat_2,feat_3,feat_4,feat_6,feat_7,feat_8) VALUES (manufacturer_name,model_name,transmission, odometer_value, year_produced, engine_fuel,engine_capacity, body_type, drivetrain, number_of_photos, feature_1, feature_2,feature_3, feature_4, feature_6, feature_7, feature_8)")
            conn.close()

            loaded_model=load_model('tuned_xgboost') # loading the model file from the storage

            # filename2 = 'sandardScalar.sav'
            # scalar = pickle.load(open(filename2, 'rb'))
            X=pd.DataFrame([[manufacturer_name,model_name, odometer_value, year_produced,engine_capacity, number_of_photos, feature_1, feature_2,feature_3, feature_4, feature_6, feature_7, feature_8,transmission, engine_fuel, body_type, drivetrain]],columns=['manufacturer_name', 'model_name', 'odometer_value', 'year_produced','engine_capacity', 'number_of_photos', 'feature_1', 'feature_2','feature_3', 'feature_4', 'feature_6', 'feature_7', 'feature_8','transmission', 'engine_fuel', 'body_type', 'drivetrain'])
            # predictions using the loaded model file
            # print(X.head(10))
            prediction=predict_model(loaded_model, data=X)
            print('prediction is', prediction)
            # showing the prediction results in a UI
            prediction = prediction['Label'][0]
            from os.path import exists
            # if exists('static/new_plot.png'):
            #     os.remove('static/new_plot.png')
            for file in os.listdir('static'):
                if file.endswith('.png'):
                    path = os.path.join('static', file)
                    os.remove(path)

            plt.ioff()
            plt.figure(figsize=(10, 10))
            #
            x = np.linspace(0, 30000, 100)
            price=prediction

            plt.plot(x, scipy.stats.norm.pdf(x, 13000, 4000))
            #
            #
            plt.plot([price, price], [0, scipy.stats.norm.pdf(price, 13000, 4000)], c='k', ls='--')
            plt.plot([0, price], [scipy.stats.norm.pdf(price, 13000, 4000), scipy.stats.norm.pdf(price, 13000, 4000)], c='k',ls='--')
            plt.scatter(price, scipy.stats.norm.pdf(price, 13000, 4000), marker='x', s=150, zorder=2,linewidth=2, color='red')



            plt.annotate('Price',ha='center', va='bottom',xytext=(price + 10000, scipy.stats.norm.pdf(price, 13000, 4000) + 0.00001),xy=(price, scipy.stats.norm.pdf(price, 13000, 4000)), arrowprops={'facecolor': 'black'})
            plt.grid()
            plt.xlim(0, 40000)
            plt.ylim(0, 0.00011)
            plt.title('Normal distribution of Price')
            plt.xlabel('Price of Car')
            plt.ylabel('Probability Density')

            import datetime

            # using now() to get current time
            now = datetime.datetime.now()
            timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))
            filename = 'static/new_plot' + timestamp +'.png'
            # buf = BytesIO()
            # plt.savefig(buf, format="png")
            # plt.savefig(filename)
            # data = base64.b64encode(buf.getbuffer()).decode("ascii")

            # plt.savefig(filename,bbox_inches='tight')
            # import matplotlib.image as mpimg
            # mpimg.imsave('new_plot2.png')





            # original = r'C:\Users\bhandary\OneDrive - Faurecia\personal\ML - mentor-mentee\Used Cars\final used cars\new_plot4.png'
            # target = r'C:\Users\bhandary\OneDrive - Faurecia\personal\ML - mentor-mentee\Used Cars\final used cars\static\new_plot.png'
            #
            # shutil.copyfile(original, target)

            # price_pred='Price of this car is :'+ str(prediction) +' Dollars '
            # data = {
            #     "price_pred": price_pred,
            #     "filename": filename,
            # }
            resp ='Price of this car is :'+ str(prediction) +' Dollars '
            # return Response('Price of this car is :'+ str(prediction) +' Dollars ')

            import time


            time.sleep(2)

            return Response(str(prediction))
            # return f"<img src='data:image/png;base64,{data}'/>"

            # return Response(jsonify(list))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')

# @application.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')
#
# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     # fig = plt.figure(figsize=(10, 10))
#
#     x = np.linspace(0, 30000, 100)
#     price=1000
#
#     axis.plot(x, scipy.stats.norm.pdf(x, 13000, 4000))
#
#
#     axis.plot([price, price], [0, scipy.stats.norm.pdf(price, 13000, 4000)], c='k', ls='--')
#     axis.plot([0, price], [scipy.stats.norm.pdf(price, 13000, 4000), scipy.stats.norm.pdf(price, 13000, 4000)], c='k',ls='--')
#     axis.scatter(price, scipy.stats.norm.pdf(price, 13000, 4000), marker='x', s=150, zorder=2,linewidth=2, color='red')
#     #
#     #
#     #
#     axis.annotate('Price',ha='center', va='bottom',xytext=(price + 10000, scipy.stats.norm.pdf(price, 13000, 4000) + 0.00001),xy=(price, scipy.stats.norm.pdf(price, 13000, 4000)), arrowprops={'facecolor': 'black'})
#     # axis.savefig('new_plot.png')
#     # return render_template('untitled1.html', name='new_plot', url='/static/images/new_plot.png')
#     # axis.grid()
#     # axis.xlim(0, 40000)
#     # axis.ylim(0, 0.00011)
#     # axis.title('Normal distribution of Price')
#
#     # xs = range(100)
#     # ys = [random.randint(1, 50) for x in xs]
#     # axis.plot(xs, ys)
#     return fig

@application.route('/plot.png', methods=['POST', 'GET'])
def filename():
    if request.method == 'POST':
        try:

            # prediction = request.values.get('prediction')
            prediction = request.get_data()
            print(prediction)

            plt.ioff()
            plt.figure(figsize=(8, 7))

            x = np.linspace(0, 30000, 10000)
            price = float(prediction)
            print(price)

            mu = 15000
            sigma = 4000

            plt.plot(x, scipy.stats.norm.pdf(x, mu, sigma))

            plt.plot([price, price], [0, scipy.stats.norm.pdf(price, mu, sigma)], c='k', ls='--')
            plt.plot([0, price], [scipy.stats.norm.pdf(price, mu, sigma), scipy.stats.norm.pdf(price, mu, sigma)],
                     c='k', ls='--')
            plt.scatter(price, scipy.stats.norm.pdf(price, mu, sigma), marker='x', s=150, zorder=2,
                        linewidth=2, color='red')

            plt.annotate('Price',
                         ha='center', va='bottom',
                         xytext=(price + 8000, scipy.stats.norm.pdf(price, mu, sigma) + 0.00001),
                         xy=(price, scipy.stats.norm.pdf(price, mu, sigma)), arrowprops={'facecolor': 'black'},
                         fontsize=20)

            plt.grid()
            plt.xlim(0, 31000)
            plt.ylim(0, 0.00012)
            plt.xticks(np.arange(0, 30001, step=2500))
            plt.yticks(np.arange(0, 0.00011, step=0.00001))
            plt.xlabel('Price of Car($)', fontsize=18)
            plt.ylabel('Probability Density', fontsize=18)
            plt.title('Normal distribution of Price', fontsize=18,pad=15)
            buf = BytesIO()
            plt.savefig(buf, format="png",bbox_inches='tight')
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            # data1=f'data:image/png;base64,{data}'
            # return Response(data1, mimetype='image/png')
            # return Response(data, mimetype='image/png;base64')
            # return f"<img src='data:image/png;base64,{data}  '/>"
            return f"data:image/png;base64,{data}"


            # for file in os.listdir('static'):
            #     if file.endswith('.png'):
            #         import time


                    # return Response('static/'+file)

        except Exception  as e:
            print(e)
            return 'something is wrong'



@application.route('/model', methods=['POST', 'GET'])
def model():
    if request.method == 'POST':
        try:
            print('inside model route')
            # manufacturer = request.POST['brand']
            # manufacturer = request.values.get('brand')
            manufacturer = request.get_data()
            # manufacturer=str(str(manufacturer)[1:])
            print(type(manufacturer))
            manufacturer =manufacturer.decode()
            print(type(manufacturer))
            df = pd.read_csv('cars.csv')

            model_name = df[df['manufacturer_name']==manufacturer]['model_name'].unique()
            print(model_name)
            model_name=list(model_name)
            dict={}
            for i in model_name:
                dict[i]=i

            print((dict))
            return jsonify(dict)


        except Exception  as e:
            print(e)
            return 'something is wrong'


# No caching at all for API endpoints.
# @application.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	application.run(debug=True) # running the app