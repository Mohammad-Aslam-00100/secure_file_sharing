from flask import Flask
from routes.ops import ops 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

app.register_blueprint(ops)

if __name__ == '__main__':
    app.run(debug=True)
