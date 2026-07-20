import copy
from datetime import datetime

def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
        'resume': '5年前端开发经验，精通 Vue 全家桶，主导过 2 个大型项目。',
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
        'resume': '硕士学历，3年 React 开发经验，熟悉前端性能优化。',
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
        'resume': '2年 Python 后端经验，熟悉 Flask + MySQL，有电商项目经验。',
        'status': 'pending',
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


class MockDB:
    def __init__(self):
        self.reset()

    def reset(self):
        self.jobs = copy.deepcopy(INITIAL_JOBS)
        self.applications = copy.deepcopy(INITIAL_APPLICATIONS)
        self.messages = copy.deepcopy(INITIAL_MESSAGES)
        self.next_job_id = max(j['id'] for j in self.jobs) + 1
        self.next_application_id = max(a['id'] for a in self.applications) + 1
        self.next_message_id = max(m['id'] for m in self.messages) + 1

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
            return None
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
        return app

    def update_application_status(self, app_id, status):
        app = self.get_application(app_id)
        if not app:
            return None
        app['status'] = status
        return app

    def get_messages(self, application_id):
        return [m for m in self.messages if m['application_id'] == application_id]

    def create_message(self, application_id, sender, sender_name, content):
        msg = {
            'id': self.next_message_id,
            'application_id': application_id,
            'sender': sender,
            'sender_name': sender_name,
            'content': content,
            'created_at': now_str()
        }
        self.messages.append(msg)
        self.next_message_id += 1
        return msg

    def get_stats(self):
        total_jobs = len(self.jobs)
        open_jobs = len([j for j in self.jobs if j['status'] == 'open'])
        total_applications = len(self.applications)
        pending_applications = len([a for a in self.applications if a['status'] == 'pending'])
        communicating = len([a for a in self.applications if a['status'] == 'communicating'])
        rejected = len([a for a in self.applications if a['status'] == 'rejected'])
        return {
            'total_jobs': total_jobs,
            'open_jobs': open_jobs,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'communicating': communicating,
            'rejected': rejected
        }


db = MockDB()
