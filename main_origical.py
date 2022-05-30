from wsgiref import simple_server
from flask import Flask, request, render_template
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
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        print('test1')
        print(request)
 #       if request.json is not None:
        print('test3')
        validate_model = validations('Predict')
        validate_model.validate_model()

        predic = prediction()
        path,json_predictions = predic.predict_values()

        return Response("Prediction File created !!!. Few of the predictions are "+str(json.loads(json_predictions) ))

#        elif request.form is not None:
#            print('test2')
#            validate_model = validations('Predict')
#            validate_model.validate_model()

#            predic = prediction()
#            path,json_predictions = predic.predict_values()
            
#            return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
#        else:
#            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            validate_model = validations()
            validate_model.validate_model()

            train_model = training()
            train_model.train_model()

    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

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
