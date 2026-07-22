import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from mock_data import db

app = Flask(__name__)
CORS(app)

VALID_ROLES = ('candidate', 'recruiter', 'hiring_manager')


def success(data=None):
    return jsonify({'code': 0, 'message': 'success', 'data': data})


def fail(message, code=4000):
    return jsonify({'code': code, 'message': message, 'data': None})


def get_current_role():
    role = request.args.get('role', request.headers.get('x-role', 'recruiter'))
    if role not in VALID_ROLES:
        return 'recruiter'
    return role


def get_current_candidate_name():
    return request.args.get('candidate_name', request.headers.get('x-candidate-name', ''))


def require_role(allowed_roles):
    role = get_current_role()
    if role not in allowed_roles:
        role_names = {'candidate': '应聘方', 'recruiter': '招聘方', 'hiring_manager': '招聘负责人'}
        allowed_names = [role_names.get(r, r) for r in allowed_roles]
        return False, f'当前角色无权执行此操作，仅{"、".join(allowed_names)}可操作'
    return True, None


def check_application_access(app_id, action='view'):
    role = get_current_role()
    application = db.get_application(app_id)
    if not application:
        return False, '投递记录不存在', 4041
    if role == 'candidate':
        candidate_name = get_current_candidate_name()
        if not candidate_name:
            return False, '请先登录后再操作', 4010
        if application['candidate_name'] != candidate_name:
            return False, '无权查看或操作他人的投递记录', 4031
    if action == 'manage' and role not in ('recruiter',):
        return False, '仅招聘方可执行此管理操作', 4030
    return True, application, 0


def check_offer_ownership(offer, action='operate'):
    role = get_current_role()
    if role == 'candidate':
        candidate_name = get_current_candidate_name()
        if not candidate_name:
            return False, '请先登录后再操作'
        if offer['candidate_name'] != candidate_name:
            return False, '无权操作他人的 Offer'
    return True, None


def check_recruiter_offer_access(offer):
    role = get_current_role()
    if role != 'recruiter':
        return True, None
    app = db.get_application(offer['application_id'])
    if not app:
        return False, 'Offer 对应投递记录不存在'
    job = db.get_job(offer['job_id'])
    if not job:
        return False, 'Offer 对应职位不存在'
    return True, None


@app.route('/api/stats', methods=['GET'])
def get_stats():
    return success(db.get_stats())


