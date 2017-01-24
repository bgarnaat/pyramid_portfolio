"""."""
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from sqlalchemy.exc import DBAPIError

from pyramid_portfolio.security import check_credentials
from pyramid_portfolio.models import Image, Project
import mimetypes


@view_config(route_name='home',
             renderer='../templates/home.jinja2')
def view_home(request):
    """Portfolio home view."""
    try:
        query = request.dbsession.query(Project).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'projects': query}


@view_config(route_name='detail',
             renderer='../templates/detail.jinja2')
def view_detail(request):
    """Show details project."""
    try:
        project_id = int(request.matchdict['id'])
        project = request.dbsession.query(Project).get(project_id)
        if not project:
            return Response("Project Not Found", content_type='text/plain', status=404)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'project': project}


@view_config(route_name='create',
             renderer='../templates/create.jinja2',
             permission='admin')
def view_create(request):
    """Create new project record."""
    if request.method == 'POST':
        project = Project(
            title=request.POST['title'],
            description=request.POST['description'],
            repository=request.POST['repository'],
            website=request.POST['website'],
        )
        if request.POST['image'] is not b'':
            image = Image(
                name=request.POST['image'].filename,
                data=request.POST['image'].file.read()
            )
            request.dbsession.add(image)
            request.dbsession.query(Image).all()

            project.image_id = image.id

        request.dbsession.add(project)
        request.dbsession.query(Project).all()
        return HTTPFound(request.route_url('detail', id=project.id))
    return {}


@view_config(route_name='edit',
             renderer='../templates/edit.jinja2',
             permission='admin')
def view_edit(request):
    """Edit specific project record."""
    project_id = int(request.matchdict['id'])
    project = request.dbsession.query(Project).get(project_id)
    if request.method == 'POST':
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.repository = request.POST['repository']
        project.website = request.POST['website']

        if request.POST['image'] is not b'':
            """Update existing image or create new image record if none exists."""
            if project.image_id is not None:
                image = request.dbsession.query(Image).get(project.image_id)
                image.name = request.POST['image'].filename
                image.data = request.POST['image'].file.read()
            else:
                image = Image(
                    name=request.POST['image'].filename,
                    data=request.POST['image'].file.read()
                )
                request.dbsession.add(image)
                request.dbsession.query(Image).all()
                project.image_id = image.id

        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=request.matchdict['id']))
    return {'project': project}


@view_config(route_name='delete',
             permission='admin')
def view_delete(request):
    """Delete specific project record."""
    # if request.POST:
    project_id = int(request.matchdict['id'])
    project = request.dbsession.query(Project).get(project_id)
    if project.image_id:
        image_id = project.image_id
        image = request.dbsession.query(Image).get(image_id)
        request.dbsession.delete(image)
    request.dbsession.delete(project)
    return HTTPFound(request.route_url('home'))


@view_config(route_name='login',
             renderer='../templates/login.jinja2',
             require_csrf=False)
def view_login(request):
    """Authenticate user."""
    if request.POST:
        if check_credentials(request.POST['username'], request.POST['password']):
            auth_header = remember(request, request.POST['username'])
            return HTTPFound(request.route_url('home'), headers=auth_header)
    return {}


@view_config(route_name='logout')
def view_logout(request):
    """Remove authentication from user and return to home."""
    auth_header = forget(request)
    return HTTPFound(request.route_url('home'), headers=auth_header)


@view_config(route_name='api_get_project_all')
def api_get_project_all(request):
    """Return list of projects as JSON."""
    projects = request.dbsession.query(Project).all()
    return [project.to_json() for project in projects]


@view_config(route_name='api_get_project_by_id')
def api_get_project_by_id(request):
    """Return requestsed project as JSON."""
    project_id = int(request.match['id'])
    project = request.dbsession.query(Project).get(project_id)
    return project.to_json()


@view_config(route_name='image')
def view_image(request):
    """Return image from database."""
    image_id = int(request.matchdict['id'])
    image = request.dbsession.query(Image).get(image_id)
    image_type = mimetypes.guess_type(image.name)[0]
    return Response(content_type=image_type, body=image.data)


db_err_msg = """\
|-o-|  |-o-|  |-o-|  |-o-|  <-o->  |-o-|  |-o-|  |-o-|  |-o-|\n
\n
This database has been commandeered by the empire.\n
\n
|-o-|  |-o-|  |-o-|  |-o-|  |-o-|  |-o-|  |-o-|  |-o-|  |-o-|
"""
