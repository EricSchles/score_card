from flask import Flask, render_template, request
import pandas as pd
import pickle
import json
import math

app = Flask(__name__)

df_vg_bounce_rate = pd.read_csv("vets_gov_bounce_rate.csv")
df_vg_new_sessions = pd.read_csv("vets_gov_new_sessions.csv")
df_vg_sessions = pd.read_csv("vets_gov_sessions.csv")
df_vg_page_views = pd.read_csv("vets_gov_page_views.csv")
df_vg_users = pd.read_csv("vets_gov_users.csv")
df_vg_ave_session_duration = pd.read_csv("vets_gov_ave_session_duration.csv")

df_gb_bounce_rate = pd.read_csv("gi_bill_bounce_rate.csv")
df_gb_new_sessions = pd.read_csv("gi_bill_new_sessions.csv")
df_gb_sessions = pd.read_csv("gi_bill_sessions.csv")
df_gb_page_views = pd.read_csv("gi_bill_page_views.csv")
df_gb_users = pd.read_csv("gi_bill_users.csv")
df_gb_ave_session_duration = pd.read_csv("gi_bill_ave_session_duration.csv")
   
@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/vets_dot_gov/timeseries",methods=["GET","POST"])
def vets_dot_gov_timeseries():
    day_index = ["day_index"] + df_vg_bounce_rate["Day Index"].tolist()
    day_index = [elem for elem in day_index if not type(elem) == type(float())]
    bounce_rate = ["bounce rate"] + [elem.strip("%") for elem in df_vg_bounce_rate["Bounce Rate"].tolist()]
    new_sessions = ["new sessions"] + [elem.strip("%") for elem in df_vg_new_sessions["% New Sessions"].tolist()] 
    sessions = ["sessions"] + df_vg_sessions["Sessions"].tolist()
    page_views = ["page views"] + df_vg_page_views["Pageviews"].tolist() 
    users = ["users"] + df_vg_users["Users"].tolist()
    return render_template(
        "vets_dot_gov_timeseries.html",
        day_index=json.dumps(day_index),
        bounce_rate=json.dumps(bounce_rate),
        new_sessions=json.dumps(new_sessions),
        sessions=json.dumps(sessions),
        page_views=json.dumps(page_views),
        users=json.dumps(users)
    )

@app.route("/gi_bill/timeseries",methods=["GET","POST"])
def gi_bill_timeseries():
    day_index = ["day_index"] + df_gb_bounce_rate["Day Index"].tolist()
    day_index = [elem for elem in day_index if not type(elem) == type(float())]
    bounce_rate = ["bounce rate"] + [elem.strip("%") for elem in df_gb_bounce_rate["Bounce Rate"].tolist()]
    new_sessions = ["new sessions"] + [elem.strip("%") for elem in df_gb_new_sessions["% New Sessions"].tolist()] 
    sessions = ["sessions"] + df_gb_sessions["Sessions"].tolist()
    page_views = ["page views"] + df_gb_page_views["Pageviews"].tolist() 
    users = ["users"] + df_gb_users["Users"].tolist()
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

def strip_percentage(listing):
    return [float(elem.strip("%")) for elem in listing]

def average(listing):
    return sum(listing)/float(len(listing))

def invert_percentage(listing):
    return [100-elem for elem in listing]

def to_seconds(listing):
    new_listing = []
    for elem in listing:
        seconds = 0
        hour_minute_second = elem.split(":")
        seconds += (int(hour_minute_second[0])*60)*60 #total hours
        seconds += (int(hour_minute_second[1])* 60) #total minutes
        seconds += int(hour_minute_second[2])
        new_listing.append(seconds)
    return new_listing
        
def calc_pages_per_session(page_views,sessions):
    pages_per_session = []
    for ind,page_view in enumerate(page_views):
        pages_per_session.append(page_view/float(sessions[ind]))
    return pages_per_session



