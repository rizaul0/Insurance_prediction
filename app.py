from flask import Flask, render_template, request, url_for
import joblib,sys
import sqlite3,smtplib

my_mail = "YOUR EMAIL"
app_pass = "YOUR APP PASSWORD"


random_forest = joblib.load("models/random_f.lb")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/side", methods=["GET", "POST"])
def side():
    Gender_female = 0
    Gender_male = 0
    smoker_no = 0
    smoker_yes = 0
    region_northeast = 0
    region_northwest = 0
    region_southeast = 0
    region_southwest = 0
    health_HealthyWeight = 0
    health_Overweight = 0
    health_Underweight = 0
    health_obese = 0
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        bmi = request.form['bmi']
        age = request.form['age']
        gen = request.form['gender']
        chl = request.form['children']
        smk = request.form['smoke']
        hlt = request.form['health']
        rgn = request.form['region']

        if gen == "Male":
            Gender_male = 1

        elif gen == "Female":
            Gender_female = 1

        if smk == "YES":
            smoker_yes = 1
        elif smk == "NO":
            smoker_no = 1

        if rgn == "Southeast":
            region_southeast = 1
        elif rgn == "Southwest":
            region_southwest = 1
        elif rgn == "Northeast":
            region_northeast = 1
        elif rgn == "Northwest":
            region_northwest = 1

        if hlt == "Underweight":
            health_Underweight = 1
        elif hlt == "HealthyWeight":
            health_HealthyWeight = 1
        elif hlt == "Overweight":
            health_Overweight = 1
        elif hlt == "Obese":
            health_obese = 1

        user = {"bmi": bmi, "age": age, "gen": gen, "chl": chl, "smk": smk, "hlt": hlt, "rgn": rgn}
        # print(type(user["age"]))
        data_insert_query = """
        INSERT INTO project (name,email,age, bmi, chl, rgn, smk, gen, hlt, predict)
        VALUES (?,?,?, ?, ?, ?, ?, ?, ?, ?)
        """
        unseen = [[age, bmi, chl, Gender_female, Gender_male, smoker_no, smoker_yes, region_northeast, region_northwest
                      , region_southeast, region_southwest, health_HealthyWeight, health_Overweight, health_Underweight,
                   health_obese]]
        print(unseen)
        predict = random_forest.predict(unseen)[0]
        print(predict)
        connect = sqlite3.connect("insurance.db")
        curses = connect.cursor()
        data = (name,email,age, bmi, chl, rgn, smk, gen, hlt, predict)
        curses.execute(data_insert_query, data)
        print("you data is inserted into database")
        connect.commit()
        curses.close()
        connect.close()
        with smtplib.SMTP("smtp.gmail.com",port=587) as server:
            server.starttls()
            server.login(my_mail,app_pass)
            server.sendmail(my_mail,email,msg=f"Subject:Insurance Prediction\n\n Hello their\n{name}\nThis are the "
                                              f"details that you have submitted"
                                              f"\nname: {name}"
                                              f"\nage: {age}"
                                              f"\ngender: {gen}"
                                              f"\nbmi {bmi}"
                                              f"\nhealth: {hlt}"
                                              f"\nregion: {rgn}"
                                              f"\nsmoke: {smk}"
                                              f"\nNo. of children: {chl}"
                                              f"\n\n your annual Insurance ammount is predicted to be"
                                              f"\n : {predict}")

    return user


if __name__ == "__main__":
    app.run(debug=True)
