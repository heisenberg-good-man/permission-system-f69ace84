<template>
  <div class="page-container communication-page">
    <div class="comm-layout">
      <div class="sidebar card">
        <div class="sidebar-header">
          <h3>
            <el-icon><ChatDotRound /></el-icon>
            {{ role === 'recruiter' ? '候选人列表' : '我的沟通' }}
          </h3>
        </div>
        <div class="candidate-list">
          <div
            v-for="app in appList"
            :key="app.id"
            class="candidate-item"
            :class="{ active: currentAppId === app.id }"
            @click="selectApp(app.id)"
          >
            <div class="avatar">
              {{ (app.candidate_name || '?').charAt(0) }}
            </div>
            <div class="info">
              <div class="name-row">
                <span class="name">{{ role === 'recruiter' ? app.candidate_name : app.job_title }}</span>
                <el-tag :type="statusType(app.status)" size="small">{{ statusText(app.status) }}</el-tag>
              </div>
              <div class="sub">
                {{ role === 'recruiter' ? app.job_title : 'HR 沟通' }}
              </div>
              <div class="time">{{ app.applied_at }}</div>
            </div>
          </div>
          <el-empty v-if="appList.length === 0" description="暂无记录" :image-size="60" />
        </div>
      </div>

      <div class="chat-area card">
        <div v-if="currentApp" class="chat-header">
          <div class="chat-title">
            <span class="name">{{ role === 'recruiter' ? currentApp.candidate_name : currentApp.job_title }}</span>
            <el-tag :type="statusType(currentApp.status)" size="small">
              {{ statusText(currentApp.status) }}
            </el-tag>
          </div>
          <div class="chat-sub">
            {{ role === 'recruiter' ? `应聘: ${currentApp.job_title}` : `候选人: ${currentApp.candidate_name}` }}
            <span v-if="role === 'recruiter'" class="divider">|</span>
            <span v-if="role === 'recruiter'">{{ currentApp.candidate_phone }}</span>
          </div>
          <div v-if="role === 'recruiter'" class="status-actions">
            <el-dropdown trigger="click" @command="changeStatus">
              <el-button size="small">
                标记状态<el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="pending">待处理</el-dropdown-item>
                  <el-dropdown-item command="communicating">沟通中</el-dropdown-item>
                  <el-dropdown-item command="rejected">不合适</el-dropdown-item>
                  <el-dropdown-item command="hired">已录用</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>

        <div v-else class="empty-chat">
          <el-icon :size="48" color="#c0c4cc"><ChatDotRound /></el-icon>
          <p>请选择一位候选人开始沟通</p>
        </div>

        <div v-if="currentApp" class="messages-container" ref="msgContainer">
          <div v-for="msg in messages" :key="msg.id" class="message-row" :class="msg.sender">
            <div class="msg-avatar">{{ (msg.sender_name || '?').charAt(0) }}</div>
            <div class="msg-bubble-wrap">
              <div class="msg-meta">
                <span class="msg-name">{{ msg.sender_name }}</span>
                <span class="msg-time">{{ msg.created_at }}</span>
              </div>
              <div class="msg-bubble">{{ msg.content }}</div>
            </div>
          </div>
        </div>

        <div v-if="currentApp" class="input-area">
          <el-input
            v-model="inputMsg"
            type="textarea"
            :rows="3"
            :placeholder="`输入消息，按 Enter 发送，Shift+Enter 换行`"
            @keydown.enter.exact.prevent="sendMsg"
          />
          <div class="send-row">
            <el-button type="primary" @click="sendMsg" :loading="sending">
              <el-icon><Promotion /></el-icon>
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowDown, Promotion } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { api } from '../api'

const route = useRoute()
const role = inject('role')
const refreshStats = inject('refreshStats')

const appList = ref([])
const currentAppId = ref(null)
const currentApp = ref(null)
const messages = ref([])
const inputMsg = ref('')
const sending = ref(false)
const msgContainer = ref(null)

const statusText = (s) => {
  const map = { pending: '待处理', communicating: '沟通中', rejected: '不合适', hired: '已录用' }
  return map[s] || s
}

const statusType = (s) => {
  const map = { pending: 'warning', communicating: 'primary', rejected: 'danger', hired: 'success' }
  return map[s] || 'info'
}

const fetchAppList = async () => {
  appList.value = await api.getApplications()
  if (!currentAppId.value && appList.value.length > 0) {
    selectApp(appList.value[0].id)
  }
}

const selectApp = async (id) => {
  currentAppId.value = id
  currentApp.value = appList.value.find(a => a.id === id) || null
  messages.value = await api.getMessages(id)
  nextTick(scrollToBottom)
}

const scrollToBottom = () => {
  if (msgContainer.value) {
    msgContainer.value.scrollTop = msgContainer.value.scrollHeight
  }
}

const sendMsg = async () => {
  if (!inputMsg.value.trim()) return
  if (!currentAppId.value) return
  sending.value = true
  try {
    const sender = role.value
    const senderName = role.value === 'recruiter' ? '李经理' : (currentApp.value?.candidate_name || '候选人')
    const msg = await api.sendMessage(currentAppId.value, {
      sender,
      sender_name: senderName,
      content: inputMsg.value
    })
    messages.value.push(msg)
    inputMsg.value = ''
    if (role.value === 'recruiter' && currentApp.value?.status === 'pending') {
      await api.updateApplicationStatus(currentAppId.value, 'communicating')
      currentApp.value.status = 'communicating'
      const app = appList.value.find(a => a.id === currentAppId.value)
      if (app) app.status = 'communicating'
      refreshStats()
    }
    nextTick(scrollToBottom)
  } finally {
    sending.value = false
  }
}

const changeStatus = async (status) => {
  if (!currentAppId.value) return
  await api.updateApplicationStatus(currentAppId.value, status)
  if (currentApp.value) currentApp.value.status = status
  const app = appList.value.find(a => a.id === currentAppId.value)
  if (app) app.status = status
  ElMessage.success('状态已更新')
  refreshStats()
}

onMounted(async () => {
  await fetchAppList()
  if (route.params.id) {
    selectApp(Number(route.params.id))
  }
})
</script>

<style scoped>
.communication-page {
  height: calc(100vh - 180px);
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
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 12px;
  flex-shrink: 0;
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

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #fafafa;
}

.message-row {
  display: flex;
  margin-bottom: 20px;
  gap: 10px;
}

.message-row.recruiter {
  flex-direction: row-reverse;
}

.message-row.candidate .msg-bubble-wrap {
  align-items: flex-start;
}

.message-row.recruiter .msg-bubble-wrap {
  align-items: flex-end;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
  color: #fff;
}

.message-row.candidate .msg-avatar {
  background: linear-gradient(135deg, #10b981, #34d399);
}

.message-row.recruiter .msg-avatar {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.msg-bubble-wrap {
  max-width: 70%;
  display: flex;
  flex-direction: column;
}

.msg-meta {
  font-size: 11px;
  color: #9ca3af;
  margin-bottom: 4px;
  display: flex;
  gap: 10px;
}

.msg-bubble {
  padding: 10px 14px;
  border-radius: 10px;
  line-height: 1.5;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-row.candidate .msg-bubble {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-top-left-radius: 2px;
}

.message-row.recruiter .msg-bubble {
  background: #409eff;
  color: #fff;
  border-top-right-radius: 2px;
}

.input-area {
  padding: 12px 16px;
  border-top: 1px solid #f0f0f0;
  background: #fff;
}

.send-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}
</style>
