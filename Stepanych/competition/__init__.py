from flask import Blueprint
competition = Blueprint('competition', __name__)
from . import routes, results, allteams, competitionAdmin, registredTeams
