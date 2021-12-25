from flask import Flask,render_template, request
import pickle
import pandas as pd
import datetime
app= Flask(__name__)
model=pickle.load(open('train_model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    #Sending data from html file to python file
    if request.method=="POST":
        tno=int(request.form["TrainNumber"])
        date_str = str(request.form["date"])
        format_str = '%Y-%m-%d'
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        day = datetime_obj.weekday() + 1
        
        dataset=pd.read_csv('unique.csv')

        ind=0
        l=[]
        flag=False
        trainName=""
        for i in dataset['TrainNo']:
            if i == tno:
                flag=True
                if dataset['Day'][ind]==day:
                    type=dataset['Type'][ind]
                    dist=dataset['Distance'][ind]
                    region=dataset['Region'][ind]
                    trainName=str(dataset['TrainName'][ind])
                    l.append(type)
                    l.append(dist)
                    l.append(region)
                    l.append(day)
                    break
            ind=ind+1

        if flag and len(l)==0:
            message="Train doesn't run on given date"
        elif flag==False:
            message="Given Train Number doesn't exist."
        else:
            final_features=[l]
            predicted_time=int(model.predict(final_features))
    
            time=""
            
            if predicted_time>=60:
                hrs=str(int(predicted_time//60))
                minutes=int(predicted_time%60)
                if minutes==0:
                    time=hrs+ " hrs "
                else:
                    time=hrs + " hrs " + str(minutes) + " minutes"
            elif predicted_time<0:
                message="Train Arriving on Time"
            else:
                time=str(predicted_time) + " minutes "
            message= trainName+" ("+ str(tno) + ") " +"is "+ time +" late."

    #sending data from python file to html file
    return render_template("predict.html",msg=message)

if __name__=="__main__":
    app.run(debug=True)