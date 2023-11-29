from flask import Flask, render_template, request, url_for
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
def index():
        return render_template('mainWeb.html')

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080, debug=True)
