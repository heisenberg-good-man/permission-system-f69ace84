import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

request.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 0) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    return res.data
  },
  error => {
    ElMessage.error(error.message || '网络错误')
    return Promise.reject(error)
  }
)

export const STATUS_TEXT = {
  pending: '新投递',
  screening: '待沟通',
  communicating: '沟通中',
  rejected: '不合适',
  hired: '已录用'
}

export const STATUS_TYPE = {
  pending: 'warning',
  screening: 'primary',
  communicating: 'success',
  rejected: 'danger',
  hired: 'info'
}

export const INTERVIEW_STATUS_TEXT = {
  scheduled: '已安排',
  completed: '已完成',
  cancelled: '已取消',
  no_show: '未到场'
}

export const INTERVIEW_STATUS_TYPE = {
  scheduled: 'primary',
  completed: 'success',
  cancelled: 'info',
  no_show: 'danger'
}

export const INTERVIEW_WAY_TEXT = {
  onsite: '现场面试',
  online: '视频面试',
  phone: '电话面试'
}

export const INTERVIEW_ROUNDS = ['初筛', '一面', '二面', '三面', '终面', 'HR面']

export const INTERVIEW_FEEDBACK_RESULT_TEXT = {
  pass: '通过',
  fail: '未通过',
  pending: '待定'
}

export const INTERVIEW_FEEDBACK_RESULT_TYPE = {
  pass: 'success',
  fail: 'danger',
  pending: 'warning'
}

export const OFFER_STATUS_TEXT = {
  draft: '草稿',
  sent: '已发送',
  accepted: '候选人已接受',
  rejected: '候选人已拒绝',
  withdrawn: '已撤回'
}

export const OFFER_STATUS_TYPE = {
  draft: 'info',
  sent: 'primary',
  accepted: 'success',
  rejected: 'danger',
  withdrawn: 'warning'
}

export const api = {
  getStats: () => request.get('/stats'),
  getStatusMeta: () => request.get('/status-meta'),

  getJobs: (status) => request.get('/jobs', { params: { status } }),
  getJob: (id) => request.get(`/jobs/${id}`),
  createJob: (data) => request.post('/jobs', data),
  updateJob: (id, data) => request.put(`/jobs/${id}`, data),
  deleteJob: (id) => request.delete(`/jobs/${id}`),
  getJobApplications: (jobId, status) => request.get(`/jobs/${jobId}/applications`, { params: { status } }),

  getApplications: (params) => request.get('/applications', { params }),
  getApplication: (id) => request.get(`/applications/${id}`),
  applyJob: (jobId, data) => request.post(`/jobs/${jobId}/apply`, data),
  updateApplicationStatus: (id, status) => request.put(`/applications/${id}/status`, { status }),

  getMessages: (appId) => request.get(`/applications/${appId}/messages`),
  sendMessage: (appId, data) => request.post(`/applications/${appId}/messages`, data),

  getInterviews: (params) => request.get('/interviews', { params }),
  getInterview: (id) => request.get(`/interviews/${id}`),
  getApplicationInterviews: (appId) => request.get(`/applications/${appId}/interviews`),
  createInterview: (appId, data) => request.post(`/applications/${appId}/interviews`, data),
  updateInterview: (id, data) => request.put(`/interviews/${id}`, data),
  cancelInterview: (id, reason) => request.post(`/interviews/${id}/cancel`, { reason }),
  submitInterviewFeedback: (id, data) => request.post(`/interviews/${id}/feedback`, data),
  getInterviewMeta: () => request.get('/interview-meta'),

  getOffers: (params) => request.get('/offers', { params }),
  getOffer: (id) => request.get(`/offers/${id}`),
  createOffer: (appId, data) => request.post(`/applications/${appId}/offers`, data),
  updateOffer: (id, data) => request.put(`/offers/${id}`, data),
  sendOffer: (id) => request.post(`/offers/${id}/send`),
  acceptOffer: (id) => request.post(`/offers/${id}/accept`),
  rejectOffer: (id, reason) => request.post(`/offers/${id}/reject`, { reason }),
  withdrawOffer: (id, reason) => request.post(`/offers/${id}/withdraw`, { reason }),
  getOfferMeta: () => request.get('/offer-meta'),

  resetData: () => request.post('/reset')
}

export default request
