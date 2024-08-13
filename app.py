
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/photos'
app.config['UPLOADED_VIDEOS_DEST'] = 'uploads/videos'
db = SQLAlchemy(app)

photos = UploadSet('photos', IMAGES)
videos = UploadSet('videos')
configure_uploads(app, (photos, videos))
patch_request_class(app)  # Limits upload size

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(200))
    video_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username})

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.form
    post = Post(content=data['content'], user_id=data['user_id'])
    if 'image' in request.files:
        post.image_url = photos.url(request.files['image'].filename)
    if 'video' in request.files:
        post.video_url = videos.url(request.files['video'].filename)
    db.session.add(post)
    db.session.commit()
    return jsonify({'id': post.id})

@app.route('/uploads/photos/<filename>')
def uploaded_photos(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/uploads/videos/<filename>')
def uploaded_videos(filename):
    return send_from_directory(app.config['UPLOADED_VIDEOS_DEST'], filename)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
