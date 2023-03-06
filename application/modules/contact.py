from flask import Blueprint, g, render_template, session, redirect, url_for, current_app
import uuid
from application.modules.auth import login_required, team_required
from application.forms import *
from application.data_models import *
import json
import base64
from datetime import datetime, timedelta, timezone
from dateutil import parser
from email.mime.text import MIMEText
import pytz
from sqlalchemy import func, Integer

contact_bp = Blueprint('contact_bp', __name__, template_folder="templates")
turbo = current_app.extensions.get("turbo")
google = current_app.extensions.get("oauthlib.client").google

@contact_bp.route("/contact/<contact_id>/<activity>", defaults={"reply": None, "complete": "false"}, methods=["GET", "POST"])
@contact_bp.route("/contact/<contact_id>/<activity>/<reply>", methods=["GET", "POST"], defaults={"complete": "false"})
@contact_bp.route("/contact/<contact_id>/<activity>/<complete>", defaults={"reply": None}, methods=["GET", "POST"])
@login_required
@team_required
def contact(contact_id, activity, reply, complete):
    """contact =
    This is the route for the contact page i.e. an individual contact, not the list.
    Calls the relevant function depending on user selection.

    <activity>
    ----------
    emails -- Sending and viewing emails to and from the contact.
    notes -- Add and view notes related to the contact.
    """
    form = EmailForm()
    if reply != None:
        reply = reply.split(",")
        form.subject.data = reply[2]
    noteForm = NoteForm()
    contact = Contacts.query.filter_by(
        contact_id=contact_id, team_id=g.team_id).first()
    google_token = session.get("google_token")
    google_email = session.get("user_google")
    if activity == "emails":
        return email_activity(google_token, form, google_email, contact_id, contact, reply)
    elif activity == "notes":
        return notes_activity(contact_id, google_token, contact)
    elif activity == "meetings":
        return meetings_activity(contact_id, google_token, contact)
    elif activity == "tasks":
        return tasks_activity(contact_id, google_token, contact, complete)
    else:
        return view_activity(contact_id, google_token, contact)

def meetings_activity(contact_id, google_token, contact):
    form = MeetingForm()
    if google_token != None:
        if form.validate_on_submit():
            response = schedule_meeting(form, contact)
            if response.status != 200:
                return redirect(url_for('authorize_email', contact_id=contact_id))
            form.title.data = ""
            form.description.data = ""
            form.date_time_start.data = None
            form.date_time_end.data = None

            # Log activity with log table
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            log_activity("meeting", g.email, timestamp, contact_id)
        try:
            response_status, meetings = get_meetings(contact.email)
            if response_status != 200:
                return redirect(url_for('authorize_email', contact_id=contact_id))
        except:
            meetings=None
    # User isn't authenticated, redirect them so they can oAuth their email.
    else:
        return redirect(url_for('authorize_email', contact_id=contact_id))
    # If we can, just update the part of the page that's changed i.e. the activity box.
    if turbo.can_stream():
        return turbo.stream(turbo.update(render_template("contact_interactions.html", contact=contact, google_token=google_token, activity="meetings", form=form, meetings=meetings), 'activity_box'))
    else:
        return render_template("contact.html", contact=contact, google_token=google_token, activity="meetings",meetings=meetings, form=form)


def schedule_meeting(form, contact):
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1"
    print(form.date_time_start.data)
    print(form.date_time_end.data)
    start_datetime = form.date_time_start.data.strftime("%Y-%m-%dT%H:%M:%S")
    end_datetime = form.date_time_end.data.strftime("%Y-%m-%dT%H:%M:%S")
    time_zone = session.get("time_zone")
    conference_data = {
        "createRequest": {
            "conferenceSolutionKey": {
                "type": "hangoutsMeet"
            },
            "requestId": str(uuid.uuid4())
        }
    }
    data = {
        "attendees": [{"email": contact.email}, {"email": session.get("user_google")}],
        "sendUpdates": "all",
        "summary": form.title.data,
        "description": form.description.data,
        "start": {"dateTime": start_datetime, "timeZone": time_zone},
        "end": {"dateTime": end_datetime, "timeZone": time_zone},
        "conferenceDataVersion": 1,
        "conferenceData": conference_data
    }
    response = google.post(url, data=data, format="json")
    return response

