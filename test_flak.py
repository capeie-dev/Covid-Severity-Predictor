from flask import Flask, render_template, request, redirect, session
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline
import joblib


app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

model = joblib.load('/home/capeie/covid_severity_predictor/models/rfc_pipeline_hospitalization.pkl')

prediction_out = 'Ambulatory'
prediction_translate = {1:'Ambulatory',2:'Hospitalized'}
@app.route('/',methods=["GET", "POST"])
def index():
    if request.method == "POST":

        req = request.form.to_dict()
        for k,v in req.items():
            if k == 'Age':
                req[k] = float(int(v)/98)
            else:
                req[k] = int(v)
        session['req'] = req
        return redirect(request.url)
    return render_template("form.html")

@app.route('/prediction',methods=['GET','POST'])
def skrtskrt():
    input_dict = session['req']
    df = pd.DataFrame(input_dict,index=[0])
    output = model.predict(df)
    prediction_out = prediction_translate[output[0]]
    return prediction_out
if __name__=="__main__":
    app.run(debug=True)