@app.route('/api/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    job_id = request.args.get('job_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return success(db.get_dashboard_stats(job_id=job_id, start_date=start_date, end_date=end_date))


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
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    data = request.get_json() or {}
    if not data.get('title'):
        return fail('职位名称不能为空', 4001)
    job = db.create_job(data)
    return success(job)


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    data = request.get_json() or {}
    job = db.update_job(job_id, data)
    if not job:
        return fail('职位不存在', 4040)
    return success(job)


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    ok = db.delete_job(job_id)
    if not ok:
        return fail('职位不存在', 4040)
    return success()


@app.route('/api/jobs/<int:job_id>/applications', methods=['GET'])
def list_job_applications(job_id):
    allowed, err_msg = require_role(('recruiter', 'hiring_manager'))
    if not allowed:
        return fail(err_msg, 4030)
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
    role = get_current_role()
    job_id = request.args.get('job_id', type=int)
    status = request.args.get('status')
    apps = db.get_applications(job_id=job_id, status=status)
    if role == 'candidate':
        candidate_name = get_current_candidate_name()
        if candidate_name:
            apps = [a for a in apps if a['candidate_name'] == candidate_name]
    return success(apps)


@app.route('/api/applications/<int:app_id>', methods=['GET'])
def get_application(app_id):
    ok, result, code = check_application_access(app_id, 'view')
    if not ok:
        return fail(result, code)
    app = result
    job = db.get_job(app['job_id'])
    return success({
        'application': app,
        'job': job
    })


@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def apply_job(job_id):
    allowed, err_msg = require_role(('candidate',))
    if not allowed:
        return fail(err_msg, 4030)
    data = request.get_json() or {}
    app, err = db.create_application(job_id, data)
    if err:
        return fail(err, 4002)
    return success(app)


@app.route('/api/applications/<int:app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    ok, result, code = check_application_access(app_id, 'manage')
    if not ok:
        return fail(result, code)
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
    ok, result, code = check_application_access(app_id, 'view')
    if not ok:
        return fail(result, code)
    msgs, err = db.get_messages(app_id)
    if err:
        return fail(err, 4041)
    return success(msgs)


@app.route('/api/applications/<int:app_id>/messages', methods=['POST'])
def send_message(app_id):
    role = get_current_role()
    ok, result, code = check_application_access(app_id, 'view')
    if not ok:
        return fail(result, code)
    if role == 'hiring_manager':
        return fail('招聘负责人无权发送沟通消息', 4030)
    data = request.get_json() or {}
    sender = data.get('sender')
    sender_name = data.get('sender_name', '')
    content = data.get('content', '')
    if role == 'candidate' and sender != 'candidate':
        return fail('应聘方只能以候选人身份发送消息', 4035)
    if role == 'recruiter' and sender != 'recruiter':
        return fail('招聘方只能以招聘方身份发送消息', 4035)
    msg, err = db.create_message(app_id, sender, sender_name, content)
    if err:
        return fail(err, 4005)
    return success(msg)


@app.route('/api/applications/<int:app_id>/interviews', methods=['GET'])
def list_application_interviews(app_id):
    ok, result, code = check_application_access(app_id, 'view')
    if not ok:
        return fail(result, code)
    interviews = db.get_interviews(application_id=app_id)
    return success(interviews)


@app.route('/api/interviews', methods=['GET'])
def list_interviews():
    role = get_current_role()
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
    if role == 'candidate':
        candidate_name = get_current_candidate_name()
        if candidate_name:
            interviews = [i for i in interviews if i['candidate_name'] == candidate_name]
    return success(interviews)


@app.route('/api/interviews/<int:interview_id>', methods=['GET'])
def get_interview(interview_id):
    interview = db.get_interview(interview_id)
    if not interview:
        return fail('面试记录不存在', 4042)
    ok, result, code = check_application_access(interview['application_id'], 'view')
    if not ok:
        return fail(result, code)
    app = db.get_application(interview['application_id'])
    job = db.get_job(interview['job_id'])
    return success({
        'interview': interview,
        'application': app,
        'job': job
    })


@app.route('/api/applications/<int:app_id>/interviews', methods=['POST'])
def create_interview(app_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    ok, result, code = check_application_access(app_id, 'manage')
    if not ok:
        return fail(result, code)
    data = request.get_json() or {}
    interview, err = db.create_interview(app_id, data)
    if err:
        return fail(err, 4006)
    return success(interview)


@app.route('/api/interviews/<int:interview_id>', methods=['PUT'])
def update_interview(interview_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    interview = db.get_interview(interview_id)
    if not interview:
        return fail('面试记录不存在', 4042)
    ok, result, code = check_application_access(interview['application_id'], 'manage')
    if not ok:
        return fail(result, code)
    data = request.get_json() or {}
    interview, err = db.update_interview(interview_id, data)
    if err:
        return fail(err, 4007)
    return success(interview)


@app.route('/api/interviews/<int:interview_id>/cancel', methods=['POST'])
def cancel_interview(interview_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    interview = db.get_interview(interview_id)
    if not interview:
        return fail('面试记录不存在', 4042)
    ok, result, code = check_application_access(interview['application_id'], 'manage')
    if not ok:
        return fail(result, code)
    data = request.get_json() or {}
    reason = data.get('reason', '')
    interview, err = db.cancel_interview(interview_id, reason)
    if err:
        return fail(err, 4008)
    return success(interview)


@app.route('/api/interview-meta', methods=['GET'])
def get_interview_meta():
    return success(db.get_interview_meta())


@app.route('/api/interviews/<int:interview_id>/feedback', methods=['POST'])
def submit_interview_feedback(interview_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    interview = db.get_interview(interview_id)
    if not interview:
        return fail('面试记录不存在', 4042)
    ok, result, code = check_application_access(interview['application_id'], 'manage')
    if not ok:
        return fail(result, code)
    data = request.get_json() or {}
    interview, err = db.submit_interview_feedback(interview_id, data)
    if err:
        return fail(err, 4009)
    return success(interview)


@app.route('/api/offers', methods=['GET'])
def list_offers():
    role = get_current_role()
    job_id = request.args.get('job_id', type=int)
    status = request.args.get('status')
    application_id = request.args.get('application_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    offers = db.get_offers(
        application_id=application_id,
        job_id=job_id,
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    if role == 'candidate':
        candidate_name = get_current_candidate_name()
        if candidate_name:
            offers = [o for o in offers if o['candidate_name'] == candidate_name]
    return success(offers)


@app.route('/api/offers/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    offer = db.get_offer(offer_id)
    if not offer:
        return fail('Offer 不存在', 4043)
    allowed, err_msg = check_offer_ownership(offer, 'view')
    if not allowed:
        return fail(err_msg, 4031)
    app = db.get_application(offer['application_id'])
    if not app:
        return fail('Offer 对应投递记录不存在', 4041)
    job = db.get_job(offer['job_id'])
    return success({
        'offer': offer,
        'application': app,
        'job': job
    })


@app.route('/api/applications/<int:app_id>/offers', methods=['POST'])
def create_offer(app_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    ok, result, code = check_application_access(app_id, 'manage')
    if not ok:
        return fail(result, code)
    data = request.get_json() or {}
    offer, err = db.create_offer(app_id, data)
    if err:
        return fail(err, 4010)
    return success(offer)


@app.route('/api/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    offer = db.get_offer(offer_id)
    if not offer:
        return fail('Offer 不存在', 4043)
    allowed2, err_msg2 = check_recruiter_offer_access(offer)
    if not allowed2:
        return fail(err_msg2, 4034)
    data = request.get_json() or {}
    offer, err = db.update_offer(offer_id, data)
    if err:
        return fail(err, 4011)
    return success(offer)


@app.route('/api/offers/<int:offer_id>/send', methods=['POST'])
def send_offer(offer_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    offer = db.get_offer(offer_id)
    if not offer:
        return fail('Offer 不存在', 4043)
    allowed2, err_msg2 = check_recruiter_offer_access(offer)
    if not allowed2:
        return fail(err_msg2, 4034)
    offer, err = db.send_offer(offer_id)
    if err:
        return fail(err, 4012)
    return success(offer)


@app.route('/api/offers/<int:offer_id>/accept', methods=['POST'])
def accept_offer(offer_id):
    allowed, err_msg = require_role(('candidate',))
    if not allowed:
        return fail(err_msg, 4030)
    offer = db.get_offer(offer_id)
    if not offer:
        return fail('Offer 不存在', 4043)
    allowed2, err_msg2 = check_offer_ownership(offer, 'accept')
    if not allowed2:
        return fail(err_msg2, 4031)
    app = db.get_application(offer['application_id'])
    if not app:
        return fail('Offer 对应投递记录不存在', 4041)
    if app['candidate_name'] != offer['candidate_name'] or app['job_id'] != offer['job_id']:
        return fail('Offer 与投递记录不匹配', 4033)
    offer, err = db.accept_offer(offer_id)
    if err:
        return fail(err, 4013)
    return success(offer)


@app.route('/api/offers/<int:offer_id>/reject', methods=['POST'])
def reject_offer(offer_id):
    allowed, err_msg = require_role(('candidate',))
    if not allowed:
        return fail(err_msg, 4030)
    offer = db.get_offer(offer_id)
    if not offer:
        return fail('Offer 不存在', 4043)
    allowed2, err_msg2 = check_offer_ownership(offer, 'reject')
    if not allowed2:
        return fail(err_msg2, 4031)
    app = db.get_application(offer['application_id'])
    if not app:
        return fail('Offer 对应投递记录不存在', 4041)
    if app['candidate_name'] != offer['candidate_name'] or app['job_id'] != offer['job_id']:
        return fail('Offer 与投递记录不匹配', 4033)
    data = request.get_json() or {}
    reason = data.get('reason', '')
    if not reason or not reason.strip():
        return fail('请填写拒绝原因', 4014)
    offer, err = db.reject_offer(offer_id, reason)
    if err:
        return fail(err, 4014)
    return success(offer)


@app.route('/api/offers/<int:offer_id>/withdraw', methods=['POST'])
def withdraw_offer(offer_id):
    allowed, err_msg = require_role(('recruiter',))
    if not allowed:
        return fail(err_msg, 4030)
    offer = db.get_offer(offer_id)
    if not offer:
        return fail('Offer 不存在', 4043)
    allowed2, err_msg2 = check_recruiter_offer_access(offer)
    if not allowed2:
        return fail(err_msg2, 4034)
    data = request.get_json() or {}
    reason = data.get('reason', '')
    if not reason or not reason.strip():
        return fail('请填写撤回原因', 4015)
    offer, err = db.withdraw_offer(offer_id, reason)
    if err:
        return fail(err, 4015)
    return success(offer)


@app.route('/api/offer-meta', methods=['GET'])
def get_offer_meta():
    return success(db.get_offer_meta())


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
