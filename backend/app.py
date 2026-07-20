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


def fail(message, code=1):
    return jsonify({'code': code, 'message': message, 'data': None})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    return success(db.get_stats())


@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    status = request.args.get('status')
    jobs = db.get_jobs(status=status)
    return success(jobs)


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = db.get_job(job_id)
    if not job:
        return fail('职位不存在')
    return success(job)


@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.get_json() or {}
    if not data.get('title'):
        return fail('职位名称不能为空')
    job = db.create_job(data)
    return success(job)


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json() or {}
    job = db.update_job(job_id, data)
    if not job:
        return fail('职位不存在')
    return success(job)


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db.delete_job(job_id)
    return success()


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
        return fail('投递不存在')
    return success(app)


@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def apply_job(job_id):
    data = request.get_json() or {}
    if not data.get('candidate_name'):
        return fail('姓名不能为空')
    app = db.create_application(job_id, data)
    if not app:
        return fail('职位不存在')
    return success(app)


@app.route('/api/applications/<int:app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    data = request.get_json() or {}
    status = data.get('status')
    if status not in ('pending', 'communicating', 'rejected', 'hired'):
        return fail('无效状态')
    app = db.update_application_status(app_id, status)
    if not app:
        return fail('投递不存在')
    return success(app)


@app.route('/api/applications/<int:app_id>/messages', methods=['GET'])
def list_messages(app_id):
    messages = db.get_messages(app_id)
    return success(messages)


@app.route('/api/applications/<int:app_id>/messages', methods=['POST'])
def send_message(app_id):
    data = request.get_json() or {}
    sender = data.get('sender')
    sender_name = data.get('sender_name', '')
    content = data.get('content', '')
    if sender not in ('recruiter', 'candidate'):
        return fail('无效发送方')
    if not content.strip():
        return fail('消息内容不能为空')
    msg = db.create_message(app_id, sender, sender_name, content)
    return success(msg)


@app.route('/api/reset', methods=['POST'])
def reset_data():
    db.reset()
    return success({'message': '数据已重置'})


if __name__ == '__main__':
    print('=' * 50)
    print('  招聘平台后端启动中...')
    print('  接口地址: http://localhost:5000')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
