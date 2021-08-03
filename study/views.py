from flask import Blueprint, render_template, request, session, redirect, url_for, abort
import bson
from study.forms import BasicStudyForm, EditStudyForm, CancelStudyForm, ThemesForm, EditThemeForm
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
    themes = Theme.objects
    form.theme.choices = [theme.name for theme in themes]
    if request.method == 'POST' and form.validate():
        if form.end_datetime.data < form.start_datetime.data:
            error = "A study must end after it starts!"
        if not error:
            user = User.objects.filter(email=session.get('email')).first()
            # tag = Tag.objects.filter(name=form.tag.data).first()
            study = Study(
                name=form.name.data,
                place=form.place.data,
                location=[form.lng.data, form.lat.data],
                theme = form.theme.data,
                start_datetime=form.start_datetime.data,
                end_datetime=form.end_datetime.data,
                description=form.description.data,
                host=user.id,
                attendees=[user],
                tag = form.tag.data.split(", ")
            )
            study.save()
            return redirect(url_for('study_page.edit', id=study.id))
    return render_template('study/create.html', form=form)

@study_page.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    try:
        study = Study.objects.filter(id=bson.ObjectId(id)).first()
        study.tag = ", ".join(study.tag)
    except bson.errors.InvalidId:
        abort(404)

    user = User.objects.filter(email=session.get('email')).first()

    if study and study.host == user.id:
        error = None
        message = None
        form = EditStudyForm(obj=study)
        themes = Theme.objects
        form.theme.choices = [theme.name for theme in themes]
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
                if study.tag:
                    tags = form.tag.data.split(", ")
                    study.tag = tags
                study.save()
                message = 'Study updated'
        return render_template('study/edit.html', form=form, error=error,
                              message=message, study=study)
    else:
        abort(404)

@study_page.route('/<id>/edit_theme', methods=['GET', 'POST'])
@login_required
def edit_theme(id):
    try:
        theme = Theme.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    user = User.objects.filter(email=session.get('email')).first()

    if theme:
        error = None
        message = None
        form = EditThemeForm(obj=theme)

        if request.method == 'POST' and form.validate():
            if not error:
                form.populate_obj(theme)
                image_url = upload_image_file(request.files.get('photo'), 'theme_photo', str(theme.id))
                if image_url:
                    theme.theme_photo = image_url

                theme.save()
                message = 'Theme updated'
        return render_template('study/edit_theme.html', form=form, error=error,
                              message=message, theme=theme)
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
        # tag = Tag.objects.filter(id=study.tag).first()
        return render_template('study/public.html', study=study, host=host, user=user)
    else:
        abort(404)

@study_page.route('/themes/<id>', methods=['GET'])
def public_theme(id):
    try:
        theme = Theme.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    if theme:
        user = User.objects.filter(email=session.get('email')).first()
        return render_template('study/public_theme.html', theme=theme, user=user)
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

@study_page.route('/<id>/join_theme', methods=['GET'])
@login_required
def join_theme(id):
    user = User.objects.filter(email=session.get('email')).first()
    try:
        theme = Theme.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    if user and theme:
        if user not in theme.subscribers:
            theme.subscribers.append(user)
            theme.save()
        return redirect(url_for('study_page.manage_theme', id=id))
    else:
        abort(404)


@study_page.route('/<id>/leave_theme', methods=['GET'])
@login_required
def leave_theme(id):
    user = User.objects.filter(email=session.get('email')).first()
    try:
        theme = Theme.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)

    if user and theme:
        if user in theme.subscribers:
            theme.subscribers.remove(user)
            theme.save()
        return redirect(url_for('study_page.manage_theme', id=id))
    else:
        abort(404)

@study_page.route('/manage/<int:study_page_number>', methods=['GET'])
@study_page.route('/manage', methods=['GET'])
@login_required
def manage(study_page_number=1):
    user = User.objects.filter(email=session.get('email')).first()
    if user:
        studies = Study.objects.filter(host=user.id).order_by('-start_datetime').paginate(page=study_page_number, per_page=30)
        themes = Theme.objects.filter(subscribers=user.id).paginate(page=study_page_number, per_page=30)
        # tags = []
        # for study in studies.items:
        #     tag_id = study.tag
        #     tag = Tag.objects.filter(id=bson.ObjectId(tag_id)).first()
        #     tags.append(tag.name)
        return render_template('study/manage.html', studies=studies, themes = themes, user = user)
    else:
        abort(404)

@study_page.route('/manage/<int:study_page_number>', methods=['GET'])
@study_page.route('/manage_themes', methods=['GET'])
@login_required
def manage_theme(study_page_number=1):
    user = User.objects.filter(email=session.get('email')).first()
    if user:
        themes = Theme.objects.filter().paginate(page=study_page_number, per_page=30)
        return render_template('study/manage_themes.html', themes=themes, user=user)
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

@study_page.route('/create_themes', methods=['GET', 'POST'])
@login_required
def create_themes():
    form = ThemesForm()
    error = None
    if request.method == 'POST' and form.validate():
        if Theme.objects.filter(name=form.name.data).first():
            error = "The tag already exists!"
        if not error:
            user = User.objects.filter(email=session.get('email')).first()
            theme = Theme(
                name=form.name.data,
                description=form.description.data,
                subscribers=[user.id]
            )
            theme.save()
            message = 'Theme created'
            return redirect(url_for('study_page.manage_theme',message=message))
    return render_template('study/create_themes.html', form=form, error=error)

@study_page.route('/search/<int:study_page_number>', methods=['GET'])
@study_page.route('/search', methods=['GET'])
def search(study_page_number=1):
    tag_name = request.args.get('tag')
    try:
        # tag = Study.objects.filter(tag=tag_name).first()
        studies = Study.objects.filter(tag=tag_name,
                                       cancel=False).order_by('-start_datetime').paginate(page=study_page_number, per_page=4)

        return render_template('study/search.html', studies=studies, tag=tag_name)
    except:
        return render_template('study/search.html', tag=tag_name)
