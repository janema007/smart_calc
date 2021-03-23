from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__,
    instance_relative_config=False,
    template_folder="templates",
    static_folder="static"
)
bootstrap = Bootstrap(app)
from app import routes
app.config['SECRET_KEY'] = 'the random string'

