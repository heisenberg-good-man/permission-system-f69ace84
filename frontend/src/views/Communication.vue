<template>
  <div class="page-container communication-page">
    <div class="comm-layout">
      <div class="sidebar card">
        <div class="sidebar-header">
          <h3>
            <el-icon><ChatDotRound /></el-icon>
            {{ isRecruiterSide ? '候选人列表' : '我的沟通' }}
          </h3>
          <el-select v-if="isRecruiter" v-model="jobFilter" placeholder="筛选职位" clearable size="small" style="width: 100%; margin-top: 8px" @change="fetchAppList">
            <el-option v-for="j in jobs" :key="j.id" :label="j.title" :value="j.id" />
          </el-select>
        </div>
        <div class="candidate-list">
          <div
            v-for="app in appList"
            :key="app.id"
            class="candidate-item"
            :class="{ active: currentAppId === app.id }"
            @click="selectApp(app.id)"
          >
            <div class="avatar" :class="app.status">
              {{ (app.candidate_name || '?').charAt(0) }}
            </div>
            <div class="info">
              <div class="name-row">
                <span class="name">{{ isRecruiterSide ? app.candidate_name : app.job_title }}</span>
                <el-tag :type="STATUS_TYPE[app.status]" size="small" effect="light">
                  {{ STATUS_TEXT[app.status] }}
                </el-tag>
              </div>
              <div class="sub">
                {{ isRecruiterSide ? app.job_title : 'HR 沟通' }}
              </div>
              <div class="time">{{ formatTime(app.applied_at) }}</div>
            </div>
          </div>
          <el-empty v-if="appList.length === 0" description="暂无记录" :image-size="60" />
        </div>
      </div>

      <div class="chat-area card">
        <div v-if="currentApp" class="chat-header">
          <div>
            <div class="chat-title">
              <span class="name">{{ isRecruiterSide ? currentApp.candidate_name : currentApp.job_title }}</span>
              <el-tag :type="STATUS_TYPE[currentApp.status]">{{ STATUS_TEXT[currentApp.status] }}</el-tag>
            </div>
            <div class="chat-sub">
              {{ isRecruiterSide ? `应聘: ${currentApp.job_title}` : `候选人: ${currentApp.candidate_name}` }}
              <span v-if="isRecruiterSide" class="divider">|</span>
              <span v-if="isRecruiterSide">{{ currentApp.candidate_phone }}</span>
            </div>
          </div>
          <div v-if="isRecruiter" class="status-actions">
            <el-dropdown trigger="click" @command="changeStatus">
              <el-button type="primary">
                推进状态
                <el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item
                    v-for="s in availableStatuses"
                    :key="s.value"
                    :command="s.value"
                  >
                    <el-tag :type="s.type" size="small" effect="dark">{{ s.label }}</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item divided disabled v-if="availableStatuses.length === 0">
                    无可推进状态
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <div v-else-if="isHiringManager" class="status-actions">
            <el-tag type="info" effect="light">只读查看</el-tag>
          </div>
        </div>

        <div v-else class="empty-chat">
          <el-icon :size="48" color="#c0c4cc"><ChatDotRound /></el-icon>
          <p>请选择一位候选人开始沟通</p>
        </div>

        <div v-if="currentApp && loadError" class="load-error">
          <el-result icon="error" :title="loadError" sub-title="该投递记录可能已被删除或不存在">
            <template #extra>
              <el-button type="primary" @click="fetchAppList">刷新列表</el-button>
            </template>
          </el-result>
        </div>

        <div v-else-if="currentApp" class="timeline-container">
          <CommunicationTimeline
            :messages="messages"
            :interviews="interviews"
            :offers="offers"
            :loading="timelineLoading"
            :error-msg="timelineError"
            :auto-scroll="true"
          />
        </div>

        <div v-if="currentApp && !loadError && isRecruiter" class="input-area">
          <div v-if="sendError" class="send-error-banner">
            <el-alert :title="sendError" type="error" :closable="false" show-icon size="small" />
          </div>
          <el-input
            v-model="inputMsg"
            type="textarea"
            :rows="3"
            placeholder="输入消息，按 Enter 发送，Shift+Enter 换行"
            @keydown.enter.exact.prevent="sendMsg"
          />
          <div class="send-row">
            <el-button type="primary" @click="sendMsg" :loading="sending">
              <el-icon><Promotion /></el-icon>
              发送
            </el-button>
          </div>
        </div>

        <div v-if="currentApp && !loadError && isHiringManager" class="readonly-footer">
          <el-alert title="招聘负责人仅可查看沟通记录，无法发送消息或操作状态" type="info" :closable="false" show-icon />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, provide } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowDown, Promotion } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { api, OFFER_STATUS_TEXT } from '../api'
import CommunicationTimeline from '../components/CommunicationTimeline.vue'

const route = useRoute()
const role = inject('role')
const isRecruiter = inject('isRecruiter')
const isHiringManager = inject('isHiringManager')
const isRecruiterSide = inject('isRecruiterSide')
const refreshStats = inject('refreshStats')
const STATUS_TEXT = inject('STATUS_TEXT')
const STATUS_TYPE = inject('STATUS_TYPE')

provide('OFFER_STATUS_TEXT', OFFER_STATUS_TEXT)

