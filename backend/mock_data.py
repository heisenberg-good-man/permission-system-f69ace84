import copy
from datetime import datetime

def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

VALID_STATUSES = ('pending', 'screening', 'communicating', 'rejected', 'hired')

STATUS_FLOW = {
    'pending': ('screening', 'communicating', 'rejected'),
    'screening': ('communicating', 'rejected', 'pending'),
    'communicating': ('rejected', 'hired', 'screening', 'pending'),
    'rejected': ('pending', 'screening'),
    'hired': ()
}

STATUS_TEXT = {
    'pending': '新投递',
    'screening': '待沟通',
    'communicating': '沟通中',
    'rejected': '不合适',
    'hired': '已录用'
}

INTERVIEW_STATUS = ('scheduled', 'completed', 'cancelled', 'no_show')

INTERVIEW_STATUS_TEXT = {
    'scheduled': '已安排',
    'completed': '已完成',
    'cancelled': '已取消',
    'no_show': '未到场'
}

INTERVIEW_STATUS_TYPE = {
    'scheduled': 'primary',
    'completed': 'success',
    'cancelled': 'info',
    'no_show': 'danger'
}

INTERVIEW_WAYS = ('onsite', 'online', 'phone')

INTERVIEW_WAY_TEXT = {
    'onsite': '现场面试',
    'online': '视频面试',
    'phone': '电话面试'
}

INTERVIEW_ROUNDS = ('初筛', '一面', '二面', '三面', '终面', 'HR面')

INITIAL_JOBS = [
    {
        'id': 1,
        'title': '高级前端工程师',
        'company': '星辰科技',
        'department': '技术部',
        'salary_min': 20000,
        'salary_max': 35000,
        'city': '北京',
        'experience': '3-5年',
        'education': '本科',
        'description': '负责公司核心产品的前端架构设计与开发，参与技术选型与性能优化。',
        'requirements': '1. 精通 Vue/React 等主流框架\n2. 熟悉 TypeScript、工程化\n3. 有大型项目经验优先',
        'status': 'open',
        'created_at': '2026-07-10 09:30:00',
        'hr_id': 1,
        'hr_name': '李经理'
    },
    {
        'id': 2,
        'title': 'Python 后端开发工程师',
        'company': '星辰科技',
        'department': '技术部',
        'salary_min': 18000,
        'salary_max': 30000,
        'city': '上海',
        'experience': '1-3年',
        'education': '本科',
        'description': '负责后端服务的设计与开发，保障系统稳定性与高性能。',
        'requirements': '1. 熟悉 Python、Flask/Django\n2. 熟悉 MySQL、Redis\n3. 有微服务经验优先',
        'status': 'open',
        'created_at': '2026-07-12 14:20:00',
        'hr_id': 1,
        'hr_name': '李经理'
    },
    {
        'id': 3,
        'title': '产品经理',
        'company': '云帆互联',
        'department': '产品部',
        'salary_min': 15000,
        'salary_max': 25000,
        'city': '深圳',
        'experience': '3-5年',
        'education': '本科',
        'description': '负责 SaaS 产品的需求调研、产品设计与迭代推进。',
        'requirements': '1. 有 B 端产品经验\n2. 优秀的文档与沟通能力\n3. 熟悉敏捷开发流程',
        'status': 'open',
        'created_at': '2026-07-15 10:00:00',
        'hr_id': 2,
        'hr_name': '王主管'
    },
    {
        'id': 4,
        'title': 'UI 设计师',
        'company': '云帆互联',
        'department': '设计部',
        'salary_min': 12000,
        'salary_max': 20000,
        'city': '杭州',
        'experience': '1-3年',
        'education': '大专',
        'description': '负责公司产品界面设计与视觉规范制定。',
        'requirements': '1. 熟练使用 Figma/Sketch\n2. 有完整作品集\n3. 对用户体验有深入理解',
        'status': 'closed',
        'created_at': '2026-07-08 16:45:00',
        'hr_id': 2,
        'hr_name': '王主管'
    }
]

