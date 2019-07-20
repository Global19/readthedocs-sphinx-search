import os

from sphinx.errors import ExtensionError
from sphinx.util.fileutil import copy_asset


ASSETS_FILES = {
    'minified': [
        os.path.join('js', 'rtd_sphinx_search.min.js'),
        os.path.join('css', 'rtd_sphinx_search.min.css'),
    ],
    'un-minified': [
        os.path.join('js', 'rtd_sphinx_search.js'),
        os.path.join('css', 'rtd_sphinx_search.css'),
    ]
}

ONLINE_BUILDERS = [
    'readthedocs',
    'readthedocsdirhtml',
    'readthedocssinglehtml',
]


def copy_asset_files(app, exception):
    if exception is None:  # build succeeded
        files = ASSETS_FILES['minified'] + ASSETS_FILES['un-minified']
        for file in files:
            path = os.path.join(os.path.dirname(__file__), 'static', file)
            copy_asset(path, os.path.join(app.outdir, '_static', file.split('.')[-1]))


def inject_static_files(app):
    """
    Inject correct CSS and JS files based on the value of ``RTD_SPHINX_SEARCH_FILE_TYPE``.

    This only injects file if the docs are build on Read the Docs.
    """

    on_rtd = os.environ.get('READTHEDOCS') == 'True'

    # only inject files if the builder is one of the ONLINE_BUILDERS
    # and on_rtd is True
    if app.builder.name not in ONLINE_BUILDERS and not on_rtd:
        return

    file_type = app.config.rtd_sphinx_search_file_type
    expected_file_type = ASSETS_FILES.keys()

    if file_type not in expected_file_type:
        raise ExtensionError(f'"{file_type}" file type is not supported')

    files = ASSETS_FILES[file_type]

    for file in files:
        if file.endswith('.js'):
            app.add_js_file(file)
        elif file.endswith('.css'):
            app.add_css_file(file)


def setup(app):

    app.add_config_value('rtd_sphinx_search_file_type', 'minified', 'html')

    app.connect('builder-inited', inject_static_files)
    app.connect('build-finished', copy_asset_files)
