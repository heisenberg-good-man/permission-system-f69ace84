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

export const api = {
  getStats: () => request.get('/stats'),

  getJobs: (status) => request.get('/jobs', { params: { status } }),
  getJob: (id) => request.get(`/jobs/${id}`),
  createJob: (data) => request.post('/jobs', data),
  updateJob: (id, data) => request.put(`/jobs/${id}`, data),
  deleteJob: (id) => request.delete(`/jobs/${id}`),

  getApplications: (params) => request.get('/applications', { params }),
  getApplication: (id) => request.get(`/applications/${id}`),
  applyJob: (jobId, data) => request.post(`/jobs/${jobId}/apply`, data),
  updateApplicationStatus: (id, status) => request.put(`/applications/${id}/status`, { status }),

  getMessages: (appId) => request.get(`/applications/${appId}/messages`),
  sendMessage: (appId, data) => request.post(`/applications/${appId}/messages`, data),

  resetData: () => request.post('/reset')
}

export default request
