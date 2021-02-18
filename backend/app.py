from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return '<Tag %r>' % (self.name)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Note %r>' % (self.name)


@app.route('/create/tag/', methods=['POST'])
def create_tag():
    req = request.get_json(force=True)
    tag = Tag(
        name=req['name']
    )
    db.session.add(tag)
    db.session.commit()
    db.session.flush()

    responce = {
        'id': tag.id,
        'name': tag.name
    }
    return jsonify(responce)


@app.route('/edit/tag/<int:tag_id>/', methods=['POST'])
def edit_tag(tag_id):
    req = request.get_json(force=True)
    tag = Tag.query.get(tag_id)
    tag.name = req['name']
    db.session.commit()
    return jsonify({'success': True})


@app.route('/edit/tag/<int:tag_id>/')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/create/note/', methods=['POST'])
def create_note():
    req = request.get_json(force=True)
    note = Note(
        name=req['name'],
        description=req['description']
    )
    db.session.add(note)
    db.session.commit()
    db.session.flush()

    responce = {
        'id': note.id,
        'name': note.name,
        'description': note.description,
    }
    return jsonify(responce)


@app.route('/edit/note/<int:note_id>/', methods=['POST'])
def edit_note(note_id):
    req = request.get_json(force=True)
    note = Note.query.get(note_id)
    note.name = req['name']
    note.description = req['description']
    db.session.commit()
    return jsonify({'success': True})


@app.route('/edit/note/<int:note_id>/')
def delete_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
