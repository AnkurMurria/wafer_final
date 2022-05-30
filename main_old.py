from validations import validations
from training import training
from prediction import prediction

def train_model():
    validate_model = validations()
    validate_model.validate_model()

    train_model = training()
    train_model.train_model()


def predict_values():
    #validate_model = validations('Predict')
    #validate_model.validate_model()

    predic = prediction()
    predic.predict_values()



predict_values()