from flask import Flask
from routes.ops import ops  # import your blueprint

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Register Blueprint
app.register_blueprint(ops)

if __name__ == '__main__':
    app.run(debug=True)
