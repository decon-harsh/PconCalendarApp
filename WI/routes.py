from __future__ import print_function
import os, shutil
import datetime
import pickle
import os.path
import json

from flask import render_template, url_for, flash, redirect, request,session
from WI import app
from uuid import uuid4
from .forms import EventForm

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# routes

@app.route("/logout", methods=["GET", "POST"])
def logout():
    creds = session.get('mycred',None)
    if creds:
        session['mycred'] = None
    return redirect(url_for("home"))


@app.route("/", methods=["GET", "POST"])
def home():

    try:
        SCOPES = ["https://www.googleapis.com/auth/calendar"]

        creds_data = session.get('mycred',None)
        if creds_data:
            creds = Credentials(creds_data['token'])
        else:
            creds=None        

        # If there are no (valid) credentials available, let the user log in else pass next.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                creds_data = {
                    'token': creds.token,
                    'refresh_token': creds.refresh_token,
                    'token_uri': creds.token_uri,
                    'client_id': creds.client_id,
                    'client_secret': creds.client_secret,
                    'scopes': creds.scopes
                }
                # Saving the credentials in browser memory
                session['mycred']=creds_data

        service = build("calendar", "v3", credentials=creds)

        # getting all events (needs to make it asynch in future) 
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        result = []
        for event in events:
            try:
                grouplist=[x['email'] for x in event['attendees']]
            except:
                grouplist =[]
            try:
                result.append(
                    {
                        "title": event['summary'],
                        "start": event["start"]["dateTime"],
                        "end": event["end"]["dateTime"],
                        'extendedProps':[i for i in grouplist],
                    }
                )
            except:
                pass

        result = result if len(result) > 0 else [] 

        return render_template("main.html", data=json.dumps(result))
    except:
        return redirect(url_for("logout"))

@app.route("/create", methods=["GET", "POST"])

def create_event():

    try:
        SCOPES = ["https://www.googleapis.com/auth/calendar"]

        creds_data = session.get('mycred',None)
        if creds_data:
            creds = Credentials(creds_data['token']) 
        else:
            creds = None      

        # If there are no (valid) credentials available, let the user log in else pass next.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                creds_data = {
                    'token': creds.token,
                    'refresh_token': creds.refresh_token,
                    'token_uri': creds.token_uri,
                    'client_id': creds.client_id,
                    'client_secret': creds.client_secret,
                    'scopes': creds.scopes
                }
                # Saving the credentials
                session['mycred']=creds_data

        def createEvent(summary,start_datetime,end_datetime,**kwargs):

            attendees_email=kwargs.get('attendees_email',[])

            if kwargs.get('meetOption',"Not Clicked") == "Clicked":
                    
                meet_id=uuid4().hex

                add_event= {
                    "summary": summary,
                    "location": kwargs.get('location','Not specified'),
                    "description": f"{meet_id}",
                    "start": {
                        "dateTime": start_datetime,
                        "timeZone": "Asia/Kolkata",
                    },
                    "end": {
                        "dateTime": end_datetime,
                        "timeZone": "Asia/Kolkata",
                    },
                    "attendees": [{"email": x} for x in attendees_email],
                    "conferenceData": {
                        "createRequest": {
                            "requestId": f"{meet_id}",
                            "conferenceSolutionKey": {"type": "hangoutsMeet"}
                        }
                    },
                    "recurrence":[
                        "RRULE:{}".format(str(kwargs.get('RRULE','FREQ=DAILY;INTERVAL=1;COUNT=1')))
                    ],
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 24 * 60},
                            {"method": "popup", "minutes": 10},
                        ],
                    },
                }

            else:
                add_event= {
                    "summary": summary,
                    "location": kwargs.get('location','Not specified'),
                    "description": kwargs.get('description','Not specified'),
                    "start": {
                        "dateTime": start_datetime,
                        "timeZone": "Asia/Kolkata",
                    },
                    "end": {
                        "dateTime": end_datetime,
                        "timeZone": "Asia/Kolkata",
                    },
                    "attendees": [{"email": x} for x in attendees_email],
                    "recurrence":[
                        "RRULE:{}".format(str(kwargs.get('RRULE','FREQ=DAILY;INTERVAL=1;COUNT=1')))
                    ],
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 24 * 60},
                            {"method": "popup", "minutes": 10},
                        ],
                    },
                }

            service = build("calendar", "v3", credentials=creds)
            event = service.events().insert(calendarId='primary', body=add_event).execute()
            return("Success")

        
        form = EventForm()
        if form.validate_on_submit():
            title = form.title.data
            grouplist= list(map(str,(form.group.data).split(" ")))
            start_datetime = form.daterange.data.split("-")[0].rstrip()
            end_datetime = form.daterange.data.split("-")[1].lstrip()
            start_datetime = datetime.datetime.strptime(start_datetime,'%d/%m/%Y %H:%M').isoformat() # 'Z' indicates UTC time
            end_datetime = datetime.datetime.strptime(end_datetime,'%d/%m/%Y %H:%M').isoformat() # 'Z' indicates UTC time
            createEvent(title,start_datetime,end_datetime,attendees_email=grouplist)
            flash("Event created successfully",'success')
            
        return render_template("create.html",form=form)    

    except:
        return redirect(url_for("logout"))