@app.route("/vets_dot_gov/stories",methods=["GET","POST"])
def vets_dot_gov_stories():
    bounce_rates = strip_percentage(df_vg_bounce_rate["Bounce Rate"].tolist())
    bounce_rates = remove_zeroes(bounce_rates) 
    inverse_bounce_rates = invert_percentage(bounce_rates)
    ave_users_finding_what_they_need = average(inverse_bounce_rates)
    new_sessions =  strip_percentage(df_vg_new_sessions["% New Sessions"].tolist())
    new_sessions = remove_zeroes(new_sessions)
    ave_percentage_of_new_sessions = average(new_sessions)
    sessions =  df_vg_sessions["Sessions"].tolist()
    sessions = remove_zeroes(sessions)
    total_new_sessions = process_sessions(new_sessions,sessions)
    ave_new_sessions_per_day = average(total_new_sessions) 
    page_views = ["page views"] + df_vg_page_views["Pageviews"].tolist()
    page_views = remove_zeroes(page_views)
    total_users = df_vg_users["Users"].tolist()
    ave_users = average(total_users)
    ave_session_duration = average(to_seconds(df_vg_ave_session_duration["Avg. Session Duration"].tolist()))/float(60)
    ave_pages_per_session = average(calc_pages_per_session(page_views[1:],sessions[1:]))
    
    return render_template(
        "vets_dot_gov_stories.html",
        ave_users_finding_what_they_need=round(ave_users_finding_what_they_need,2),
        ave_new_sessions_per_day=round(ave_new_sessions_per_day,2),
        ave_percentage_of_new_sessions=round(ave_percentage_of_new_sessions,2),
        ave_session_duration=round(ave_session_duration,2),
        ave_pages_per_session=round(ave_pages_per_session,2),
        gi_bill=False,
        vets_dot_gov=True
        #users_finding_what_they_need=json.dumps(bounce_rate),
        #new_sessions=json.dumps(new_sessions),
        #sessions=json.dumps(sessions),
        #page_views=json.dumps(page_views),
        #users=json.dumps(users)
    )

@app.route("/gi_bill/stories",methods=["GET","POST"])
def gi_bill_stories():
    bounce_rates = strip_percentage(df_gb_bounce_rate["Bounce Rate"].tolist())
    bounce_rates = remove_zeroes(bounce_rates) #[elem for elem in bounce_rates if elem != 0]
    inverse_bounce_rates = invert_percentage(bounce_rates)
    ave_users_finding_what_they_need = average(inverse_bounce_rates)
    new_sessions =  strip_percentage(df_gb_new_sessions["% New Sessions"].tolist())
    new_sessions = remove_zeroes(new_sessions)
    ave_percentage_of_new_sessions = average(new_sessions)
    sessions =  df_gb_sessions["Sessions"].tolist()
    sessions = remove_zeroes(sessions)
    total_new_sessions = process_sessions(new_sessions,sessions)
    ave_new_sessions_per_day = average(total_new_sessions) 
    page_views = ["page views"] + df_gb_page_views["Pageviews"].tolist() 
    total_users = df_vg_users["Users"].tolist()
    ave_users = average(total_users)
    ave_session_duration = average(to_seconds(df_gb_ave_session_duration["Avg. Session Duration"].tolist()))/float(60)
    ave_pages_per_session = average(calc_pages_per_session(page_views[1:],sessions[1:]))

    return render_template(
        "vets_dot_gov_stories.html",
        ave_users_finding_what_they_need=round(ave_users_finding_what_they_need,2),
        ave_new_sessions_per_day=round(ave_new_sessions_per_day,2),
        ave_percentage_of_new_sessions=round(ave_percentage_of_new_sessions,2),
        ave_session_duration=round(ave_session_duration,2),
        ave_pages_per_session=round(ave_pages_per_session,2),
        gi_bill=True,
        vets_dot_gov=False
        #users_finding_what_they_need=json.dumps(bounce_rate),
        #new_sessions=json.dumps(new_sessions),
        #sessions=json.dumps(sessions),
        #page_views=json.dumps(page_views),
        #users=json.dumps(users)
    )



@app.route("/comparison",methods=["GET","POST"])
def comparison():
    return render_template("comparison.html")

if __name__ == '__main__':
    app.run(debug=True)
