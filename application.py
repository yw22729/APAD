from flask import Flask, redirect, url_for, render_template
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
    @app.route("/map1")
    def mapview():

        studies = Study.objects
        data = []
        for study in studies:
            data.append({'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 
            'lng': study.location["coordinates"][0], 
            'lat': study.location["coordinates"][1], 
            'infobox': f"<img width=100% height=100% src='{study.study_photo}'/>" })
        # creating a map in the view
        print(data)
        mymap = Map(
            identifier="view-side",
            lat=37.4419,
            lng=-122.1419,
            markers=[(37.4419, -122.1419), (37.4300, -122.1400)]
        )
        sndmap = Map(
            identifier="sndmap",
            lat=30.2880433,
            lng=-97.7308176,
            markers= data

            # , {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat': -97.7430608, 'lng': 30.267153, 'infobox': '<b>Hello World</b>'}, {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat': -96.67055030000002, 'lng': 33.1031744, 'infobox': '<b>Hello World</b>'}, {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat': -97.6779842, 'lng': 30.6332618, 'infobox': '<b>Hello World</b>'}, {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat': -98.1244531, 'lng': 29.7030024, 'infobox': '<b>Hello World</b>'}]
            
            
            
            
            # [
            # {
            #     'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            #     'lat': 37.4419,
            #     'lng': -122.1419,
            #     'infobox': "<b>Hello World</b>"
            # },
            # {
            #     'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            #     'lat': 37.4300,
            #     'lng': -122.1400,
            #     'infobox': "<b>Hello World from other place</b>"
            # }
            # ]
        )
        return render_template('example.html', mymap=mymap, sndmap=sndmap,data=data)
    return app
