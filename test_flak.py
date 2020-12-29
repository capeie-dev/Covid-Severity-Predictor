from flask import Flask, render_template, request, redirect, session
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline
import joblib


app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

hosp_model = joblib.load('/home/capeie/covid_severity_predictor/models/rfc_pipeline_hospitalization.pkl')
icu_model = joblib.load('/home/capeie/covid_severity_predictor/models/rfc_pipeline_ICU.pkl')
ventilator_model = joblib.load('/home/capeie/covid_severity_predictor/models/rfc_pipeline_Ventilator.pkl')
death_model = joblib.load('/home/capeie/covid_severity_predictor/models/rfc_pipeline_Death.pkl')
prediction_out = 'Ambulatory'
prediction_translate = {1:'Can self quarantine',2:'Will need Hospitalization',99:'Not sure'}
general = {0:'Chill no ded ',1:'Rip he ded af'}
icu_translate = {1:'ICU needed',2:"ICU not needed"}
vet_translate = {1:'Ventilator needed',2:"Ventilator not needed"}
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
    hosp_output = hosp_model.predict(df)
    hosp_output = prediction_translate[hosp_output[0]]
    death_output = death_model.predict(df)
    print(death_output)
    prediction_out = general[death_output[0]]
    icu_output = 'Not Applicable'
    ventilator_output = 'Not Applicable'
    if hosp_output == 'Will need Hospitalization':
        icu_output = icu_model.predict(df)
        icu_output = icu_translate[icu_output[0]]
        ventilator_output = ventilator_model.predict(df)
        ventilator_output = vet_translate[ventilator_output[0]]

    return render_template('predictions.html',hosp=hosp_output,ded=prediction_out,icu=icu_output,ventilator=ventilator_output)
    '''if hosp_output[0] == 2:
        icu_output = icu_model.predict(df)
        vent_output = ventilator_model.predict(df)
        lit = (hosp_output,death_output,icu_output,vent_output)
        return lit
    else:
        lit = (hosp_output,death_output)
        return lit'''
if __name__=="__main__":
    app.run(debug=True)