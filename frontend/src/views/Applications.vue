<template>
  <div class="page-container applications-page">
    <div class="page-header card">
      <div class="page-title">
        <el-icon><User /></el-icon>
        候选人管理
      </div>
      <div class="header-actions">
        <el-select v-model="jobFilter" placeholder="全部职位" clearable style="width: 200px" @change="fetchData">
          <el-option v-for="j in jobs" :key="j.id" :label="j.title" :value="j.id" />
        </el-select>
        <el-radio-group v-model="statusFilter" size="default" @change="fetchData">
          <el-radio-button value="">全部</el-radio-button>
          <el-radio-button value="pending">
            <el-icon><Bell /></el-icon>
            新投递 ({{ statusCount.pending }})
          </el-radio-button>
          <el-radio-button value="screening">
            <el-icon><Clock /></el-icon>
            待沟通 ({{ statusCount.screening }})
          </el-radio-button>
          <el-radio-button value="communicating">
            <el-icon><ChatDotRound /></el-icon>
            沟通中 ({{ statusCount.communicating }})
          </el-radio-button>
          <el-radio-button value="rejected">
            <el-icon><Close /></el-icon>
            不合适 ({{ statusCount.rejected }})
          </el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <div class="content-layout">
      <div class="candidate-list card">
        <div class="list-header">
          <span class="list-title">候选人列表</span>
          <span class="list-count">共 {{ filteredApps.length }} 人</span>
        </div>
        <div class="candidate-items">
          <div
            v-for="app in filteredApps"
            :key="app.id"
            class="candidate-item"
            :class="{ active: selectedId === app.id }"
            @click="selectCandidate(app)"
          >
            <div class="candidate-avatar">
              {{ app.candidate_name.charAt(0) }}
            </div>
            <div class="candidate-info">
              <div class="info-top">
                <span class="name">{{ app.candidate_name }}</span>
                <el-tag :type="STATUS_TYPE[app.status]" size="small" effect="light">
                  {{ STATUS_TEXT[app.status] }}
                </el-tag>
              </div>
              <div class="info-mid">
                <el-icon><Briefcase /></el-icon>
                {{ app.job_title }}
              </div>
              <div class="info-bottom">
                <span><el-icon><Reading /></el-icon> {{ app.education }}</span>
                <span><el-icon><Clock /></el-icon> {{ app.experience }}</span>
                <span class="time">{{ formatTime(app.applied_at) }}</span>
              </div>
            </div>
          </div>
          <el-empty v-if="filteredApps.length === 0" description="暂无候选人" :image-size="60" />
        </div>
      </div>

      <div class="candidate-detail card" v-if="selectedApp">
        <div class="detail-header">
          <div>
            <h3 class="detail-name">{{ selectedApp.candidate_name }}</h3>
            <div class="detail-subtitle">
              应聘：{{ selectedApp.job_title }}
              <el-tag :type="STATUS_TYPE[selectedApp.status]" style="margin-left: 8px">
                {{ STATUS_TEXT[selectedApp.status] }}
              </el-tag>
            </div>
          </div>
          <div class="detail-actions">
            <el-button type="primary" @click="goToComm(selectedApp.id)">
              <el-icon><ChatDotRound /></el-icon>
              发起沟通
            </el-button>
            <el-dropdown trigger="click" @command="handleStatusChange">
              <el-button>
                推进状态
                <el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item
                    v-for="s in availableStatuses"
                    :key="s.value"
                    :disabled="selectedApp.status === s.value"
                    :command="s.value"
                  >
                    <el-tag :type="s.type" size="small" effect="dark">{{ s.label }}</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item divided disabled v-if="availableStatuses.length === 0">
                    当前状态无可推进选项
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>

        <el-tabs v-model="activeTab" class="detail-tabs">
          <el-tab-pane label="简历详情" name="resume">
            <el-descriptions :column="2" border size="default">
              <el-descriptions-item label="姓名">{{ selectedApp.candidate_name }}</el-descriptions-item>
              <el-descriptions-item label="应聘职位">{{ selectedApp.job_title }}</el-descriptions-item>
              <el-descriptions-item label="手机号">{{ selectedApp.candidate_phone }}</el-descriptions-item>
              <el-descriptions-item label="邮箱">{{ selectedApp.candidate_email }}</el-descriptions-item>
              <el-descriptions-item label="学历">{{ selectedApp.education }}</el-descriptions-item>
              <el-descriptions-item label="工作经验">{{ selectedApp.experience }}</el-descriptions-item>
              <el-descriptions-item label="投递时间" :span="2">{{ selectedApp.applied_at }}</el-descriptions-item>
            </el-descriptions>

            <div class="resume-section">
              <h4 class="section-title">
                <el-icon><Document /></el-icon>
                简历内容
              </h4>
              <div class="resume-content">{{ selectedApp.resume || '暂无简历内容' }}</div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="沟通记录" name="messages">
            <div class="messages-preview">
              <div v-if="messages.length === 0" class="no-messages">
                <el-empty description="暂无沟通记录" :image-size="60" />
                <el-button type="primary" @click="goToComm(selectedApp.id)">
                  发起第一次沟通
                </el-button>
              </div>
              <div v-else class="msg-list">
                <div v-for="msg in messages.slice(-5)" :key="msg.id" class="msg-item" :class="msg.sender">
                  <div class="msg-avatar">{{ msg.sender_name.charAt(0) }}</div>
                  <div class="msg-body">
                    <div class="msg-head">
                      <span class="msg-sender">{{ msg.sender_name }}</span>
                      <span class="msg-time">{{ msg.created_at }}</span>
                    </div>
                    <div class="msg-text">{{ msg.content }}</div>
                  </div>
                </div>
              </div>
              <div class="msg-more" v-if="messages.length > 5">
                <el-button type="primary" link @click="goToComm(selectedApp.id)">
                  查看全部 {{ messages.length }} 条消息 →
                </el-button>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <div class="candidate-detail card empty-detail" v-else>
        <el-empty description="请选择一位候选人查看详情" :image-size="80" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { api } from '../api'