def get_meetings(contact_email):
    """Function to fetch any email's in the user's google from contact_email OR to contact_email."""
    # The query asks google to return all emails in the user's account TO contact_email OR FROM contact_email.
    query = contact_email
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    # Get all the threads for this google account that match our query.
    response_fetch_meetings = google.get(url, data={"q": query})
    # If the request failed, return the status.
    if response_fetch_meetings.status != 200:
        return response_fetch_meetings.status, None
    return (200, parse_meetings(response_fetch_meetings.data))

def parse_meetings(meetings):
    """Function to parse calendar events / meetings returned by Google's API"""
    meetings_parsed = []
    for item in meetings['items']:
        start_time = item['start'].get('dateTime', '')
        end_time = item['end'].get('dateTime', '')

        # Parse timestamps into datetime objects
        start_datetime = parser.parse(start_time) if start_time else None
        end_datetime = parser.parse(end_time) if end_time else None

        meeting = {
            'summary': item.get('summary', ''),
            'description': item.get('description', ''),
            'starts': start_datetime.strftime('%-H:%M %A, %B %d, %Y') if start_datetime else '',
            'ends': end_datetime.strftime('%-H:%M %A, %B %d, %Y') if end_datetime else '',
            'link': item['conferenceData']['entryPoints'][0]['uri']
        }
        meetings_parsed.append(meeting)
    return meetings_parsed

def tasks_activity(contact_id, google_token, contact, complete="false"):
    form = TaskForm()
    upcoming_tasks, past_due_tasks, completed_tasks = None, None, None
    tasks = None
    if google_token != None:
        if complete != "false":
            complete_task(contact_id, complete)
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            log_activity("complete_task", g.email, timestamp, contact_id)
        task_list = get_task_list(contact)
        if type(task_list) != str:
            return redirect(url_for('authorize_email', contact_id=contact_id))
        if form.validate_on_submit():
            add_task(form, task_list, contact)
            form.title.data = ""
            form.due.data = None
            if task_list == None:
                task_list = get_task_list(contact)
        upcoming_tasks, past_due_tasks, completed_tasks = get_tasks(task_list, contact.contact_id)
        tasks = "Not None"
    # User isn't authenticated, redirect them so they can oAuth their email.
    else:
        return redirect(url_for('authorize_email', contact_id=contact_id))
    # If we can, just update the part of the page that's changed i.e. the activity box.
    if turbo.can_stream():
        return turbo.stream(turbo.update(render_template("contact_interactions.html", contact=contact, google_token=google_token, activity="tasks", form=form, tasks=tasks, upcoming_tasks=upcoming_tasks, past_due_tasks=past_due_tasks, completed_tasks=completed_tasks), 'activity_box'))
    else:
        return render_template("contact.html", contact=contact, google_token=google_token, activity="tasks", form=form, tasks=tasks, upcoming_tasks=upcoming_tasks, past_due_tasks=past_due_tasks, completed_tasks=completed_tasks)

def get_task_list(contact):
    url = "https://tasks.googleapis.com/tasks/v1/users/@me/lists"
    response = google.get(url)
    try:
        for task_list in response.data["items"]:
            try:
                if task_list["title"].split(": ")[1] == contact.email:
                    return task_list["id"]
            except:
                pass
    except:
        return redirect(url_for('authorize_email', contact_id=contact.contact_id))
    return None

def create_task_list(contact):
    url = "https://tasks.googleapis.com/tasks/v1/users/@me/lists"
    # Get all the threads for this google account that match our query.
    response = google.post(url, data={"title": f"Sherpa CRM: {contact.email}"}, format="json")
    return response.data["id"]

