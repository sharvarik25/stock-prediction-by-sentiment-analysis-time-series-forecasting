from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/dataeda')
def dataeda():
    return render_template('dataeda.html')


@app.route('/architecture')
def show_architecture():
    return render_template('architecture.html')


@app.route('/sentimentanalysis')
def sentimentanalysis():
    return render_template('sentimentanalysis.html')


@app.route('/timeseriesanalysis')
def timeseriesanalysis():
    return render_template('timeseriesanalysis.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