const router = useRouter()
const refreshStats = inject('refreshStats')
const STATUS_TEXT = inject('STATUS_TEXT')
const STATUS_TYPE = inject('STATUS_TYPE')

const jobs = ref([])
const applications = ref([])
const messages = ref([])
const jobFilter = ref('')
const statusFilter = ref('')
const selectedId = ref(null)
const activeTab = ref('resume')

const STATUS_FLOW = {
  pending: ['screening', 'communicating', 'rejected'],
  screening: ['communicating', 'rejected', 'pending'],
  communicating: ['rejected', 'hired', 'screening', 'pending'],
  rejected: ['pending', 'screening'],
  hired: []
}

const selectedApp = computed(() => {
  return applications.value.find(a => a.id === selectedId.value) || null
})

const filteredApps = computed(() => {
  return applications.value.filter(a => {
    if (jobFilter.value && a.job_id !== jobFilter.value) return false
    if (statusFilter.value && a.status !== statusFilter.value) return false
    return true
  })
})

const statusCount = computed(() => {
  const count = { pending: 0, screening: 0, communicating: 0, rejected: 0, hired: 0 }
  const list = jobFilter.value
    ? applications.value.filter(a => a.job_id === jobFilter.value)
    : applications.value
  list.forEach(a => {
    if (count[a.status] !== undefined) count[a.status]++
  })
  return count
})

const availableStatuses = computed(() => {
  if (!selectedApp.value) return []
  const current = selectedApp.value.status
  const next = STATUS_FLOW[current] || []
  return next.map(s => ({
    value: s,
    label: STATUS_TEXT[s],
    type: STATUS_TYPE[s]
  }))
})

const formatTime = (t) => {
  if (!t) return ''
  return t.substring(5, 16)
}

const fetchData = async () => {
  const [jobsData, appsData] = await Promise.all([
    api.getJobs(),
    api.getApplications({ job_id: jobFilter.value || undefined, status: statusFilter.value || undefined })
  ])
  jobs.value = jobsData
  applications.value = appsData
  if (selectedId.value && !appsValueContains(selectedId.value)) {
    if (appsData.length > 0) {
      selectCandidate(appsData[0])
    } else {
      selectedId.value = null
    }
  }
}

