# Store locations where users can go to that is unrelated to authentication

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user, login_required
from .models import Note
from . import db
import json

# Saying that we have views split across multiple files
views = Blueprint('views', __name__)  # Setup blueprint for flask app


# URL to get to this endpoint, this will not be accessible until logged in
@views.route('/', methods=['GET', 'POST'])  # Decorator
@login_required
def home():  # This function will run when we go to /
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            # Create a new note
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category="success")

    # In our template, we can pass current user and check to see if it is authenticated
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Take the string of request data coming from javascript, turn it into a python dictionary object, to allow us to access the noteId
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)  # Look for note that has id
    if note:  # Check if note exists
        if note.user_id == current_user.id:  # Check if we own this note
            db.session.delete(note)  # Then delete the note
            db.session.commit()
    return jsonify({})