def add_task(form, task_list, contact):
    if task_list == None:
        task_list = create_task_list(contact)
    url = f"https://tasks.googleapis.com/tasks/v1/lists/{task_list}/tasks"
    title = form.title.data
    due = form.due.data
    # Need to get rid of timezone info from timestamps.
    gmt = pytz.timezone('GMT')
    due = gmt.localize(due)
    due = due.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    response = google.post(url, data={"title": title, "due": due}, format="json")
    if response.status != 200:
        return redirect(url_for('authorize_email', contact_id=contact.contact_id))
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    log_activity("task", g.email, timestamp, contact.contact_id)

def complete_task(contact_id, task_id):
    form = TaskForm()
    contact = Contacts.query.filter_by(contact_id=contact_id, team_id=g.team_id).first()
    tasks = "Not None"
    google_token = session.get("google_token")
    task_list = get_task_list(contact)
    task = google.get(url=f"https://tasks.googleapis.com/tasks/v1/lists/{task_list}/tasks/{task_id}").data
    response = google.put(url=f"https://tasks.googleapis.com/tasks/v1/lists/{task_list}/tasks/{task_id}", data={"id":task_id, "status": "completed", "title": task["title"], "due": task["due"]}, format="json")
    if response.status != 200:
        return redirect(url_for('authorize_email', contact_id=contact.contact_id))
    upcoming_tasks, past_due_tasks, completed_tasks = get_tasks(task_list, contact_id)
    turbo.push(turbo.replace(render_template("contact_interactions.html", contact=contact, google_token=google_token, activity="tasks", form=form, tasks=tasks, upcoming_tasks=upcoming_tasks, past_due_tasks=past_due_tasks, completed_tasks=completed_tasks), 'activity_box'))
    return '', 205

def get_tasks(task_list, contact_id):
    if task_list == None:
        return None
    url = f"https://tasks.googleapis.com/tasks/v1/lists/{task_list}/tasks"
    try:
        response = google.get(url)
    except:
        return redirect(url_for('authorize_email', contact_id=contact_id))
    tasks_output = []
    try:
        tasks = response.data["items"]
        for task in tasks:
            if "due" in task:
                if task["due"] != "":
                    if "due" in task:
                        task["due"] = parser.parse(task["due"]).strftime("%Y-%m-%d")
            tasks_output.append(task)
    except Exception as e:
        tasks_output = None
    if response.status != 200:
        return redirect(url_for('authorize_email', contact_id=contact_id))
    upcoming_tasks, past_due_tasks, completed_tasks = split_tasks(tasks_output)
    return upcoming_tasks, past_due_tasks, completed_tasks

def split_tasks(tasks):
    upcoming_tasks = []
    past_due_tasks = []
    completed_tasks = []

    for task in tasks:
        if task.get('status') == 'completed':
            completed_tasks.append(task)
        elif task.get('status') == 'needsAction':
            due_date = task.get('due')
            if due_date:
                due_date = datetime.strptime(due_date, '%Y-%m-%d')
                if due_date.date() < datetime.today().date():
                    past_due_tasks.append(task)
                else:
                    upcoming_tasks.append(task)
            else:
                upcoming_tasks.append(task)

    return upcoming_tasks, past_due_tasks, completed_tasks


def notes_activity(contact_id, google_token, contact):
    """Function for the notes activity on the contacts page."""
    response = ""
    notes = Notes.query.filter_by(contact_id=contact_id)
    noteForm = NoteForm()
    if noteForm.validate_on_submit():
        note = Notes()
        note.contact_id = contact_id
        note.note = noteForm.note.data
        note.author = g.email
        # Timestamp the note.
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        note.date = timestamp
        db.session.add(note)
        db.session.commit()
        noteForm.note.data = None
        response = "Note Added"
        
        # Log Activity with log table
        log_activity("note", g.email, timestamp, contact_id)
    # If we can, just update the part of the page that's changed i.e. the activity box.
    if turbo.can_stream():
        return turbo.stream(turbo.update(render_template("contact_interactions.html", notes=notes, google_token=google_token, contact=contact, activity="notes", noteForm=noteForm, response=response), 'activity_box'))
    else:
        return render_template("contact.html", notes=notes, contact=contact, google_token=google_token, activity="notes", noteForm=noteForm)

