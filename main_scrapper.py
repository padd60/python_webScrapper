from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask('SuperScrapper')

db = {}


@app.route('/')
def home():
    return render_template('sample.html')

# @는 데코레이터 : 아래에 있는 함수를 찾아주는 역할

# route() 안에 인자를 밑에 함수에서 사용하면 동적 url을 사용할 수 있다.


@app.route('/report')
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect('/')
    return render_template('report.html', searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route('/export')
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file('jobs.csv')
    except:
        return redirect('/')


app.run(host='127.0.0.1')
