<template>
  <div class="page-container job-detail-page">
    <el-page-header @back="$router.back()" class="back-header">
      <template #content>
        <span>职位详情</span>
      </template>
    </el-page-header>

    <div v-if="loading" class="loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <div v-else-if="job" class="detail-content">
      <div class="card job-main">
        <div class="job-header">
          <div>
            <h1 class="job-title">{{ job.title }}</h1>
            <div class="job-tags">
              <el-tag :type="job.status === 'open' ? 'success' : 'info'">
                {{ job.status === 'open' ? '招聘中' : '已关闭' }}
              </el-tag>
              <el-tag type="warning">{{ job.experience }}</el-tag>
              <el-tag type="info">{{ job.education }}</el-tag>
              <span v-if="role === 'recruiter'" class="apply-count">
                <el-icon><User /></el-icon>
                投递 {{ applications.length }} 人
              </span>
            </div>
          </div>
          <div class="job-salary">{{ formatSalary(job.salary_min, job.salary_max) }}</div>
        </div>

        <div class="job-info-row">
          <div class="info-item">
            <el-icon><OfficeBuilding /></el-icon>
            <span>{{ job.company }} · {{ job.department }}</span>
          </div>
          <div class="info-item">
            <el-icon><Location /></el-icon>
            <span>{{ job.city }}</span>
          </div>
          <div class="info-item">
            <el-icon><User /></el-icon>
            <span>HR: {{ job.hr_name }}</span>
          </div>
          <div class="info-item">
            <el-icon><Clock /></el-icon>
            <span>发布于 {{ job.created_at }}</span>
          </div>
        </div>
      </div>

      <div class="detail-body">
        <div class="left-section">
          <div class="card">
            <h3 class="section-title">
              <el-icon><Document /></el-icon>
              职位描述
            </h3>
            <div class="section-content">{{ job.description }}</div>
          </div>

          <div class="card">
            <h3 class="section-title">
              <el-icon><List /></el-icon>
              任职要求
            </h3>
            <div class="section-content" style="white-space: pre-line">{{ job.requirements }}</div>
          </div>

          <div v-if="role === 'recruiter'" class="card">
            <div class="section-header">
              <h3 class="section-title">
                <el-icon><User /></el-icon>
                候选人列表 ({{ applications.length }})
              </h3>
              <el-radio-group v-model="appStatusFilter" size="small" @change="filterApps">
                <el-radio-button value="">全部</el-radio-button>
                <el-radio-button value="pending">新投递</el-radio-button>
                <el-radio-button value="screening">待沟通</el-radio-button>
                <el-radio-button value="communicating">沟通中</el-radio-button>
                <el-radio-button value="rejected">不合适</el-radio-button>
              </el-radio-group>
            </div>

            <el-table :data="filteredApps" v-if="filteredApps.length > 0" size="default" stripe>
              <el-table-column prop="candidate_name" label="姓名" width="100" />
              <el-table-column prop="education" label="学历" width="80" />
              <el-table-column prop="experience" label="经验" width="90" />
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="STATUS_TYPE[row.status]" size="small">{{ STATUS_TEXT[row.status] }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="applied_at" label="投递时间" width="160" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="goToComm(row.id)">
                    沟通
                  </el-button>
                  <el-dropdown trigger="click" @command="(v) => changeAppStatus(row, v)">
                    <el-button link size="small">
                      推进状态<el-icon><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item
                          v-for="s in getNextStatuses(row.status)"
                          :key="s.value"
                          :command="s.value"
                        >
                          <el-tag :type="s.type" size="small" effect="dark">{{ s.label }}</el-tag>
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </template>
              </el-table-column>
            </el-table>
            <el-empty v-else description="暂无投递" :image-size="80" />
          </div>
        </div>

        <div class="right-section">
          <div v-if="role === 'candidate' && job.status === 'open'" class="card apply-card">
            <h3 class="section-title">
              <el-icon><EditPen /></el-icon>
              投递简历
            </h3>
            <el-form :model="form" label-position="top">
              <el-form-item label="姓名">
                <el-input v-model="form.candidate_name" placeholder="请输入姓名" />
              </el-form-item>
              <el-form-item label="手机号">
                <el-input v-model="form.candidate_phone" placeholder="请输入手机号" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="form.candidate_email" placeholder="请输入邮箱" />
              </el-form-item>
              <el-form-item label="学历">
                <el-select v-model="form.education" placeholder="请选择" style="width: 100%">
                  <el-option label="大专" value="大专" />
                  <el-option label="本科" value="本科" />
                  <el-option label="硕士" value="硕士" />
                  <el-option label="博士" value="博士" />
                </el-select>
              </el-form-item>
              <el-form-item label="工作经验">
                <el-select v-model="form.experience" placeholder="请选择" style="width: 100%">
                  <el-option label="应届生" value="应届生" />
                  <el-option label="1-3年" value="1-3年" />
                  <el-option label="3-5年" value="3-5年" />
                  <el-option label="5-10年" value="5-10年" />
                  <el-option label="10年以上" value="10年以上" />
                </el-select>
              </el-form-item>
              <el-form-item label="简历">
                <el-input
                  v-model="form.resume"
                  type="textarea"
                  :rows="5"
                  placeholder="请输入简历内容或自我评价"
                />
              </el-form-item>
              <el-button type="primary" style="width: 100%" @click="submitApply" :loading="submitting">
                立即投递
              </el-button>
            </el-form>
          </div>

          <div v-else-if="role === 'candidate' && job.status !== 'open'" class="card">
            <el-empty description="该职位已关闭，无法投递" :image-size="80" />
          </div>

          <div v-if="role === 'recruiter'" class="card">
            <h3 class="section-title">
              <el-icon><Setting /></el-icon>
              职位操作
            </h3>
            <div class="action-buttons">
              <el-button type="primary" style="width: 100%; margin-bottom: 8px" @click="toggleStatus">
                {{ job.status === 'open' ? '关闭招聘' : '开启招聘' }}
              </el-button>
              <el-button style="width: 100%; margin-bottom: 8px" @click="goToManage">
                返回职位管理
              </el-button>
              <el-button type="danger" plain style="width: 100%" @click="goToCandidates">
                查看全部候选人
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Loading, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { api } from '../api'

const route = useRoute()
const router = useRouter()
const role = inject('role')
const refreshStats = inject('refreshStats')
const STATUS_TEXT = inject('STATUS_TEXT')
const STATUS_TYPE = inject('STATUS_TYPE')

const job = ref(null)
const loading = ref(false)
const submitting = ref(false)
const applications = ref([])
const appStatusFilter = ref('')

const STATUS_FLOW = {
  pending: ['screening', 'communicating', 'rejected'],
  screening: ['communicating', 'rejected', 'pending'],
  communicating: ['rejected', 'hired', 'screening', 'pending'],
  rejected: ['pending', 'screening'],
  hired: []
}

const form = ref({
  candidate_name: '',
  candidate_phone: '',
  candidate_email: '',
  education: '',
  experience: '',
  resume: ''
})

const filteredApps = computed(() => {
  if (!appStatusFilter.value) return applications.value
  return applications.value.filter(a => a.status === appStatusFilter.value)
})

const fetchJob = async () => {
  loading.value = true
  try {
    job.value = await api.getJob(route.params.id)
    if (role.value === 'recruiter') {
      applications.value = await api.getApplications({ job_id: route.params.id })
    }
  } finally {
    loading.value = false
  }
}

const filterApps = () => {}

const formatSalary = (min, max) => {
  if (!min && !max) return '面议'
  return `${(min / 1000).toFixed(0)}K - ${(max / 1000).toFixed(0)}K`
}

const getNextStatuses = (current) => {
  const next = STATUS_FLOW[current] || []
  return next.map(s => ({
    value: s,
    label: STATUS_TEXT[s],
    type: STATUS_TYPE[s]
  }))
}

const submitApply = async () => {
  if (!form.value.candidate_name) {
    ElMessage.warning('请输入姓名')
    return
  }
  submitting.value = true
  try {
    await api.applyJob(route.params.id, form.value)
    ElMessage.success('投递成功！')
    form.value = {
      candidate_name: '',
      candidate_phone: '',
      candidate_email: '',
      education: '',
      experience: '',
      resume: ''
    }
    refreshStats()
  } catch (e) {
    ElMessage.error(e.message || '投递失败')
  } finally {
    submitting.value = false
  }
}

const toggleStatus = async () => {
  const newStatus = job.value.status === 'open' ? 'closed' : 'open'
  try {
    await api.updateJob(route.params.id, { status: newStatus })
    job.value.status = newStatus
    ElMessage.success(newStatus === 'open' ? '已开启招聘' : '已关闭招聘')
    refreshStats()
  } catch (e) {
    ElMessage.error(e.message || '操作失败')
  }
}

const changeAppStatus = async (row, newStatus) => {
  try {
    await api.updateApplicationStatus(row.id, newStatus)
    row.status = newStatus
    ElMessage.success(`状态已更新为「${STATUS_TEXT[newStatus]}」`)
    refreshStats()
  } catch (e) {
    ElMessage.error(e.message || '状态更新失败')
  }
}

const goToComm = (id) => {
  router.push(`/communication/${id}`)
}

const goToManage = () => {
  router.push('/job-manage')
}

const goToCandidates = () => {
  router.push('/applications')
}

onMounted(() => {
  fetchJob()
})
</script>

<style scoped>
.job-detail-page {
  max-width: 1200px;
  margin: 0 auto;
}

.back-header {
  margin-bottom: 16px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #909399;
}

.loading p {
  margin-top: 12px;
}

.job-main {
  margin-bottom: 16px;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.job-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: #1f2937;
}

.job-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}

.apply-count {
  margin-left: 8px;
  font-size: 13px;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 4px;
}

.job-salary {
  font-size: 28px;
  font-weight: 700;
  color: #f56c6c;
  white-space: nowrap;
}

.job-info-row {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #6b7280;
  font-size: 14px;
}

.detail-body {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-content {
  color: #4b5563;
  line-height: 1.8;
  font-size: 14px;
}

.apply-card {
  position: sticky;
  top: 20px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
}

@media (max-width: 900px) {
  .detail-body {
    grid-template-columns: 1fr;
  }
}
</style>