def email_activity(google_token, form, google_email, contact_id, contact, reply):
        """Function for the email activity on the contacts page."""
        # Make sure user has authorized their google.
        if google_token != None:
            # If the user's submitted a valid email, send the email on their behalf.
            if form.validate_on_submit():
                subject = form.subject.data
                message = form.message.data
                from_email = google_email
                to_email = contact.email
                response = send_email(
                    subject, message, from_email, to_email, reply)
                # If sending the email failed, redirect them so they can oAuth their email.
                if response != 200:
                    return redirect(url_for('authorize_email', contact_id=contact_id))
                reply = None
                form.subject.data = ""
                form.message.data = ""

                # Log activity with log table
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
                log_activity("email", g.email, timestamp, contact_id)
            try:
                # Fetch this user's emails.
                response_status, threads = get_emails(
                    contact.email)
                # If the fetching of the user's emails wasn't successful redirect them to re-authorize their email.
                if response_status != 200:
                    return redirect(url_for('authorize_email', contact_id=contact_id))
            except:
                threads = None
        # User isn't authenticated, redirect them so they can oAuth their email.
        else:
            return redirect(url_for('authorize_email', contact_id=contact_id))
        # If we can, just update the part of the page that's changed i.e. the activity box.
        if turbo.can_stream():
            return turbo.stream(
                turbo.update(render_template("contact_interactions.html", contact=contact, activity="emails",
                                            google_token=google_token, form=form, google_email=google_email, threads=threads, reply=reply), 'activity_box')
            )
        else:
            return render_template("contact.html", contact=contact, activity="emails", google_token=google_token, form=form, google_email=google_email, threads=threads, reply=reply)


def send_email(subject, message, from_email, to_email, reply=None):
    """Function to send an email with an oAuth authenticated google account."""
    message = MIMEText(message)
    message["from"] = from_email
    message["to"] = to_email
    if reply != None:
        # reply[0] is the message_id we wish to reply to.
        message["in-reply-to"] = reply[0]
        # reply[0] is the message_id we wish to reply to.
        message["references"] = reply[0]
        message["message-id"] = reply[0]
        # reply[2] is the subject of the email thread we wish to reply to.
        message["subject"] = reply[2]
    else:
        message["subject"] = subject
    if reply != None:
        message = json.dumps(
            {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode(), "threadId": reply[1]})
    else:
        message = json.dumps(
            {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()})
    url = f"https://gmail.googleapis.com/gmail/v1/users/{from_email}/messages/send"
    response = google.post(url, data=message, format="text")
    return response.status


def get_emails(contact_email):
    """Function to fetch any email's in the user's google from contact_email OR to contact_email."""
    # The query asks google to return all emails in the user's account TO contact_email OR FROM contact_email.
    query = f"from: {contact_email} OR to: {contact_email}"
    user_google = session.get('user_google')
    url = f"https://gmail.googleapis.com/gmail/v1/users/{user_google}/threads"
    # Get all the threads for this google account that match our query.
    response_fetch_threads = google.get(url, data={"q": query})
    # If the request failed, return the status.
    if response_fetch_threads.status != 200:
        return response_fetch_threads.status, None
    threads = []
    # For each thread returned by google.
    for thread in response_fetch_threads.data["threads"]:
        url = f"https://gmail.googleapis.com/gmail/v1/users/{user_google}/threads/{thread['id']}"
        # Fetch all the emails in that thread.
        emails = google.get(url).data
        # Add the parsed emails to the threads list.
        threads.append(parse_thread(emails))
    # Sort the threads by the thread with the most recent reply.
    threads = sorted(threads, key=lambda x: max(
        email["timestamp"] for email in x), reverse=True)
    # Return the response status and the list of email threads.
    return (200, threads)


