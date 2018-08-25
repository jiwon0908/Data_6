from flask import Flask, render_template,url_for

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def show_home():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/<path>')
def show_path(path):
    return render_template('%s.html' % path)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True)