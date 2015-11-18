from flask import Flask, render_template, request
import pandas as pd
import pickle
from auth_method import requires_auth
import json

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

@app.route("/vets_dot_gov",methods=["GET","POST"])
@requires_auth
def vets_dot_gov():
    day_index = df_vg_bounce_rate["Day Index"].tolist()
    bounce_rate = df_vg_bounce_rate["Bounce Rate"].tolist()
    new_sessions = df_vg_new_sessions["% New Sessions"].tolist() 
    sessions = df_vg_sessions["Sessions"].tolist()
    page_views = df_vg_page_views["Pageviews"].tolist() 
    users = df_vg_users["Users"].tolist()
    
    return render_template(
        "vets_dot_gov.html",
        day_index=day_index,
        bounce_rate=bounce_rate,
        new_sessions=new_sessions,
        sessions=sessions,
        page_views=page_views,
        users=users
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