def parse_thread(thread):
    """Function to parse a thread of emails returned by google's API."""
    emails = []
    # For each email in this thread.
    for message in thread['messages']:
        # Set up a dictionary to represent the email.
        email = {}
        email['subject'] = None
        email['sender_email'] = None
        email['recipient_email'] = None
        email['timestamp'] = None
        email['body'] = None
        email['threadId'] = message['threadId']
        # Map each value to its appropriate header (except body.)
        for header in message['payload']['headers']:
            if header['name'].lower() == 'from':
                email['sender_email'] = header['value']
            elif header['name'].lower() == 'to':
                email['recipient_email'] = header['value']
            elif header['name'].lower() == 'subject':
                email['subject'] = header['value']
            elif header['name'].lower() == 'date':
                # Need to get rid of timezone info from timestamps.
                date_format = "%a, %d %b %Y %H:%M:%S"
                try:
                    email['timestamp'] = datetime.strptime(
                        " ".join(header['value'].split(" ")[0:-1]), date_format)
                except:
                    email['timestamp'] = datetime.strptime(
                        " ".join(header['value'].split(" ")[0:-2]), date_format)
                timestamp=header['value']
                timezone_offset = int(timestamp[-5:-2])
                email['timestamp'] -= timedelta(hours=timezone_offset)
            elif header['name'].lower() == "message-id":
                email['id'] = header['value']
        # Build the body of the email and add to the dict, then append the email to this thread's list.
        email["body"] = build_email_body(message['payload'])
        emails.append(email)
    # Return the list of emails i.e. the now parsed thread.
    return emails


def build_email_body(message):
    """Method to build the body of a google api response by traversing the nested dictionaries in the JSON."""
    # If data is in the body key, we've found the content of the email's body.
    if 'data' in message['body']:
        encoded_body = message['body']['data']
        body = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
        return body
    # Otherwise, traverse to the next level of the nested dictionary.
    else:
        return build_email_body(message["parts"][0])

@contact_bp.route("/reply_email/<message_id>/<thread_id>/<contact_id>/<subject>", methods=["GET", "POST"])
@login_required
@team_required
def reply_email(message_id, thread_id, contact_id, subject):
    reply = message_id + "," + thread_id + "," + subject
    return redirect(url_for('contact_bp.contact', contact_id=contact_id, activity="emails", reply=reply))


@contact_bp.route("/remove_note/<note_id>/<contact_id>", methods=["GET", "POST"])
@login_required
@team_required
def remove_note(note_id, contact_id):
    """This route removes the specified note for the specified contact."""
    # Fetch the note from the db.
    note = Notes.query.filter_by(note_id=note_id).first()
    # Delete the note if it exists.
    if note is not None:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('contact_bp.contact', contact_id=contact_id, activity="notes"))

def log_activity(activity_type, actor, timestamp, contact_id):
    activity = ActivityLog()
    activity.activity_type = activity_type
    activity.actor = actor
    activity.timestamp = timestamp
    activity.contact_id = contact_id

    if activity_type == "note":
        activity.description = f"{actor} created a note on {timestamp}"
    elif activity_type == "email":
        activity.description = f"{actor} sent an email on {timestamp}"
    elif activity_type == "task":
        activity.description = f"{actor} created a task on {timestamp}"
    elif activity_type == "complete_task":
        activity.description = f"{actor} completed a task on {timestamp}"
    else:
        activity.description = f"{actor} scheduled a meeting {timestamp}"

    db.session.add(activity)
    db.session.commit()
    
def view_activity(contact_id, google_token, contact):
    log = ActivityLog.query.filter_by(contact_id=contact_id)

    # Convert the timestamp strings to datetime objects
    log = log.all()
    for entry in log:
        try:
            entry.timestamp = datetime.strptime(entry.timestamp, "%d/%m/%Y %H:%M")
        except:
            pass

    # Sort the log by the datetime objects
    log = sorted(log, key=lambda x: x.timestamp, reverse=True)


    # If we can, just update the part of the page that's changed i.e. the activity box.
    if turbo.can_stream():
        return turbo.stream(turbo.update(render_template("contact_interactions.html", google_token=google_token, contact=contact, activity="activity", log=log), 'activity_box'))
    else:
        return render_template("contact.html", contact=contact, google_token=google_token, activity="activity", log=log)
