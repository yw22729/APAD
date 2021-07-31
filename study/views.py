from flask import Blueprint, render_template, request, session, redirect, url_for, abort
import bson


from study.forms import BasicStudyForm, EditStudyForm, CancelStudyForm
from user.decorators import login_required
from study.models import Study, Theme
from user.models import User
from utilities.storage import upload_image_file

study_page = Blueprint('study_page', __name__)

@study_page.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BasicStudyForm()
    error = None
    if request.method == 'POST' and form.validate():
        if form.end_datetime.data < form.start_datetime.data:
            error = "A study must end after it starts!"
        if not error:
            user = User.objects.filter(email=session.get('email')).first()

            study = Study(
                name=form.name.data,
                place=form.place.data,
                theme = form.theme.data,
                location=[form.lng.data, form.lat.data],
                start_datetime=form.start_datetime.data,
                end_datetime=form.end_datetime.data,
                description=form.description.data,
                host=user.id,
                attendees=[user]
            )
            study.save()
            tag = Tag(
                name=form.tag.data
            )
            tag.save()
            return redirect(url_for('study_page.edit', id=study.id, tag_id=tag.id))
    return render_template('study/create.html', form=form)

@study_page.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id,tag_id):
    try:
        study = Study.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    user = User.objects.filter(email=session.get('email')).first()
    tag = Tag.objects.filter(id=bson.ObjectId(tag_id)).first()

    if study and study.host == user.id:
        error = None
        message = None
        form = EditStudyForm(obj=study)
        if request.method == 'POST' and form.validate():
            if form.end_datetime.data < form.start_datetime.data:
                error = 'A study must end after it starts!'
            if not error:
                form.populate_obj(study)
                if form.lng.data and form.lat.data:
                    study.location = [form.lng.data, form.lat.data]
                image_url = upload_image_file(request.files.get('photo'), 'study_photo', str(study.id))
                if image_url:
                    study.study_photo = image_url
                study.save()
                message = 'Study updated'
        return render_template('study/edit.html', form=form, error=error,
                              message=message, study=study)
    else:
        abort(404)

@study_page.route('/<id>/cancel', methods=['GET', 'POST'])
@login_required
def cancel(id):
    try:
        study = Study.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)
    user = User.objects.filter(email=session.get('email')).first()

    if study and study.host == user.id and study.cancel == False:
        error = None
        form = CancelStudyForm()
        if request.method == 'POST' and form.validate():
            if form.confirm.data == 'yes':
                study.cancel = True
                study.save()
                return redirect(url_for('study_page.edit', id=study.id))
            else:
                error = 'Say yes if you want to cancel'
        return render_template('study/cancel.html', form=form, error=error, study=study)
    else:
        abort(404)

@study_page.route('/<id>', methods=['GET'])
def public(id):
    try:
        study = Study.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    if study:
        host = User.objects.filter(id=study.host).first()
        user = User.objects.filter(email=session.get('email')).first()
        return render_template('study/public.html', study=study, host=host, user=user)
    else:
        abort(404)

@study_page.route('/<id>/join', methods=['GET'])
@login_required
def join(id):
    user = User.objects.filter(email=session.get('email')).first()
    try:
        study = Study.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    if user and study:
        if user not in study.attendees:
            study.attendees.append(user)
            study.save()
        return redirect(url_for('study_page.public', id=id))
    else:
        abort(404)

@study_page.route('/<id>/leave', methods=['GET'])
@login_required
def leave(id):
    user = User.objects.filter(email=session.get('email')).first()
    try:
        study = Study.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    if user and study:
        if user in study.attendees:
            study.attendees.remove(user)
            study.save()
        return redirect(url_for('study_page.public', id=id))
    else:
        abort(404)

@study_page.route('/manage/<int:study_page_number>', methods=['GET'])
@study_page.route('/manage', methods=['GET'])
@login_required
def manage(study_page_number=1):
    user = User.objects.filter(email=session.get('email')).first()
    if user:
        studies = Study.objects.filter(host=user.id).order_by('-start_datetime').paginate(page=study_page_number, per_page=4)
        return render_template('study/manage.html', studies=studies)
    else:
        abort(404)

@study_page.route('/explore/<int:study_page_number>', methods=['GET'])
@study_page.route('/explore', methods=['GET'])
def explore(study_page_number=1):
    place = request.args.get('place')
    try:
        lng = float(request.args.get('lng'))
        lat = float(request.args.get('lat'))
        studies = Study.objects(location__near=[lng, lat], location__max_distance=10000,
                               cancel=False).order_by('-start_datetime').paginate(page=study_page_number, per_page=4)
        return render_template('study/explore.html', studies=studies, place=place, lng=lng, lat=lat)
    except:
        return render_template('study/explore.html', place=place)
