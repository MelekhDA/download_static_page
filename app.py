import os

import pickle
from flask import (
    Flask, request, jsonify, send_file
)
from flask_sqlalchemy import SQLAlchemy

from settings import STATUS_ARCHIVE_READY

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import SitePage


@app.route('/archive', methods=['POST'])
def create_archive():
    """API for save request by url"""

    url = request.json.get('url')

    if url is None:
        return jsonify({'error': 'not found url'}), 400

    site_page = SitePage(url=url)
    db.session.add(site_page)
    db.session.commit()

    return jsonify({'success': 'url is being processed', 'id': site_page.id})


@app.route('/archive/<int:id_archive>/', methods=['GET'])
def get_archive(id_archive):
    """API for issuing an archive on an existing request"""

    site_page = SitePage.query.get(id_archive)

    if site_page is None:
        return (
            f'Sorry, no archive (id={id_archive}) was found for this request.',
            400
        )

    if site_page.status != STATUS_ARCHIVE_READY:
        return (
            f'Please wait, your request '
            f'(at the address {site_page.url}) is being processed',
            400
        )

    try:
        load_zipfile = pickle.loads(site_page.zipfile)
    except pickle.UnpicklingError:
        return (
            f'Sorry, there was an error preparing the archive.',
            400
        )

    return send_file(
        load_zipfile,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=f'archive_{site_page.id}.zip'
    )


@app.errorhandler(404)
def page_not_found(error):
    """Default page for 404 status"""

    return "Oops. This route is not found", 404


@app.errorhandler(500)
def page_not_found(error):
    """Default page for 500 status"""

    return "An error occurred on the server side. " \
           "We already know about it, the site " \
           "will be restored soon. Thanks.", 500


if __name__ == '__main__':
    app.run()