const STATUS_FLOW = {
  pending: ['screening', 'communicating', 'rejected'],
  screening: ['communicating', 'rejected', 'pending'],
  communicating: ['rejected', 'hired', 'screening', 'pending'],
  rejected: ['pending', 'screening'],
  hired: []
}

const jobs = ref([])
const appList = ref([])
const currentAppId = ref(null)
const currentApp = ref(null)
const messages = ref([])
const interviews = ref([])
const offers = ref([])
const inputMsg = ref('')
const sending = ref(false)
const sendError = ref('')
const timelineLoading = ref(false)
const timelineError = ref('')
const msgContainer = ref(null)
const jobFilter = ref('')
const loadError = ref('')

const availableStatuses = computed(() => {
  if (!currentApp.value) return []
  const current = currentApp.value.status
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

const fetchAppList = async () => {
  try {
    const [jobsData, appsData] = await Promise.all([
      api.getJobs(),
      api.getApplications({ job_id: jobFilter.value || undefined })
    ])
    jobs.value = jobsData
    appList.value = appsData
  } catch (e) {}
}

const loadTimelineData = async (appId) => {
  timelineLoading.value = true
  timelineError.value = ''
  try {
    const [msgs, ivs, ofs] = await Promise.all([
      api.getMessages(appId),
      api.getApplicationInterviews(appId),
      api.getOffers({ application_id: appId })
    ])
    messages.value = msgs
    interviews.value = ivs
    offers.value = ofs
  } catch (e) {
    timelineError.value = e.message || '加载失败'
    messages.value = []
    interviews.value = []
    offers.value = []
  } finally {
    timelineLoading.value = false
  }
}

const selectApp = async (id) => {
  currentAppId.value = id
  loadError.value = ''
  sendError.value = ''
  const app = appList.value.find(a => a.id === id)
  currentApp.value = app || null
  await loadTimelineData(id)
}

const sendMsg = async () => {
  if (!inputMsg.value.trim()) return
  if (!currentAppId.value) return
  sending.value = true
  sendError.value = ''
  try {
    const sender = role.value
    const senderName = role.value === 'recruiter' ? '李经理' : (currentApp.value?.candidate_name || '候选人')
    await api.sendMessage(currentAppId.value, {
      sender,
      sender_name: senderName,
      content: inputMsg.value
    })
    inputMsg.value = ''
    await loadTimelineData(currentAppId.value)
    if (role.value === 'recruiter' && currentApp.value?.status === 'pending') {
      try {
        await api.updateApplicationStatus(currentAppId.value, 'screening')
        currentApp.value.status = 'screening'
        const app = appList.value.find(a => a.id === currentAppId.value)
        if (app) app.status = 'screening'
        refreshStats()
      } catch (e) {}
    }
  } catch (e) {
    sendError.value = e.message || '发送失败'
  } finally {
    sending.value = false
  }
}

const changeStatus = async (status) => {
  if (!currentAppId.value) return
  try {
    await api.updateApplicationStatus(currentAppId.value, status)
    if (currentApp.value) currentApp.value.status = status
    const app = appList.value.find(a => a.id === currentAppId.value)
    if (app) app.status = status
    ElMessage.success(`状态已更新为「${STATUS_TEXT[status]}」`)
    refreshStats()
  } catch (e) {
    ElMessage.error(e.message || '状态更新失败')
  }
}

onMounted(async () => {
  await fetchAppList()
  if (route.params.id) {
    const id = Number(route.params.id)
    if (appList.value.some(a => a.id === id)) {
      selectApp(id)
    } else {
      ElMessage.warning('指定的投递记录不存在，已显示第一条')
      if (appList.value.length > 0) {
        selectApp(appList.value[0].id)
      }
    }
  } else if (appList.value.length > 0) {
    selectApp(appList.value[0].id)
  }
})
</script>

<style scoped>
.communication-page {
  height: calc(100vh - 180px);
  padding: 20px;
}

.comm-layout {
  display: flex;
  height: 100%;
  gap: 16px;
}

.sidebar {
  width: 300px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.sidebar-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 16px;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 8px;
}

.candidate-list {
  flex: 1;
  overflow-y: auto;
}

.candidate-item {
  display: flex;
  padding: 12px 16px;
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
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 12px;
  flex-shrink: 0;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
}

.avatar.pending {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
}

.avatar.screening {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.avatar.communicating {
  background: linear-gradient(135deg, #10b981, #34d399);
}

.avatar.rejected {
  background: linear-gradient(135deg, #6b7280, #9ca3af);
}

.info {
  flex: 1;
  min-width: 0;
}

.name-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.name {
  font-weight: 600;
  font-size: 14px;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sub {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.time {
  font-size: 11px;
  color: #9ca3af;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.chat-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-title {
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-sub {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
}

.divider {
  margin: 0 8px;
  color: #d1d5db;
}

.empty-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  gap: 12px;
}

.empty-chat p {
  margin: 0;
}

.load-error {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-container {
  flex: 1;
  overflow: hidden;
}

.input-area {
  padding: 12px 16px;
  border-top: 1px solid #f0f0f0;
  background: #fff;
}

.send-error-banner {
  margin-bottom: 8px;
}

.send-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.readonly-footer {
  padding: 12px 16px;
  border-top: 1px solid #f0f0f0;
  background: #fff;
}
</style>
