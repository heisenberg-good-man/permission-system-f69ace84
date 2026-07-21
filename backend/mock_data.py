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

INTERVIEW_FEEDBACK_RESULTS = ('pass', 'fail', 'pending')

INTERVIEW_FEEDBACK_RESULT_TEXT = {
    'pass': '通过',
    'fail': '未通过',
    'pending': '待定'
}

OFFER_STATUS = ('draft', 'sent', 'accepted', 'rejected', 'withdrawn')

OFFER_STATUS_TEXT = {
    'draft': '草稿',
    'sent': '已发送',
    'accepted': '候选人已接受',
    'rejected': '候选人已拒绝',
    'withdrawn': '已撤回'
}

OFFER_STATUS_TYPE = {
    'draft': 'info',
    'sent': 'primary',
    'accepted': 'success',
    'rejected': 'danger',
    'withdrawn': 'warning'
}

def _gen_dates():
    from datetime import datetime, timedelta
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    monday = now - timedelta(days=now.weekday())
    tuesday = monday + timedelta(days=1)
    wednesday = monday + timedelta(days=2)
    thursday = monday + timedelta(days=3)
    two_weeks_ago = monday - timedelta(days=7)
    last_month = now - timedelta(days=30)
    return {
        'today': today + ' 10:00:00',
        'today_afternoon': today + ' 14:30:00',
        'today_evening': today + ' 18:00:00',
        'this_tuesday': tuesday.strftime('%Y-%m-%d') + ' 09:00:00',
        'this_wednesday': wednesday.strftime('%Y-%m-%d') + ' 11:00:00',
        'this_thursday': thursday.strftime('%Y-%m-%d') + ' 15:00:00',
        'this_week': monday.strftime('%Y-%m-%d') + ' 11:00:00',
        'last_week': two_weeks_ago.strftime('%Y-%m-%d') + ' 10:00:00',
        'last_week_friday': (two_weeks_ago + timedelta(days=4)).strftime('%Y-%m-%d') + ' 16:00:00',
        'last_month': last_month.strftime('%Y-%m-%d') + ' 15:00:00',
        'today_interview': today + ' 15:00:00',
        'tomorrow_interview': (now + timedelta(days=1)).strftime('%Y-%m-%d') + ' 10:00:00',
        'yesterday_interview': (now - timedelta(days=1)).strftime('%Y-%m-%d') + ' 14:00:00',
        'week_interview': tuesday.strftime('%Y-%m-%d') + ' 11:00:00',
        'old_interview': two_weeks_ago.strftime('%Y-%m-%d') + ' 10:00:00',
        'offer_join_today': (now + timedelta(days=7)).strftime('%Y-%m-%d'),
        'offer_join_next_week': (now + timedelta(days=14)).strftime('%Y-%m-%d'),
        'offer_join_next_month': (now + timedelta(days=30)).strftime('%Y-%m-%d'),
    }


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
        'created_at': 'DYNAMIC_last_month',
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
        'created_at': 'DYNAMIC_this_week',
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
        'created_at': 'DYNAMIC_today',
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
        'created_at': 'DYNAMIC_last_week',
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
        'applied_at': 'DYNAMIC_today'
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
        'applied_at': 'DYNAMIC_this_week'
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
        'applied_at': 'DYNAMIC_last_week'
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
        'applied_at': 'DYNAMIC_last_month'
    },
    {
        'id': 5,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '孙七',
        'candidate_phone': '13800138005',
        'candidate_email': 'sunqi@example.com',
        'education': '本科',
        'experience': '5年',
        'resume': '5年 Python 后端经验，精通 Django + PostgreSQL，带过 3 人团队。',
        'status': 'pending',
        'applied_at': 'DYNAMIC_today_afternoon'
    },
    {
        'id': 6,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '周八',
        'candidate_phone': '13800138006',
        'candidate_email': 'zhouba@example.com',
        'education': '本科',
        'experience': '6年',
        'resume': '6年前端经验，精通 Vue3 + TypeScript，有大型中台项目经验。',
        'status': 'communicating',
        'applied_at': 'DYNAMIC_last_week'
    },
    {
        'id': 7,
        'job_id': 3,
        'job_title': '产品经理',
        'candidate_name': '吴九',
        'candidate_phone': '13800138007',
        'candidate_email': 'wujiu@example.com',
        'education': '硕士',
        'experience': '5年',
        'resume': '5年 B 端产品经验，负责过企业 SaaS 产品全生命周期。',
        'status': 'communicating',
        'applied_at': 'DYNAMIC_this_tuesday'
    },
    {
        'id': 8,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '郑十',
        'candidate_phone': '13800138008',
        'candidate_email': 'zhengshi@example.com',
        'education': '硕士',
        'experience': '3年',
        'resume': '3年后端经验，熟悉 FastAPI + MySQL，有高并发系统经验。',
        'status': 'communicating',
        'applied_at': 'DYNAMIC_this_wednesday'
    },
    {
        'id': 9,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '钱十一',
        'candidate_phone': '13800138009',
        'candidate_email': 'qianshiyi@example.com',
        'education': '本科',
        'experience': '4年',
        'resume': '4年前端经验，熟悉 React + Node.js 全栈开发。',
        'status': 'communicating',
        'applied_at': 'DYNAMIC_last_month'
    },
    {
        'id': 10,
        'job_id': 3,
        'job_title': '产品经理',
        'candidate_name': '陈十二',
        'candidate_phone': '13800138010',
        'candidate_email': 'chenshier@example.com',
        'education': '本科',
        'experience': '3年',
        'resume': '3年 C 端产品经验，有用户增长产品经验。',
        'status': 'screening',
        'applied_at': 'DYNAMIC_today'
    }
]

