from flask import Flask, redirect, url_for, render_template, json, jsonify, Response, make_response
from flask_mongoengine import MongoEngine
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import bcrypt
from flask import request


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

    @app.route('/json/themes/<name>')
    def studies_in_theme(name):
        studies = Study.objects.filter(theme=name,cancel=False)
        return jsonify(studies)

    from user.models import User
    @app.route('/json/users')
    def users_json():
        users = User.objects
        return jsonify(users)

    @app.route('/json/user_themes/<email>')
    def users_themes(email):
        user = User.objects.filter(email=email.lower()).first()
        themes = Theme.objects.filter(subscribers=user.id)
        return jsonify(themes)

    @app.route('/json/user_studies/<email>')
    def users_studies(email):
        user = User.objects.filter(email=email.lower()).first()
        studies = Study.objects.filter(host=user.id).order_by('-start_datetime')
        return jsonify(studies)

    @app.route('/json/user_login/<email>/<password>')
    def user_login(email, password):
        user = User.objects.filter(email=email.lower()).first()
        if user:
            if bcrypt.checkpw(password, user.password):
                result = [{"result":"true"}]
            else:
                result = [{"result":"false"}]
        else:
            result = [{"result":"false"}]
        return jsonify(result)

    from datetime import datetime
    from dateutil import parser
    @app.route('/json/create', methods=['GET', 'POST'])
    def user_create():

        result = request.args.to_dict(flat=False)
        print(request.args)
        print(request.args.getlist('location'))
        email = result['email'][0]
        name = result['name'][0]
        location = [float(i) for i in request.args.getlist('location')]
        place = result['place'][0]
        theme = result['theme'][0]
        description=result["description"][0]
        tag=result['tag'][0]
        startTime = parser.parse(result["start_time"][0])
        print(startTime)
        start_time=startTime
        endTime = parser.parse(result["start_time"][0])
        end_time=endTime
        image_url=result["image_url"][0]

        try:
            user = User.objects.filter(email=email).first()
            print(user)
            study = Study(
                name=name,
                place=place,
                location=location,
                theme = theme,
                start_datetime=start_time,
                end_datetime=end_time,
                description=description,
                host=user.id,
                attendees=[user],
                tag = tag.split(", ")
            )
            print(study)
            study.save()


            # image_url = upload_image_file(request.files.get('photo'), 'study_photo', str(study.id))
            if image_url:
                study.study_photo = image_url
            study.save()
            return "true"
        except Exception as inst:
            print("has error")
            return str(inst)


    return app
