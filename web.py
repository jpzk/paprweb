from flask import Flask
from flask import render_template
from flask import make_response
from flask import request

import os
import smtplib
import json

app = Flask(__name__)

languages = {
        'German' : 'de_DE.UTF-8',
        'English' : 'en_GB.UTF-8',
        'French' : 'fr_FR.UTF-8',
        'Spanish' : 'es_ES.UTF-8',
        'Polish' : 'pl_PL.UTF-8',
        'Russian' : 'ru_RU.UTF-8',
        'Japanese' : 'ja_JP.UTF-8',
        'Chinese' : 'zh_CN.UTF-8'
        }

months = {'January':1, 'Feburary':2, 'March':3, 'April':4, 'May':5,
        'June':6, 'July':7, 'August':8, 'September':9, 'October':10,
        'November':11, 'December':12}

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/feedback", methods=['POST'])
def feedback():
    data = json.loads(request.form['json'])

    email = data['email']
    msg = data['message']
    content = 'Feedback from %s with message: %s' % (email, msg)
    
    recipients = ['jendrik@madewithtea.com','pczek@gmail.com']
    s = smtplib.SMTP('localhost')
    s.sendmail('papercalendar', recipients, content)
    s.quit()

@app.route("/download", methods=['POST'])
def download():

    locale = languages[request.form['language']]
    month = months[request.form['startmonth']]
    year = str(int(request.form['year']))

    out = 'generated/papr_%s%s%s.pdf' % (month, year, locale)

    # generate
    options = (locale, month, out, year)
    os.system('python papr/papr/papr.py -l %s -m %s -o %s -y %s' % options)

    # serve
    hnd = open(out,'rb')
    content = hnd.read()
    hnd.close()
    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=calendar.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

if __name__ == "__main__":
    app.run()