const appsValueContains = (id) => {
  return applications.value.some(a => a.id === id)
}

const selectCandidate = async (app) => {
  selectedId.value = app.id
  activeTab.value = 'resume'
  try {
    messages.value = await api.getMessages(app.id)
  } catch (e) {
    messages.value = []
    ElMessage.error(e.message || '加载沟通记录失败')
  }
}

const handleStatusChange = async (newStatus) => {
  if (!selectedId.value) return
  try {
    await api.updateApplicationStatus(selectedId.value, newStatus)
    const app = applications.value.find(a => a.id === selectedId.value)
    if (app) app.status = newStatus
    ElMessage.success(`状态已更新为「${STATUS_TEXT[newStatus]}」`)
    refreshStats()
    if (activeTab.value === 'messages') {
      try {
        messages.value = await api.getMessages(selectedId.value)
      } catch (e) {}
    }
  } catch (e) {
    ElMessage.error(e.message || '状态更新失败')
  }
}

const goToComm = (id) => {
  router.push(`/communication/${id}`)
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.content-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 16px;
  height: calc(100vh - 260px);
}

.candidate-list {
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.list-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.list-title {
  font-weight: 600;
  color: #1f2937;
}

.list-count {
  font-size: 13px;
  color: #6b7280;
}

.candidate-items {
  flex: 1;
  overflow-y: auto;
}

.candidate-item {
  display: flex;
  padding: 14px 20px;
  cursor: pointer;
  border-bottom: 1px solid #f9fafb;
  transition: background 0.2s;
}

.candidate-item:hover {
  background: #f5f7fa;
}

.candidate-item.active {
  background: #ecf5ff;
  border-left: 3px solid #409eff;
  padding-left: 17px;
}

.candidate-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  margin-right: 12px;
  flex-shrink: 0;
}

.candidate-info {
  flex: 1;
  min-width: 0;
}

.info-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.name {
  font-weight: 600;
  font-size: 15px;
  color: #1f2937;
}

.info-mid {
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.info-bottom {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #6b7280;
  align-items: center;
}

.info-bottom span {
  display: flex;
  align-items: center;
  gap: 3px;
}

.info-bottom .time {
  margin-left: auto;
  color: #9ca3af;
}

.candidate-detail {
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.detail-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.detail-name {
  font-size: 22px;
  margin: 0 0 6px 0;
  color: #1f2937;
}

.detail-subtitle {
  font-size: 14px;
  color: #6b7280;
}

.detail-actions {
  display: flex;
  gap: 8px;
}

.detail-tabs {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.detail-tabs :deep(.el-tabs__content) {
  flex: 1;
  overflow-y: auto;
  padding: 0 24px 24px;
}

.detail-tabs :deep(.el-tab-pane) {
  height: 100%;
}

.resume-section {
  margin-top: 20px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.resume-content {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  line-height: 1.8;
  color: #4b5563;
  white-space: pre-wrap;
  font-size: 14px;
}

.messages-preview {
  padding-top: 8px;
}

.no-messages {
  text-align: center;
  padding: 40px 0;
}

.no-messages .el-button {
  margin-top: 16px;
}

.msg-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.msg-item {
  display: flex;
  gap: 10px;
}

.msg-item.recruiter {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 12px;
  color: #fff;
  flex-shrink: 0;
}

.msg-item.candidate .msg-avatar {
  background: #10b981;
}

.msg-item.recruiter .msg-avatar {
  background: #6366f1;
}

.msg-body {
  max-width: 70%;
}

.msg-head {
  font-size: 11px;
  color: #9ca3af;
  margin-bottom: 4px;
  display: flex;
  gap: 10px;
}

.msg-item.recruiter .msg-head {
  justify-content: flex-end;
}

.msg-text {
  padding: 8px 12px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #e5e7eb;
  font-size: 13px;
  line-height: 1.5;
}

.msg-item.recruiter .msg-text {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.msg-more {
  text-align: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.empty-detail {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
