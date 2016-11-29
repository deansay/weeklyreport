from flask import make_response, jsonify, request
import datetime
from server import app
from server.model import db
from server.model.week import Week

date_format = '%Y-%m-%d'

@app.route('/weeks/init', methods=['post'])
def generate_weeks():
    count_num = 18
    for i in range(count_num):
        day = get_previous_report_day(i)
        week = Week(day)
        db.session.add(week)
    db.session.commit()
    result = {'success': True}
    response = make_response(jsonify(result), 200)
    # response.set_cookie('username', 'the username')
    response.headers['Content-type'] = 'application/json'
    return response


def get_previous_report_day(times):
    today = datetime.date.today()
    previous_day = today - (datetime.timedelta(7 - today.weekday())) * times
    return datetime.date.strftime(previous_day, date_format)


@app.route('/weeks', methods=['get'])
def get_all_weeks():
    weeks = Week.query.all()
    response = make_response(jsonify([week.serialize() for week in weeks]), 200)
    # response.set_cookie('username', 'the username')
    response.headers['Content-type'] = 'application/json'
    return response


@app.route('/weeks', methods=['post'])
def save_week():
    week_date = request.values['date']
    week = Week(week_date)
    db.session.add(week)
    db.session.commit()

    response = make_response(jsonify({'week': week.serialize()}), 200)
    # response.set_cookie('username', 'the username')
    response.headers['Content-type'] = 'application/json'
    return response


@app.route('/weeks/<week_id>', methods=['put'])
def update_week(week_id):
    # status could be skipped [skip], holiday[] or normal [active]
    week = Week.query.filter_by(id=week_id).first()
    status = request.values['status']
    week.status = status
    db.session.commit()
    response = make_response(jsonify(week), 200)
    response.headers['Content-type'] = 'application/json'
    return response


@app.route('/weeks/next', methods=['get'])
def next_week():
    today = datetime.date.today()
    today = datetime.date.strftime(today, date_format)
    week = Week.query.filter(Week.date>today).first()
    if week is None:
        next_report_day = get_next_report_day()
        week = Week(next_report_day)
        db.session.add(week)
        db.session.commit()
    response = make_response(jsonify(week.serialize()), 200)
    response.headers['Content-type'] = 'application/json'
    return response


def get_next_report_day():
    today = datetime.date.today()
    if today.weekday() == app.config['REPORT_DAY']: #
        next_day = today
    else:
        next_day = today + datetime.timedelta(7 - today.weekday())
    return datetime.date.strftime(next_day, date_format)
