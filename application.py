from flask import Flask, redirect, url_for, render_template, json, jsonify, Response, make_response
from flask_mongoengine import MongoEngine
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


db = MongoEngine()
def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)

    db.init_app(app)
    GoogleMaps(app, key="AIzaSyCRQzAIwUhY_dp-FhBEdtxzNZQ2m0_zvdQ")

    from user.views import user_page
    app.register_blueprint(user_page, url_prefix="/user")

    from study.views import study_page
    app.register_blueprint(study_page, url_prefix="/study")


    @app.route('/')
    def home():
        return redirect(url_for('study_page.search'))

    from study.models import Study
    @app.route("/map")
    def map():

        studies = Study.objects
        data = []
        for study in studies:
            data.append({'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lng': study.location["coordinates"][0],
            'lat': study.location["coordinates"][1],
            'infobox': f"<img width=100px height=100px src='{study.study_photo}'/>" })
        # creating a map in the view
        # print(data)
        sndmap = Map(
            identifier="sndmap",
            lat=30.2880433,
            lng=-97.7308176,
            markers= data,
            style="height:80%;width:100%;",
            zoom=12
        )
        return render_template('map.html', sndmap=sndmap,data=data)

    @app.route('/json/studies')
    def studies_json():
        studies = Study.objects
        return jsonify(studies)

    from study.models import Theme
    @app.route('/json/themes')
    def themes_json():
        themes = Theme.objects
        return jsonify(themes)

    from user.models import User
    @app.route('/json/users')
    def users_json():
        users = User.objects
        return jsonify(users)
    return app
