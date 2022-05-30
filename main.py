from wsgiref import simple_server
from flask import Flask, request, render_template, redirect, url_for
from flask import Response
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import json

from validations import validations
from training import training
from prediction import prediction


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('home.html')

@app.route("/pipeline", methods=['GET'])
@cross_origin()
def pipeline():
    return render_template('pipeline.html')

#page with prediction button
@app.route("/predicttionpage", methods=['GET'])
@cross_origin()
def predicttionpage():
    return render_template('predictionpage.html')

#page with train button
@app.route("/trainingpage", methods=['GET'])
@cross_origin()
def trainingpage():
    return render_template('trainingpage.html')

#page to show info log
@app.route("/infolog", methods=['GET'])
@cross_origin()
def infolog():
    file = open('logs/infolog.txt','r')
    text = file.read()
    return render_template('infolog.html', logtext = text)

#page to show error log
@app.route("/errorlog", methods=['GET'])
@cross_origin()
def errorlog():
    file = open('logs/errorlog.txt','r')
    text = file.read()
    return render_template('errorlog.html', logtext = text)

#clear info log
@app.route('/deleteinfolog')
def deleteinfolog():
    open('logs/infolog.txt', 'w').close()
    return redirect(url_for("infolog"))

#clear error log
@app.route('/deleteerrorlog')
def deleteerrorlog():
    open('logs/errorlog.txt', 'w').close()
    return redirect(url_for("errorlog"))

#fetch info log for training and prediciton instance.
@app.route('/fetchinfo')
def fetchinfo():
    file = open('logs/infolog.txt','r')
    text = file.read()
    print("fetchinfo")
    return Response(text)

#initiate process of prediction
@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        validate_model = validations('Predict')
        validate_model.validate_model()

        predic = prediction()
        path,json_predictions = predic.predict_values()

        return Response("Prediction File created !!!. Few of the predictions are "+str(json.loads(json_predictions) ))

    except Exception as e:
        return Response("Error Occurred! %s" %e)


#initiate process of training
@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        validate_model = validations()
        validate_model.validate_model()

        train_model = training()
        train_model.train_model()

    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

#port = int(os.getenv("PORT",5000))
if __name__ == "__main__":
    #host = '0.0.0.0'
    #port = 5000
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()
    app.run(debug=False)
