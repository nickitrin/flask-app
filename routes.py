from flask import render_template, Blueprint, request, current_app, redirect, url_for, flash
import uuid

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    db = current_app.firestore_db
    stories_ref = db.collection('stories')
    stories = []
    for doc in stories_ref.stream():
        story = doc.to_dict()
        story['id'] = doc.id  # Captura o ID do documento
        stories.append(story)
    
    # Log de depuração
    print("Histórias encontradas:", stories)

    return render_template('index.html', stories=stories)

@main_bp.route('/criarhistoria')
def create():
    db = current_app.firestore_db
    stories_ref = db.collection('stories')
    stories = [doc.to_dict() for doc in stories_ref.stream()]
    return render_template('createstory.html')

@main_bp.route('/add_story', methods=['POST'])
def add_story():
    db = current_app.firestore_db
    title = request.form.get('title')
    content = request.form.get('content')
    story_data = {
        'title': title,
        'content': content
    }
    db.collection('stories').add(story_data)
    return redirect(url_for('main.index'))

@main_bp.route('/story/<story_id>')
def story(story_id):
    db = current_app.firestore_db
    story_ref = db.collection('stories').document(story_id)
    story = story_ref.get().to_dict()
    if story is None:
        return "Story not found", 404

    print("História encontrada:", story)

    return render_template('story.html', story=story)