import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from mock_data import db

app = Flask(__name__)
CORS(app)


def success(data=None):
    return jsonify({'code': 0, 'message': 'success', 'data': data})


def fail(message, code=4000):
    return jsonify({'code': code, 'message': message, 'data': None})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    return success(db.get_stats())


@app.route('/api/status-meta', methods=['GET'])
def get_status_meta():
    return success(db.get_status_meta())


@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    status = request.args.get('status')
    jobs = db.get_jobs(status=status)
    return success(jobs)


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = db.get_job(job_id)
    if not job:
        return fail('职位不存在', 4040)
    return success(job)


@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.get_json() or {}
    if not data.get('title'):
        return fail('职位名称不能为空', 4001)
    job = db.create_job(data)
    return success(job)


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json() or {}
    job = db.update_job(job_id, data)
    if not job:
        return fail('职位不存在', 4040)
    return success(job)


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    ok = db.delete_job(job_id)
    if not ok:
        return fail('职位不存在', 4040)
    return success()


@app.route('/api/jobs/<int:job_id>/applications', methods=['GET'])
def list_job_applications(job_id):
    job = db.get_job(job_id)
    if not job:
        return fail('职位不存在', 4040)
    status = request.args.get('status')
    apps = db.get_applications(job_id=job_id, status=status)
    return success({
        'job': job,
        'applications': apps
    })


@app.route('/api/applications', methods=['GET'])
def list_applications():
    job_id = request.args.get('job_id', type=int)
    status = request.args.get('status')
    apps = db.get_applications(job_id=job_id, status=status)
    return success(apps)


@app.route('/api/applications/<int:app_id>', methods=['GET'])
def get_application(app_id):
    app = db.get_application(app_id)
    if not app:
        return fail('投递记录不存在', 4041)
    job = db.get_job(app['job_id'])
    return success({
        'application': app,
        'job': job
    })


@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def apply_job(job_id):
    data = request.get_json() or {}
    app, err = db.create_application(job_id, data)
    if err:
        return fail(err, 4002)
    return success(app)


@app.route('/api/applications/<int:app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    data = request.get_json() or {}
    status = data.get('status')
    if not status:
        return fail('状态参数不能为空', 4003)
    app, err = db.update_application_status(app_id, status)
    if err:
        return fail(err, 4004)
    return success(app)


@app.route('/api/applications/<int:app_id>/messages', methods=['GET'])
def list_messages(app_id):
    msgs, err = db.get_messages(app_id)
    if err:
        return fail(err, 4041)
    return success(msgs)


@app.route('/api/applications/<int:app_id>/messages', methods=['POST'])
def send_message(app_id):
    data = request.get_json() or {}
    sender = data.get('sender')
    sender_name = data.get('sender_name', '')
    content = data.get('content', '')
    msg, err = db.create_message(app_id, sender, sender_name, content)
    if err:
        return fail(err, 4005)
    return success(msg)


@app.route('/api/applications/<int:app_id>/interviews', methods=['GET'])
def list_application_interviews(app_id):
    app = db.get_application(app_id)
    if not app:
        return fail('投递记录不存在', 4041)
    interviews = db.get_interviews(application_id=app_id)
    return success(interviews)


@app.route('/api/interviews', methods=['GET'])
def list_interviews():
    job_id = request.args.get('job_id', type=int)
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    interviews = db.get_interviews(
        job_id=job_id,
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    return success(interviews)


@app.route('/api/interviews/<int:interview_id>', methods=['GET'])
def get_interview(interview_id):
    interview = db.get_interview(interview_id)
    if not interview:
        return fail('面试记录不存在', 4042)
    app = db.get_application(interview['application_id'])
    job = db.get_job(interview['job_id'])
    return success({
        'interview': interview,
        'application': app,
        'job': job
    })


@app.route('/api/applications/<int:app_id>/interviews', methods=['POST'])
def create_interview(app_id):
    data = request.get_json() or {}
    interview, err = db.create_interview(app_id, data)
    if err:
        return fail(err, 4006)
    return success(interview)


@app.route('/api/interviews/<int:interview_id>', methods=['PUT'])
def update_interview(interview_id):
    data = request.get_json() or {}
    interview, err = db.update_interview(interview_id, data)
    if err:
        return fail(err, 4007)
    return success(interview)


@app.route('/api/interviews/<int:interview_id>/cancel', methods=['POST'])
def cancel_interview(interview_id):
    data = request.get_json() or {}
    reason = data.get('reason', '')
    interview, err = db.cancel_interview(interview_id, reason)
    if err:
        return fail(err, 4008)
    return success(interview)


@app.route('/api/interview-meta', methods=['GET'])
def get_interview_meta():
    return success(db.get_interview_meta())


@app.route('/api/reset', methods=['POST'])
def reset_data():
    db.reset()
    return success({'message': '数据已重置为初始状态'})


if __name__ == '__main__':
    print('=' * 50)
    print('  招聘平台后端启动中...')
    print('  接口地址: http://localhost:5000')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
