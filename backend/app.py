from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

tags_r = db.Table(
    'tags_relationship',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id')),
    db.Column('note_id', db.Integer, db.ForeignKey('note.note_id')),
)


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=True)
    is_note = db.Column(db.Boolean, default=False)
    is_complete = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', secondary=tags_r, backref=db.backref('notes', lazy='dynamic'))


@app.route('/get/tags/', methods=['GET'])
def get_all_tags():
    tags = Tag.query.all()
    return jsonify([{'id': tag.tag_id, 'name': tag.name} for tag in tags])


@app.route('/get/tag/<int:tag_id>/', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return jsonify({'id': tag.tag_id, 'name': tag.name})


@app.route('/create/tag/', methods=['POST'])
def create_tag():
    if request.method == 'POST':
        req = request.form
        tag = Tag(
            name=req['name']
        )
        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)

        responce = {
            'id': tag.tag_id,
            'name': tag.name
        }
        return jsonify(responce)
    abort(404)


@app.route('/edit/tag/<int:tag_id>/', methods=['POST'])
def edit_tag(tag_id):
    if request.method == 'POST':
        req = request.form
        tag = Tag.query.get(tag_id)
        tag.name = req['name']
        db.session.commit()
        return jsonify({'success': True})
    abort(404)


@app.route('/delete/tag/<int:tag_id>/', methods=['DELETE'])
def delete_tag(tag_id):
    if request.method == 'DELETE':
        tag = Tag.query.get(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return jsonify({'success': True})
    abort(404)


@app.route('/get/notes/', methods=['GET'])
def get_all_notes():
    notes = Note.query.all()
    notes = [{
        'id': note.note_id,
        'name': note.name,
        'date': note.due_date,
        'is_note': note.is_note,
        'completed': note.is_complete,
        'tags': [{'id': tag.tag_id, 'name': tag.name} for tag in note.tags]
    } for note in notes]
    return jsonify(notes)


@app.route('/get/note/<int:note_id>/', methods=['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)
    note = {
        'id': note.note_id,
        'name': note.name,
        'date': note.due_date,
        'is_note': note.is_note,
        'completed': note.is_complete,
        'tags': [{'id': tag.tag_id, 'name': tag.name} for tag in note.tags]
    }
    return jsonify(note)


@app.route('/create/note/', methods=['POST'])
def create_note():
    if request.method == 'POST':
        req = request.form
        note = Note(
            name=req['name'],
        )
        if req.get('date'):
            dt = datetime.datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S')
            note.due_date = dt
        if req.get('is_note'):
            note.is_note = True if req['is_note'] == 'true' else False
        if req.get('completed'):
            note.is_complete = True if req['completed'] == 'true' else False
        db.session.add(note)
        db.session.commit()
        db.session.flush()

        responce = {
            'id': note.note_id,
            'name': note.name,
            'date': note.due_date,
            'is_note': note.is_note,
            'completed': note.is_complete,
            'tags': [{'id': tag.tag_id, 'name': tag.name} for tag in note.tags]
        }
        return jsonify(responce)
    abort(404)


@app.route('/edit/note/<int:note_id>/', methods=['POST'])
def edit_note(note_id):
    if request.method == 'POST':
        req = request.form
        note = Note.query.get(note_id)
        if req.get('name'):
            note.name = req['name']
        if req.get('description'):
            note.description = req['description']
        if req.get('date'):
            dt = datetime.datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S')
            note.due_date = dt
        if req.get('is_note'):
            note.is_note = True if req['is_note'] == 'true' else False
        if req.get('completed'):
            note.is_complete = True if req['completed'] == 'true' else False
        db.session.commit()
        return jsonify({'success': True})
    abort(404)


@app.route('/delete/note/<int:note_id>/', methods=['DELETE'])
def delete_note(note_id):
    if request.method == 'DELETE':
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    abort(404)


@app.route('/addtag/', methods=['POST'])
def add_tag_to_note():
    if request.method == 'POST':
        req = request.form
        note = Note.query.get(req['note_id'])
        tag = Tag.query.get(req['tag_id'])
        note.tags.append(tag)
        db.session.commit()
        return jsonify({'success': True})
    abort(404)


@app.route('/removetag/', methods=['POST'])
def remove_tag_from_note():
    if request.method == 'POST':
        req = request.form
        note = Note.query.get(req['note_id'])
        note.tags = [tag for tag in note.tags if tag.tag_id != int(req['tag_id'])]
        db.session.commit()
        return jsonify({'success': True})
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)