INITIAL_MESSAGES = [
    {
        'id': 1,
        'application_id': 2,
        'sender': 'recruiter',
        'sender_name': '李经理',
        'content': '您好，您的简历我们已经看过了，想约您下周一上午 10 点面试，方便吗？',
        'created_at': 'DYNAMIC_this_tuesday'
    },
    {
        'id': 2,
        'application_id': 2,
        'sender': 'candidate',
        'sender_name': '李四',
        'content': '好的，没问题，时间可以的。',
        'created_at': 'DYNAMIC_this_tuesday'
    },
    {
        'id': 3,
        'application_id': 2,
        'sender': 'recruiter',
        'sender_name': '李经理',
        'content': '好的，那我们稍后把面试邀请发到您邮箱。',
        'created_at': 'DYNAMIC_this_tuesday'
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
        'interview_time': 'DYNAMIC_today_interview',
        'interviewer': '张技术总监',
        'location': '北京市朝阳区望京SOHO T3 20层会议室A',
        'meeting_link': '',
        'remark': '请携带简历和作品集',
        'status': 'scheduled',
        'feedback_result': '',
        'feedback_comment': '',
        'feedback_rating': 0,
        'feedback_at': '',
        'created_at': 'DYNAMIC_this_tuesday',
        'updated_at': 'DYNAMIC_this_tuesday'
    },
    {
        'id': 2,
        'application_id': 3,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '王五',
        'round': '初筛',
        'way': 'phone',
        'interview_time': 'DYNAMIC_week_interview',
        'interviewer': '李经理',
        'location': '',
        'meeting_link': '',
        'remark': '电话初筛，30分钟',
        'status': 'completed',
        'feedback_result': 'pass',
        'feedback_comment': '基础扎实，经验匹配，进入一面',
        'feedback_rating': 4,
        'feedback_at': 'DYNAMIC_week_interview',
        'created_at': 'DYNAMIC_last_week',
        'updated_at': 'DYNAMIC_week_interview'
    },
    {
        'id': 3,
        'application_id': 5,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '孙七',
        'round': '一面',
        'way': 'online',
        'interview_time': 'DYNAMIC_tomorrow_interview',
        'interviewer': '王技术经理',
        'location': '',
        'meeting_link': 'https://meeting.example.com/456',
        'remark': '',
        'status': 'scheduled',
        'feedback_result': '',
        'feedback_comment': '',
        'feedback_rating': 0,
        'feedback_at': '',
        'created_at': 'DYNAMIC_today',
        'updated_at': 'DYNAMIC_today'
    },
    {
        'id': 4,
        'application_id': 6,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '周八',
        'round': '二面',
        'way': 'onsite',
        'interview_time': 'DYNAMIC_last_week',
        'interviewer': '张技术总监',
        'location': '北京市朝阳区望京SOHO T3 20层会议室A',
        'meeting_link': '',
        'remark': '',
        'status': 'completed',
        'feedback_result': 'pass',
        'feedback_comment': '技术扎实，经验丰富，符合岗位要求',
        'feedback_rating': 5,
        'feedback_at': 'DYNAMIC_last_week',
        'created_at': 'DYNAMIC_last_week',
        'updated_at': 'DYNAMIC_last_week'
    },
    {
        'id': 5,
        'application_id': 7,
        'job_id': 3,
        'job_title': '产品经理',
        'candidate_name': '吴九',
        'round': '终面',
        'way': 'onsite',
        'interview_time': 'DYNAMIC_this_tuesday',
        'interviewer': '产品总监',
        'location': '深圳市南山区科技园',
        'meeting_link': '',
        'remark': '',
        'status': 'completed',
        'feedback_result': 'pass',
        'feedback_comment': '产品思维好，经验匹配',
        'feedback_rating': 4,
        'feedback_at': 'DYNAMIC_this_tuesday',
        'created_at': 'DYNAMIC_this_tuesday',
        'updated_at': 'DYNAMIC_this_tuesday'
    },
    {
        'id': 6,
        'application_id': 8,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '郑十',
        'round': '一面',
        'way': 'online',
        'interview_time': 'DYNAMIC_this_wednesday',
        'interviewer': '王技术经理',
        'location': '',
        'meeting_link': 'https://meeting.example.com/789',
        'remark': '',
        'status': 'completed',
        'feedback_result': 'pass',
        'feedback_comment': '基础扎实，潜力大',
        'feedback_rating': 4,
        'feedback_at': 'DYNAMIC_this_wednesday',
        'created_at': 'DYNAMIC_this_wednesday',
        'updated_at': 'DYNAMIC_this_wednesday'
    },
    {
        'id': 7,
        'application_id': 9,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '钱十一',
        'round': '二面',
        'way': 'onsite',
        'interview_time': 'DYNAMIC_last_month',
        'interviewer': '张技术总监',
        'location': '北京市朝阳区望京SOHO T3 20层会议室A',
        'meeting_link': '',
        'remark': '',
        'status': 'completed',
        'feedback_result': 'pass',
        'feedback_comment': '全栈能力强，适合岗位',
        'feedback_rating': 4,
        'feedback_at': 'DYNAMIC_last_month',
        'created_at': 'DYNAMIC_last_month',
        'updated_at': 'DYNAMIC_last_month'
    },
    {
        'id': 8,
        'application_id': 3,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '王五',
        'round': '二面',
        'way': 'onsite',
        'interview_time': 'DYNAMIC_this_thursday',
        'interviewer': '王技术经理',
        'location': '上海市浦东新区陆家嘴',
        'meeting_link': '',
        'remark': '',
        'status': 'completed',
        'feedback_result': 'pass',
        'feedback_comment': '表现不错，可以发 Offer',
        'feedback_rating': 4,
        'feedback_at': 'DYNAMIC_this_thursday',
        'created_at': 'DYNAMIC_this_wednesday',
        'updated_at': 'DYNAMIC_this_thursday'
    }
]

