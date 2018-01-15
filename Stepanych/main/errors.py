from flask import render_template
from . import main

@main.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@main.app_errorhandler(400)
def not_found(error):
    return render_template('400.html'), 400

@main.app_errorhandler(401)
def not_found(error):
    return render_template('401.html'), 401

@main.app_errorhandler(403)
def not_found(error):
    return render_template('403.html'), 403   

@main.app_errorhandler(405)
def not_found(error):
    return render_template('405.html'), 405       

@main.app_errorhandler(500)
def not_found(error):
    return render_template('500.html'), 500    

  