from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import re

app = Flask(__name__)

# Represents the list of tasks to be shown on the View interface
to_do_list = []

# Stores error messages, but empty when no errors present
status = ""


class Task:
    """An object which aggregates the task, it's associated email and the
     associated priority level into one piece. This is convenient so that
     each (row on the table) entry on the list can be represented by a single
     object."""

    def __init__(self, task, owner, priority):
        """Initializes the common variables for each task: the task itself,
        the owner, and the priority level."""
        self.task = task
        self.owner = owner
        self.priority = priority


@app.route('/')
def display():
    """Graphical interface that displays the to do list and allows users
    to add to it. Interface is also known as the view in the MVC pattern.
    The status variable will display any errors that come about."""

    return render_template('display.html', to_do_list=to_do_list,
                           status=status)


@app.route('/submit', methods=['POST'])
def submit():
    """Gathers information from the View interface and validates if appropriate
     information was selected for the task, e-mail, and priority. If validation
     of any of the three pieces of information fails then the status global
     variable will be changed accordingly to reflect the error the user needs
     to fix. No task will be added to the to do list. Tasks will only be added
     if all the validation tests pass. Task validations checks if there is any
     information typed into the text box. E-mail validation checks if the e-mail
     follows a the proper syntax format against a regular expression string.
     Priority validation checks if the user has correctly selected High, Medium,
     or Low."""

    global status
    task = request.form['task']
    owner = request.form['email']
    priority = request.form['priority']

    if task == "":
        status = "Error: You must enter a task."
        return redirect("/")
    else:
        status = ""

    # E-mail addresses will be checked against this regular expression that
    # accounts for any number of characters being chosen for the username that
    # exists prior to the @ sign with the exception of the @ sign itself, fol-
    # lowed by exactly one @ sign, then any alphanumeric characters following
    # it as the beginning of the domain name. Hyphens are then possible in
    # the domain name if they are surrounded by alphanumeric characters.
    # Hyphens are allowed to be next to one another. There is a required .
    # character which represents subdomains or the top-level domain. This is
    # for email addresses that may contain this such as pabejar@yahoo.com.ph
    # or patrick.abejar@spsmail.cuny.edu. An unlimited number of these .
    # characters can be placed after the @ sign in the e-mail address as long
    # as it is not the leading or last character after the @ sign. E-mail
    # addresses may also be represented with IP addresses by this regex.
    pattern = "^[^@]+[@]{1}[a-zA-Z0-9]+([\-]+[a-zA-Z0-9]+)*([\.]{1}[a-zA-Z" \
              "0-9]+([\-]+[a-zA-Z0-9]+)*)+"

    if not re.search(pattern, owner):
        status = "Error: There was a problem adding the task. Try entering" \
                 " a valid e-mail."
        return redirect("/")
    else:
        status = ""

    if priority != "High" and priority != "Medium" and priority != "Low":
        status = "Error: There was a problem adding the task. Please select" \
                 " a priority."
        return redirect("/")
    else:
        status = ""

    t = Task(task, owner, priority)
    to_do_list.append(t)

    return redirect("/")


@app.route('/clear', methods=['POST'])
def clear():
    """Clears the entire to do list."""

    del to_do_list[:]
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():
    """Deletes one task/row at a time from the to do list. It does so by
    retrieving what index was stored as a hidden <input> based on jinja's
    loop.index0 variable. One iteration of the for loop in the View int-
    erface represents one row. The index labels are sequential starting
    from zero. These are attached to the same form as a button that is lab-
    eled delete, which will be passed to this control, /delete. This will
    then delete that corresponding index from the to do list here."""

    delete_index = int(request.form['index'])
    del to_do_list[delete_index]
    return redirect("/")

if __name__ == "__main__":

    # RUNS ON PORT 5000 ON 127.0.0.1, SINCE PORT 80 REQUIRES SUDO
    app.run()