INITIAL_OFFERS = [
    {
        'id': 1,
        'application_id': 6,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '周八',
        'position': '高级前端工程师',
        'salary_min': 28000,
        'salary_max': 35000,
        'join_date': 'DYNAMIC_offer_join_next_week',
        'probation_months': 3,
        'benefits': '六险一金、年终奖、股票期权、免费三餐、健身房',
        'attachment_note': 'Offer letter 已发送至邮箱，请查收',
        'remark': '表现优秀，薪资上浮 10%',
        'status': 'accepted',
        'sent_at': 'DYNAMIC_last_week',
        'replied_at': 'DYNAMIC_today',
        'reject_reason': '',
        'withdraw_reason': '',
        'created_at': 'DYNAMIC_last_week',
        'updated_at': 'DYNAMIC_today'
    },
    {
        'id': 2,
        'application_id': 7,
        'job_id': 3,
        'job_title': '产品经理',
        'candidate_name': '吴九',
        'position': '高级产品经理',
        'salary_min': 22000,
        'salary_max': 28000,
        'join_date': 'DYNAMIC_offer_join_next_month',
        'probation_months': 3,
        'benefits': '六险一金、年终奖、带薪年假、节日福利',
        'attachment_note': 'Offer letter 已发送',
        'remark': '',
        'status': 'sent',
        'sent_at': 'DYNAMIC_today',
        'replied_at': '',
        'reject_reason': '',
        'withdraw_reason': '',
        'created_at': 'DYNAMIC_this_tuesday',
        'updated_at': 'DYNAMIC_today'
    },
    {
        'id': 3,
        'application_id': 3,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '王五',
        'position': 'Python 后端工程师',
        'salary_min': 20000,
        'salary_max': 26000,
        'join_date': 'DYNAMIC_offer_join_next_week',
        'probation_months': 3,
        'benefits': '六险一金、年终奖、技术培训、弹性工作',
        'attachment_note': 'Offer letter 已发送',
        'remark': '',
        'status': 'rejected',
        'sent_at': 'DYNAMIC_this_wednesday',
        'replied_at': 'DYNAMIC_this_thursday',
        'reject_reason': '已接受其他公司 Offer',
        'withdraw_reason': '',
        'created_at': 'DYNAMIC_this_tuesday',
        'updated_at': 'DYNAMIC_this_thursday'
    },
    {
        'id': 4,
        'application_id': 8,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '郑十',
        'position': 'Python 后端工程师',
        'salary_min': 22000,
        'salary_max': 28000,
        'join_date': 'DYNAMIC_offer_join_today',
        'probation_months': 3,
        'benefits': '六险一金、年终奖、股票期权',
        'attachment_note': '',
        'remark': '候选人薪资期望较高，需要审批',
        'status': 'draft',
        'sent_at': '',
        'replied_at': '',
        'reject_reason': '',
        'withdraw_reason': '',
        'created_at': 'DYNAMIC_this_wednesday',
        'updated_at': 'DYNAMIC_this_wednesday'
    },
    {
        'id': 5,
        'application_id': 9,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '钱十一',
        'position': '高级前端工程师',
        'salary_min': 25000,
        'salary_max': 32000,
        'join_date': 'DYNAMIC_offer_join_next_month',
        'probation_months': 3,
        'benefits': '六险一金、年终奖、股票期权',
        'attachment_note': 'Offer letter 已发送',
        'remark': '',
        'status': 'withdrawn',
        'sent_at': 'DYNAMIC_last_month',
        'replied_at': '',
        'reject_reason': '',
        'withdraw_reason': '岗位编制调整，暂停招聘',
        'created_at': 'DYNAMIC_last_month',
        'updated_at': 'DYNAMIC_last_week_friday'
    },
    {
        'id': 6,
        'application_id': 2,
        'job_id': 1,
        'job_title': '高级前端工程师',
        'candidate_name': '李四',
        'position': '前端工程师',
        'salary_min': 18000,
        'salary_max': 25000,
        'join_date': 'DYNAMIC_offer_join_next_week',
        'probation_months': 3,
        'benefits': '六险一金、年终奖、免费三餐',
        'attachment_note': 'Offer letter 已发送至邮箱',
        'remark': '面试表现优秀，强烈推荐',
        'status': 'sent',
        'sent_at': 'DYNAMIC_today_afternoon',
        'replied_at': '',
        'reject_reason': '',
        'withdraw_reason': '',
        'created_at': 'DYNAMIC_this_tuesday',
        'updated_at': 'DYNAMIC_today_afternoon'
    },
    {
        'id': 7,
        'application_id': 5,
        'job_id': 2,
        'job_title': 'Python 后端开发工程师',
        'candidate_name': '孙七',
        'position': '高级 Python 工程师',
        'salary_min': 28000,
        'salary_max': 35000,
        'join_date': 'DYNAMIC_offer_join_next_month',
        'probation_months': 3,
        'benefits': '六险一金、年终奖、股票期权、带团队补贴',
        'attachment_note': '',
        'remark': '资深候选人，需总监审批薪资',
        'status': 'draft',
        'sent_at': '',
        'replied_at': '',
        'reject_reason': '',
        'withdraw_reason': '',
        'created_at': 'DYNAMIC_today',
        'updated_at': 'DYNAMIC_today'
    }
]