INITIAL_APPLICATIONS = [
    {
        'id': 1,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '张三',
        'candidate_phone': '13800138001',
        'candidate_email': 'zhangsan@example.com',
        'education': '本科',
        'experience': '4年',
        'resume': '5年前端开发经验，精通 Vue 全家桶，主导过 2 个大型项目。\n\n工作经历：\n- 2022-至今 某互联网公司 高级前端工程师\n- 2019-2022 某科技公司 前端开发工程师\n\n技能：Vue3, TypeScript, Vite, Node.js',
        'status': 'pending',
        'applied_at': '2026-07-13 11:20:00'
    },
    {
        'id': 2,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '李四',
        'candidate_phone': '13800138002',
        'candidate_email': 'lisi@example.com',
        'education': '硕士',
        'experience': '3年',
        'resume': '硕士学历，3年 React 开发经验，熟悉前端性能优化。\n\n项目经验：\n- 主导某电商后台系统重构，首屏加载速度提升 60%\n- 搭建前端监控系统，支持错误追踪与性能指标采集\n\n技能：React, TypeScript, Webpack, 性能优化',
        'status': 'communicating',
        'applied_at': '2026-07-14 09:10:00'
    },
    {
        'id': 3,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '王五',
        'candidate_phone': '13800138003',
        'candidate_email': 'wangwu@example.com',
        'education': '本科',
        'experience': '2年',
        'resume': '2年 Python 后端经验，熟悉 Flask + MySQL，有电商项目经验。\n\n教育背景：\n- 2019-2023 某某大学 计算机科学与技术 本科\n\n技能：Python, Flask, MySQL, Redis, Docker',
        'status': 'screening',
        'applied_at': '2026-07-16 15:30:00'
    },
    {
        'id': 4,
        'job_id': 3,
        'job_title': '产品经理',
        'candidate_name': '赵六',
        'candidate_phone': '13800138004',
        'candidate_email': 'zhaoliu@example.com',
        'education': '本科',
        'experience': '4年',
        'resume': '4年 B 端产品经验，负责过 CRM 系统从 0 到 1。',
        'status': 'rejected',
        'applied_at': '2026-07-11 10:00:00'
    }
]

INITIAL_MESSAGES = [
    {
        'id': 1,
        'application_id': 2,
        'sender': 'recruiter',
        'sender_name': '李经理',
        'content': '您好，您的简历我们已经看过了，想约您下周一上午 10 点面试，方便吗？',
        'created_at': '2026-07-15 10:30:00'
    },
    {
        'id': 2,
        'application_id': 2,
        'sender': 'candidate',
        'sender_name': '李四',
        'content': '好的，没问题，时间可以的。',
        'created_at': '2026-07-15 11:00:00'
    },
    {
        'id': 3,
        'application_id': 2,
        'sender': 'recruiter',
        'sender_name': '李经理',
        'content': '好的，那我们稍后把面试邀请发到您邮箱。',
        'created_at': '2026-07-15 11:15:00'
    }
]

INITIAL_INTERVIEWS = [
    {
        'id': 1,
        'application_id': 2,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '李四',
        'round': '一面',
        'way': 'onsite',
        'interview_time': '2026-07-22 10:00:00',
        'interviewer': '张技术总监',
        'location': '北京市朝阳区望京SOHO T3 20层会议室A',
        'meeting_link': '',
        'remark': '请携带简历和作品集',
        'status': 'scheduled',
        'created_at': '2026-07-15 14:00:00',
        'updated_at': '2026-07-15 14:00:00'
    }
]


