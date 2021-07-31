from flask import Flask, redirect, url_for
from flask_mongoengine import MongoEngine

db = MongoEngine()
def create_app(config=None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_object(config)
     
    db.init_app(app)
    
    from user.views import user_page
    app.register_blueprint(user_page, url_prefix="/user")

    from study.views import study_page
    app.register_blueprint(study_page, url_prefix="/study")
    
    @app.route('/')
    def home():
        return redirect(url_for('study_page.explore'))
    
    return app