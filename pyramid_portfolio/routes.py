"""Configuration of app routes."""


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # HTML Routes:
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('create', '/project/create')
    config.add_route('detail', '/project/{id:\d+}')
    config.add_route('edit', '/project/{id:\d+}/edit')
    config.add_route('delete', '/project/{id:\d+}/delete')
    # API Routes:
    config.add_route('api_get_project_all', '/api/project/all')
    config.add_route('api_get_project_by_id', '/api/project/{id:\d+}')