class MockDB:
    def __init__(self):
        self.reset()

    def reset(self):
        self.jobs = copy.deepcopy(INITIAL_JOBS)
        self.applications = copy.deepcopy(INITIAL_APPLICATIONS)
        self.messages = copy.deepcopy(INITIAL_MESSAGES)
        self.interviews = copy.deepcopy(INITIAL_INTERVIEWS)
        self.next_job_id = max(j['id'] for j in self.jobs) + 1
        self.next_application_id = max(a['id'] for a in self.applications) + 1
        self.next_message_id = max(m['id'] for m in self.messages) + 1
        self.next_interview_id = max(i['id'] for i in self.interviews) + 1

    def get_status_meta(self):
        return {
            'valid_statuses': list(VALID_STATUSES),
            'status_flow': STATUS_FLOW,
            'status_text': STATUS_TEXT
        }

    def get_jobs(self, status=None):
        if status:
            return [j for j in self.jobs if j['status'] == status]
        return self.jobs

    def get_job(self, job_id):
        for j in self.jobs:
            if j['id'] == job_id:
                return j
        return None

    def create_job(self, data):
        job = {
            'id': self.next_job_id,
            'title': data.get('title', ''),
            'company': data.get('company', '星辰科技'),
            'department': data.get('department', ''),
            'salary_min': data.get('salary_min', 0),
            'salary_max': data.get('salary_max', 0),
            'city': data.get('city', ''),
            'experience': data.get('experience', ''),
            'education': data.get('education', ''),
            'description': data.get('description', ''),
            'requirements': data.get('requirements', ''),
            'status': 'open',
            'created_at': now_str(),
            'hr_id': 1,
            'hr_name': '李经理'
        }
        self.jobs.insert(0, job)
        self.next_job_id += 1
        return job

    def update_job(self, job_id, data):
        job = self.get_job(job_id)
        if not job:
            return None
        for k, v in data.items():
            if k in job and k not in ('id', 'created_at'):
                job[k] = v
        return job

    def delete_job(self, job_id):
        job = self.get_job(job_id)
        if not job:
            return False
        self.jobs = [j for j in self.jobs if j['id'] != job_id]
        return True

    def get_applications(self, job_id=None, status=None):
        result = self.applications
        if job_id:
            result = [a for a in result if a['job_id'] == job_id]
        if status:
            result = [a for a in result if a['status'] == status]
        return result

    def get_application(self, app_id):
        for a in self.applications:
            if a['id'] == app_id:
                return a
        return None

    def create_application(self, job_id, data):
        job = self.get_job(job_id)
        if not job:
            return None, '职位不存在，无法投递'
        if job['status'] != 'open':
            return None, '该职位已关闭招聘，无法投递'
        if not data.get('candidate_name'):
            return None, '候选人姓名不能为空'
        app = {
            'id': self.next_application_id,
            'job_id': job_id,
            'job_title': job['title'],
            'candidate_name': data.get('candidate_name', ''),
            'candidate_phone': data.get('candidate_phone', ''),
            'candidate_email': data.get('candidate_email', ''),
            'education': data.get('education', ''),
            'experience': data.get('experience', ''),
            'resume': data.get('resume', ''),
            'status': 'pending',
            'applied_at': now_str()
        }
        self.applications.insert(0, app)
        self.next_application_id += 1
        return app, None

    def update_application_status(self, app_id, new_status):
        app = self.get_application(app_id)
        if not app:
            return None, '投递记录不存在'
        if new_status not in VALID_STATUSES:
            return None, f'无效状态: {new_status}'
        old_status = app['status']
        if old_status == new_status:
            return app, None
        allowed = STATUS_FLOW.get(old_status, ())
        if new_status not in allowed:
            return None, f'无法从「{STATUS_TEXT[old_status]}」流转到「{STATUS_TEXT[new_status]}」'
        app['status'] = new_status
        return app, None

    def get_messages(self, application_id):
        app = self.get_application(application_id)
        if not app:
            return None, '投递记录不存在，无法加载消息'
        msgs = [m for m in self.messages if m['application_id'] == application_id]
        return msgs, None

    def create_message(self, application_id, sender, sender_name, content):
        app = self.get_application(application_id)
        if not app:
            return None, '投递记录不存在，无法发送消息'
        if sender not in ('recruiter', 'candidate'):
            return None, '无效发送方'
        if not content or not content.strip():
            return None, '消息内容不能为空'
        msg = {
            'id': self.next_message_id,
            'application_id': application_id,
            'sender': sender,
            'sender_name': sender_name or ('招聘方' if sender == 'recruiter' else '候选人'),
            'content': content.strip(),
            'created_at': now_str()
        }
        self.messages.append(msg)
        self.next_message_id += 1
        return msg, None

    def get_stats(self):
        total_jobs = len(self.jobs)
        open_jobs = len([j for j in self.jobs if j['status'] == 'open'])
        total_applications = len(self.applications)
        pending = len([a for a in self.applications if a['status'] == 'pending'])
        screening = len([a for a in self.applications if a['status'] == 'screening'])
        communicating = len([a for a in self.applications if a['status'] == 'communicating'])
        rejected = len([a for a in self.applications if a['status'] == 'rejected'])
        hired = len([a for a in self.applications if a['status'] == 'hired'])
        scheduled_interviews = len([i for i in self.interviews if i['status'] == 'scheduled'])
        return {
            'total_jobs': total_jobs,
            'open_jobs': open_jobs,
            'closed_jobs': total_jobs - open_jobs,
            'total_applications': total_applications,
            'pending_applications': pending,
            'screening': screening,
            'communicating': communicating,
            'rejected': rejected,
            'hired': hired,
            'scheduled_interviews': scheduled_interviews,
            'status_text': STATUS_TEXT
        }

    def get_interview_meta(self):
        return {
            'status_list': list(INTERVIEW_STATUS),
            'status_text': INTERVIEW_STATUS_TEXT,
            'status_type': INTERVIEW_STATUS_TYPE,
            'way_list': list(INTERVIEW_WAYS),
            'way_text': INTERVIEW_WAY_TEXT,
            'round_list': list(INTERVIEW_ROUNDS)
        }

    def get_interviews(self, application_id=None, job_id=None, status=None, start_date=None, end_date=None):
        result = self.interviews
        if application_id:
            result = [i for i in result if i['application_id'] == application_id]
        if job_id:
            result = [i for i in result if i['job_id'] == job_id]
        if status:
            result = [i for i in result if i['status'] == status]
        if start_date:
            result = [i for i in result if i['interview_time'] >= start_date]
        if end_date:
            result = [i for i in result if i['interview_time'] <= end_date + ' 23:59:59']
        result = sorted(result, key=lambda x: x['interview_time'], reverse=True)
        return result

    def get_interview(self, interview_id):
        for i in self.interviews:
            if i['id'] == interview_id:
                return i
        return None

    def create_interview(self, application_id, data):
        app = self.get_application(application_id)
        if not app:
            return None, '投递记录不存在，无法安排面试'
        if app['status'] == 'rejected':
            return None, '该候选人状态为「不合适」，无法安排面试'
        if app['status'] == 'hired':
            return None, '该候选人已录用，无需安排面试'
        if not data.get('interview_time'):
            return None, '面试时间不能为空'
        if not data.get('interviewer'):
            return None, '面试官不能为空'
        if not data.get('round'):
            return None, '面试轮次不能为空'
        if not data.get('way'):
            return None, '面试方式不能为空'
        way = data.get('way')
        if way not in INTERVIEW_WAYS:
            return None, f'无效的面试方式: {way}'
        interview = {
            'id': self.next_interview_id,
            'application_id': application_id,
            'job_id': app['job_id'],
            'job_title': app['job_title'],
            'candidate_name': app['candidate_name'],
            'round': data.get('round', ''),
            'way': way,
            'interview_time': data.get('interview_time', ''),
            'interviewer': data.get('interviewer', ''),
            'location': data.get('location', ''),
            'meeting_link': data.get('meeting_link', ''),
            'remark': data.get('remark', ''),
            'status': 'scheduled',
            'created_at': now_str(),
            'updated_at': now_str()
        }
        self.interviews.insert(0, interview)
        self.next_interview_id += 1
        if app['status'] in ('pending', 'screening'):
            app['status'] = 'communicating'
        sys_msg = f'【系统消息】已安排{interview["round"]}：{INTERVIEW_WAY_TEXT[interview["way"]]}，时间：{interview["interview_time"]}，面试官：{interview["interviewer"]}'
        if interview['location']:
            sys_msg += f'，地点：{interview["location"]}'
        if interview['meeting_link']:
            sys_msg += f'，会议链接：{interview["meeting_link"]}'
        self._add_system_message(application_id, sys_msg)
        return interview, None

    def update_interview(self, interview_id, data):
        interview = self.get_interview(interview_id)
        if not interview:
            return None, '面试记录不存在'
        if interview['status'] != 'scheduled':
            return None, '只有已安排状态的面试可以修改'
        if 'way' in data and data['way'] not in INTERVIEW_WAYS:
            return None, f'无效的面试方式: {data["way"]}'
        old_time = interview['interview_time']
        for k, v in data.items():
            if k in interview and k not in ('id', 'application_id', 'job_id', 'job_title', 'candidate_name', 'status', 'created_at'):
                interview[k] = v
        interview['updated_at'] = now_str()
        app = self.get_application(interview['application_id'])
        if app and old_time != interview['interview_time']:
            sys_msg = f'【系统消息】面试时间已调整：{interview["round"]}调整为 {interview["interview_time"]}'
            self._add_system_message(interview['application_id'], sys_msg)
        return interview, None

    def cancel_interview(self, interview_id, reason=''):
        interview = self.get_interview(interview_id)
        if not interview:
            return None, '面试记录不存在'
        if interview['status'] != 'scheduled':
            return None, '只有已安排状态的面试可以取消'
        interview['status'] = 'cancelled'
        interview['updated_at'] = now_str()
        app = self.get_application(interview['application_id'])
        if app:
            sys_msg = f'【系统消息】{interview["round"]}已取消'
            if reason:
                sys_msg += f'，原因：{reason}'
            self._add_system_message(interview['application_id'], sys_msg)
        return interview, None

    def _add_system_message(self, application_id, content):
        msg = {
            'id': self.next_message_id,
            'application_id': application_id,
            'sender': 'system',
            'sender_name': '系统通知',
            'content': content,
            'created_at': now_str()
        }
        self.messages.append(msg)
        self.next_message_id += 1


db = MockDB()
