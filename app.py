from flask import Flask, render_template, request
import pandas as pd
import pickle
from auth_method import requires_auth
import json
import math

app = Flask(__name__)

df_vg_bounce_rate = pd.read_csv("vets_gov_bounce_rate.csv")
df_vg_new_sessions = pd.read_csv("vets_gov_new_sessions.csv")
df_vg_sessions = pd.read_csv("vets_gov_sessions.csv")
df_vg_page_views = pd.read_csv("vets_gov_page_views.csv")
df_vg_users = pd.read_csv("vets_gov_users.csv")

df_gb_bounce_rate = pd.read_csv("gi_bill_bounce_rate.csv")
df_gb_new_sessions = pd.read_csv("gi_bill_new_sessions.csv")
df_gb_sessions = pd.read_csv("gi_bill_sessions.csv")
df_gb_page_views = pd.read_csv("gi_bill_page_views.csv")
df_gb_users = pd.read_csv("gi_bill_users.csv")
   
@app.route("/",methods=["GET","POST"])
@requires_auth
def index():
    return render_template("index.html")

@app.route("/vets_dot_gov/timeseries",methods=["GET","POST"])
@requires_auth
def vets_dot_gov_timeseries():
    day_index = ["day_index"] + df_vg_bounce_rate["Day Index"].tolist()
    day_index = [elem for elem in day_index if not type(elem) == type(float())]
    bounce_rate = ["bounce rate"] + [elem.strip("%") for elem in df_vg_bounce_rate["Bounce Rate"].tolist()]
    new_sessions = ["new sessions"] + [elem.strip("%") for elem in df_vg_new_sessions["% New Sessions"].tolist()] 
    sessions = ["sessions"] + df_vg_sessions["Sessions"].tolist()
    page_views = ["page views"] + df_vg_page_views["Pageviews"].tolist() 
    users = ["users"] + df_vg_users["Users"].tolist()
    print type(json.dumps(day_index))

    return render_template(
        "vets_dot_gov_timeseries.html",
        day_index=json.dumps(day_index),
        bounce_rate=json.dumps(bounce_rate),
        new_sessions=json.dumps(new_sessions),
        sessions=json.dumps(sessions),
        page_views=json.dumps(page_views),
        users=json.dumps(users)
    )


def process_sessions(new_sessions,sessions):
    new_sessions = [elem/100 for elem in new_sessions]
    total_new_sessions = []
    for ind,session in enumerate(sessions):
        total_new_sessions.append(session * new_sessions[ind])
    return total_new_sessions

def remove_zeroes(listing):
    return [elem for elem in listing if elem != 0]

@app.route("/vets_dot_gov/stories",methods=["GET","POST"])
@requires_auth
def vets_dot_gov_stories():
    bounce_rates = [float(elem.strip("%")) for elem in df_vg_bounce_rate["Bounce Rate"].tolist()]
    bounce_rates = remove_zeroes(bounce_rates) #[elem for elem in bounce_rates if elem != 0]
    ave_users_finding_what_they_need = sum(bounce_rates)/float(len(bounce_rates))
    new_sessions =  [float(elem.strip("%")) for elem in df_vg_new_sessions["% New Sessions"].tolist()]
    new_sessions = remove_zeroes(new_sessions)
    ave_percentage_of_new_sessions = sum(new_sessions)/float(len(new_sessions))
    sessions =  df_vg_sessions["Sessions"].tolist()
    sessions = remove_zeroes(sessions)
    total_new_sessions = process_sessions(new_sessions,sessions)
    ave_new_sessions_per_day = sum(total_new_sessions)/float(len(total_new_sessions)) 
    page_views = ["page views"] + df_vg_page_views["Pageviews"].tolist() 
    total_users = df_vg_users["Users"].tolist()
    ave_users = sum(total_users)/float(len(total_users))
    
    return render_template(
        "vets_dot_gov_stories.html",
        ave_users_finding_what_they_need=round(ave_users_finding_what_they_need,2),
        ave_new_sessions_per_day=round(ave_new_sessions_per_day,2),
        ave_percentage_of_new_sessions=round(ave_percentage_of_new_sessions,2)
        #users_finding_what_they_need=json.dumps(bounce_rate),
        #new_sessions=json.dumps(new_sessions),
        #sessions=json.dumps(sessions),
        #page_views=json.dumps(page_views),
        #users=json.dumps(users)
    )

@app.route("/gi_bill",methods=["GET","POST"])
@requires_auth
def gi_bill():
    return render_template("gi_bill.html")

@app.route("/comparison",methods=["GET","POST"])
@requires_auth
def comparison():
    return render_template("comparison.html")

app.run(debug=True)