class MockDB:
    def __init__(self):
        self.reset()

    def reset(self):
        dates = _gen_dates()

        def _replace_dates(obj):
            if isinstance(obj, list):
                return [_replace_dates(item) for item in obj]
            if isinstance(obj, dict):
                return {k: _replace_dates(v) for k, v in obj.items()}
            if isinstance(obj, str) and obj.startswith('DYNAMIC_'):
                key = obj.replace('DYNAMIC_', '')
                return dates.get(key, obj)
            return obj

        self.jobs = _replace_dates(copy.deepcopy(INITIAL_JOBS))
        self.applications = _replace_dates(copy.deepcopy(INITIAL_APPLICATIONS))
        self.messages = _replace_dates(copy.deepcopy(INITIAL_MESSAGES))
        self.interviews = _replace_dates(copy.deepcopy(INITIAL_INTERVIEWS))
        self.offers = _replace_dates(copy.deepcopy(INITIAL_OFFERS))
        self.next_job_id = max(j['id'] for j in self.jobs) + 1
        self.next_application_id = max(a['id'] for a in self.applications) + 1
        self.next_message_id = max(m['id'] for m in self.messages) + 1
        self.next_interview_id = max(i['id'] for i in self.interviews) + 1
        self.next_offer_id = max((o['id'] for o in self.offers), default=0) + 1

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
        sent_offers = len([o for o in self.offers if o['status'] == 'sent'])
        accepted_offers = len([o for o in self.offers if o['status'] == 'accepted'])
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
            'sent_offers': sent_offers,
            'accepted_offers': accepted_offers,
            'status_text': STATUS_TEXT
        }

    def get_dashboard_stats(self, job_id=None, start_date=None, end_date=None):
        from datetime import datetime, timedelta
        now = datetime.now()
        today_str = now.strftime('%Y-%m-%d')
        week_start = now - timedelta(days=now.weekday())
        week_start_str = week_start.strftime('%Y-%m-%d')
        week_end_date = week_start + timedelta(days=6)
        week_end_str = week_end_date.strftime('%Y-%m-%d') + ' 23:59:59'

        end_date_full = end_date + ' 23:59:59' if end_date else None

        jobs = self.jobs
        if job_id:
            jobs = [j for j in jobs if j['id'] == job_id]
        if start_date:
            jobs = [j for j in jobs if j['created_at'] >= start_date]
        if end_date_full:
            jobs = [j for j in jobs if j['created_at'] <= end_date_full]

        apps = self.applications
        if job_id:
            apps = [a for a in apps if a['job_id'] == job_id]
        if start_date:
            apps = [a for a in apps if a['applied_at'] >= start_date]
        if end_date_full:
            apps = [a for a in apps if a['applied_at'] <= end_date_full]

        interviews = self.interviews
        if job_id:
            interviews = [i for i in interviews if i['job_id'] == job_id]
        if start_date:
            interviews = [i for i in interviews if i['interview_time'] >= start_date]
        if end_date_full:
            interviews = [i for i in interviews if i['interview_time'] <= end_date_full]

        offers = self.offers
        if job_id:
            offers = [o for o in offers if o['job_id'] == job_id]
        if start_date:
            offers = [o for o in offers if o['created_at'] >= start_date]
        if end_date_full:
            offers = [o for o in offers if o['created_at'] <= end_date_full]

        total_jobs = len(jobs)
        open_jobs = len([j for j in jobs if j['status'] == 'open'])

        total_applications = len(apps)
        pending = len([a for a in apps if a['status'] == 'pending'])
        screening = len([a for a in apps if a['status'] == 'screening'])
        communicating = len([a for a in apps if a['status'] == 'communicating'])
        rejected = len([a for a in apps if a['status'] == 'rejected'])
        hired = len([a for a in apps if a['status'] == 'hired'])
        active_applications = pending + screening + communicating

        scheduled_interviews = len([i for i in interviews if i['status'] == 'scheduled'])
        completed_interviews = len([i for i in interviews if i['status'] == 'completed'])
        cancelled_interviews = len([i for i in interviews if i['status'] == 'cancelled'])
        total_interviews = len(interviews)

        today_interviews = len([i for i in interviews if i['interview_time'].startswith(today_str)])
        week_interviews = len([i for i in interviews if i['interview_time'] >= week_start_str and i['interview_time'] <= week_end_str])

        draft_offers = len([o for o in offers if o['status'] == 'draft'])
        sent_offers = len([o for o in offers if o['status'] == 'sent'])
        accepted_offers = len([o for o in offers if o['status'] == 'accepted'])
        rejected_offers = len([o for o in offers if o['status'] == 'rejected'])
        withdrawn_offers = len([o for o in offers if o['status'] == 'withdrawn'])
        processed_offers = accepted_offers + rejected_offers + withdrawn_offers
        total_offers = len(offers)

        conversion = {
            'applications': total_applications,
            'to_interview': total_interviews,
            'interview_pass_rate': round(completed_interviews / total_interviews * 100, 1) if total_interviews > 0 else 0,
            'to_offer': total_offers,
            'offer_accept_rate': round(accepted_offers / sent_offers * 100, 1) if sent_offers > 0 else 0,
            'to_hire': hired
        }

        all_jobs_for_filter = self.jobs
        job_list = [{'id': j['id'], 'title': j['title'], 'status': j['status']} for j in all_jobs_for_filter]

        return {
            'total_jobs': total_jobs,
            'open_jobs': open_jobs,
            'closed_jobs': total_jobs - open_jobs,
            'total_applications': total_applications,
            'active_applications': active_applications,
            'pending_applications': pending,
            'screening': screening,
            'communicating': communicating,
            'rejected': rejected,
            'hired': hired,
            'total_interviews': total_interviews,
            'scheduled_interviews': scheduled_interviews,
            'completed_interviews': completed_interviews,
            'cancelled_interviews': cancelled_interviews,
            'today_interviews': today_interviews,
            'week_interviews': week_interviews,
            'total_offers': total_offers,
            'draft_offers': draft_offers,
            'sent_offers': sent_offers,
            'accepted_offers': accepted_offers,
            'rejected_offers': rejected_offers,
            'withdrawn_offers': withdrawn_offers,
            'processed_offers': processed_offers,
            'conversion': conversion,
            'job_list': job_list,
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
        if app['status'] not in ('screening', 'communicating'):
            return None, f'候选人状态为「{STATUS_TEXT[app["status"]]}」，无法安排面试，请先推进到「待沟通」或「沟通中」状态'
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
        old_round = interview['round']
        old_way = interview['way']
        old_time = interview['interview_time']
        old_interviewer = interview['interviewer']
        old_location = interview['location']
        old_meeting_link = interview['meeting_link']
        for k, v in data.items():
            if k in interview and k not in ('id', 'application_id', 'job_id', 'job_title', 'candidate_name', 'status', 'created_at'):
                interview[k] = v
        interview['updated_at'] = now_str()
        app = self.get_application(interview['application_id'])
        if app:
            changes = []
            if old_time != interview['interview_time']:
                changes.append(f'时间调整为 {interview["interview_time"]}')
            if old_way != interview['way']:
                changes.append(f'方式调整为 {INTERVIEW_WAY_TEXT[interview["way"]]}')
            if old_interviewer != interview['interviewer']:
                changes.append(f'面试官调整为 {interview["interviewer"]}')
            if old_round != interview['round']:
                changes.append(f'轮次调整为 {interview["round"]}')
            if old_location != interview['location']:
                changes.append(f'地点已更新')
            if old_meeting_link != interview['meeting_link']:
                changes.append(f'会议链接已更新')
            if changes:
                sys_msg = f'【系统消息】面试信息已更新：{interview["round"]}，{", ".join(changes)}'
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

    def submit_interview_feedback(self, interview_id, feedback):
        interview = self.get_interview(interview_id)
        if not interview:
            return None, '面试记录不存在'
        if interview['status'] not in ('scheduled', 'completed'):
            return None, '只有已安排或已完成的面试可以提交反馈'
        result = feedback.get('result')
        if result not in INTERVIEW_FEEDBACK_RESULTS:
            return None, f'无效的反馈结果: {result}'
        interview['feedback_result'] = result
        interview['feedback_comment'] = feedback.get('comment', '')
        interview['feedback_rating'] = int(feedback.get('rating', 0) or 0)
        interview['feedback_at'] = now_str()
        interview['status'] = 'completed'
        interview['updated_at'] = now_str()
        app = self.get_application(interview['application_id'])
        if app:
            result_text = INTERVIEW_FEEDBACK_RESULT_TEXT[result]
            sys_msg = f'【系统消息】{interview["round"]}反馈已提交，结果：{result_text}'
            if feedback.get('comment'):
                sys_msg += f'，评价：{feedback["comment"]}'
            self._add_system_message(interview['application_id'], sys_msg)
            if result == 'fail':
                if app['status'] != 'rejected':
                    app['status'] = 'rejected'
        return interview, None

    def get_offers(self, application_id=None, job_id=None, status=None, start_date=None, end_date=None):
        result = self.offers
        if application_id:
            result = [o for o in result if o['application_id'] == application_id]
        if job_id:
            result = [o for o in result if o['job_id'] == job_id]
        if status:
            result = [o for o in result if o['status'] == status]
        if start_date:
            result = [o for o in result if o['created_at'][:10] >= start_date]
        if end_date:
            result = [o for o in result if o['created_at'][:10] <= end_date]
        result = sorted(result, key=lambda x: x['created_at'], reverse=True)
        return result

    def get_offer(self, offer_id):
        for o in self.offers:
            if o['id'] == offer_id:
                return o
        return None

    def create_offer(self, application_id, data):
        app = self.get_application(application_id)
        if not app:
            return None, '投递记录不存在，无法创建 Offer'
        if app['status'] == 'rejected':
            return None, '该候选人状态为「不合适」，无法创建 Offer'
        passed_interviews = [i for i in self.interviews
                             if i['application_id'] == application_id
                             and i['status'] == 'completed'
                             and i['feedback_result'] == 'pass']
        if not passed_interviews:
            return None, '该候选人没有通过的面试反馈，无法创建 Offer'
        if not data.get('salary_min') or not data.get('salary_max'):
            return None, '薪资范围不能为空'
        if not data.get('join_date'):
            return None, '入职日期不能为空'
        job = self.get_job(app['job_id'])
        offer = {
            'id': self.next_offer_id,
            'application_id': application_id,
            'job_id': app['job_id'],
            'job_title': app['job_title'],
            'candidate_name': app['candidate_name'],
            'position': data.get('position', job['title'] if job else app['job_title']),
            'salary_min': data.get('salary_min', 0),
            'salary_max': data.get('salary_max', 0),
            'join_date': data.get('join_date', ''),
            'probation_months': int(data.get('probation_months', 3) or 3),
            'benefits': data.get('benefits', ''),
            'attachment_note': data.get('attachment_note', ''),
            'remark': data.get('remark', ''),
            'status': 'draft',
            'sent_at': '',
            'replied_at': '',
            'reject_reason': '',
            'withdraw_reason': '',
            'created_at': now_str(),
            'updated_at': now_str()
        }
        self.offers.insert(0, offer)
        self.next_offer_id += 1
        return offer, None

    def update_offer(self, offer_id, data):
        offer = self.get_offer(offer_id)
        if not offer:
            return None, 'Offer 不存在'
        if offer['status'] != 'draft':
            return None, '只有草稿状态的 Offer 可以编辑'
        for k, v in data.items():
            if k in offer and k not in ('id', 'application_id', 'job_id', 'job_title', 'candidate_name', 'status', 'created_at', 'sent_at', 'replied_at'):
                offer[k] = v
        offer['updated_at'] = now_str()
        return offer, None

    def send_offer(self, offer_id):
        offer = self.get_offer(offer_id)
        if not offer:
            return None, 'Offer 不存在'
        if offer['status'] != 'draft':
            return None, '只有草稿状态的 Offer 可以发送'
        offer['status'] = 'sent'
        offer['sent_at'] = now_str()
        offer['updated_at'] = now_str()
        app = self.get_application(offer['application_id'])
        if app:
            app['status'] = 'communicating'
            sys_msg = f'【系统消息】Offer 已发送，岗位：{offer["position"]}，薪资：{offer["salary_min"]}-{offer["salary_max"]}K，请查收并尽快回复。'
            self._add_system_message(offer['application_id'], sys_msg)
        return offer, None

    def accept_offer(self, offer_id):
        offer = self.get_offer(offer_id)
        if not offer:
            return None, 'Offer 不存在'
        if offer['status'] == 'accepted':
            return None, '该 Offer 已接受，请勿重复操作'
        if offer['status'] == 'rejected':
            return None, '该 Offer 已拒绝，无法接受'
        if offer['status'] == 'withdrawn':
            return None, '该 Offer 已撤回，无法接受'
        if offer['status'] == 'draft':
            return None, '该 Offer 尚未发送，无法接受'
        if offer['status'] != 'sent':
            return None, f'当前状态为「{OFFER_STATUS_TEXT.get(offer["status"], offer["status"])}」，无法接受'
        offer['status'] = 'accepted'
        offer['replied_at'] = now_str()
        offer['updated_at'] = now_str()
        app = self.get_application(offer['application_id'])
        if app:
            app['status'] = 'hired'
            sys_msg = '【系统消息】候选人已接受 Offer，入职日期：' + offer['join_date'] + '，时间：' + offer['replied_at']
            self._add_system_message(offer['application_id'], sys_msg)
        return offer, None

    def reject_offer(self, offer_id, reason=''):
        offer = self.get_offer(offer_id)
        if not offer:
            return None, 'Offer 不存在'
        if offer['status'] == 'accepted':
            return None, '该 Offer 已接受，无法拒绝'
        if offer['status'] == 'rejected':
            return None, '该 Offer 已拒绝，请勿重复操作'
        if offer['status'] == 'withdrawn':
            return None, '该 Offer 已撤回，无法拒绝'
        if offer['status'] != 'sent':
            return None, f'当前状态为「{OFFER_STATUS_TEXT.get(offer["status"], offer["status"])}」，无法拒绝'
        if not reason or not reason.strip():
            return None, '请填写拒绝原因'
        offer['status'] = 'rejected'
        offer['replied_at'] = now_str()
        offer['reject_reason'] = reason
        offer['updated_at'] = now_str()
        app = self.get_application(offer['application_id'])
        if app:
            app['status'] = 'rejected'
            sys_msg = '【系统消息】候选人已拒绝 Offer'
            if reason:
                sys_msg += f'，原因：{reason}'
            sys_msg += f'，时间：{offer["replied_at"]}'
            self._add_system_message(offer['application_id'], sys_msg)
        return offer, None

    def withdraw_offer(self, offer_id, reason=''):
        offer = self.get_offer(offer_id)
        if not offer:
            return None, 'Offer 不存在'
        if offer['status'] == 'accepted':
            return None, '该 Offer 已接受，无法撤回'
        if offer['status'] == 'rejected':
            return None, '该 Offer 已拒绝，无法撤回'
        if offer['status'] == 'withdrawn':
            return None, '该 Offer 已撤回，请勿重复操作'
        if offer['status'] not in ('draft', 'sent'):
            return None, f'当前状态为「{OFFER_STATUS_TEXT.get(offer["status"], offer["status"])}」，无法撤回'
        if not reason or not reason.strip():
            return None, '请填写撤回原因'
        old_status = offer['status']
        offer['status'] = 'withdrawn'
        offer['withdraw_reason'] = reason
        offer['updated_at'] = now_str()
        app = self.get_application(offer['application_id'])
        if app and old_status == 'sent':
            app['status'] = 'communicating'
        if app:
            sys_msg = '【系统消息】'
            if old_status == 'draft':
                sys_msg += '草稿 Offer 已撤回'
            else:
                sys_msg += 'Offer 已撤回'
            if reason:
                sys_msg += f'，原因：{reason}'
            sys_msg += f'，时间：{offer["updated_at"]}'
            self._add_system_message(offer['application_id'], sys_msg)
        return offer, None

    def get_offer_meta(self):
        return {
            'status_list': list(OFFER_STATUS),
            'status_text': OFFER_STATUS_TEXT,
            'status_type': OFFER_STATUS_TYPE
        }

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
