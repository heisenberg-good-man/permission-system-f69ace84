<template>
  <div class="timeline-container">
    <div v-if="loading" class="timeline-loading">
      <el-icon class="is-loading" :size="20"><Loading /></el-icon>
      <span>加载中...</span>
    </div>
    <div v-else-if="errorMsg" class="timeline-error">
      <el-alert :title="errorMsg" type="error" :closable="false" show-icon />
    </div>
    <div v-else-if="items.length === 0" class="timeline-empty">
      <el-empty description="暂无记录" :image-size="60" />
    </div>
    <div v-else class="timeline-list" ref="timelineRef">
      <div
        v-for="item in items"
        :key="item.id"
        class="timeline-item"
        :class="[item.type, item.sender_role]"
      >
        <div class="timeline-icon">
          <el-icon><component :is="getIcon(item.type)" /></el-icon>
        </div>
        <div class="timeline-content">
          <div class="timeline-meta">
            <span class="timeline-role">{{ getRoleLabel(item) }}</span>
            <span class="timeline-time">{{ item.created_at }}</span>
          </div>
          <div class="timeline-text" :class="{ 'system-text': item.type === 'system' }">
            {{ item.content }}
          </div>
          <div v-if="item.job_title" class="timeline-tag">
            <el-tag size="small" type="info" effect="light">{{ item.job_title }}</el-tag>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, inject } from 'vue'
import { Loading, ChatDotRound, Bell, Calendar, Present, User } from '@element-plus/icons-vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  interviews: {
    type: Array,
    default: () => []
  },
  offers: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  errorMsg: {
    type: String,
    default: ''
  },
  autoScroll: {
    type: Boolean,
    default: false
  }
})

const STATUS_TEXT = inject('STATUS_TEXT', {})
const OFFER_STATUS_TEXT = inject('OFFER_STATUS_TEXT', {})
const INTERVIEW_STATUS_TEXT = inject('INTERVIEW_STATUS_TEXT', {})

const timelineRef = ref(null)

const items = computed(() => {
  const list = []
  props.messages.forEach(m => {
    list.push({
      id: `msg-${m.id}`,
      type: m.sender === 'system' ? 'system' : 'message',
      sender_role: m.sender,
      sender_name: m.sender_name,
      content: m.content,
      created_at: m.created_at,
      application_id: m.application_id,
      job_title: m.job_title || ''
    })
  })
  props.interviews.forEach(i => {
    list.push({
      id: `iv-${i.id}`,
      type: 'interview',
      sender_role: 'system',
      sender_name: '面试安排',
      content: `${i.round} - ${INTERVIEW_STATUS_TEXT[i.status] || i.status}，${i.interview_time}，面试官：${i.interviewer}`,
      created_at: i.created_at,
      application_id: i.application_id,
      job_title: i.job_title || ''
    })
  })
  props.offers.forEach(o => {
    list.push({
      id: `offer-${o.id}`,
      type: 'offer',
      sender_role: 'system',
      sender_name: 'Offer 状态',
      content: `${OFFER_STATUS_TEXT[o.status] || o.status} - ${o.position}，薪资 ${o.salary_min}-${o.salary_max}K`,
      created_at: o.updated_at || o.created_at,
      application_id: o.application_id,
      job_title: o.job_title || ''
    })
  })
  list.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
  return list
})

const getIcon = (type) => {
  const icons = {
    system: Bell,
    message: ChatDotRound,
    interview: Calendar,
    offer: Present
  }
  return icons[type] || User
}

const getRoleLabel = (item) => {
  if (item.type === 'system') return '系统通知'
  if (item.type === 'interview') return '面试安排'
  if (item.type === 'offer') return 'Offer 动态'
  if (item.sender_role === 'recruiter') return '招聘方'
  if (item.sender_role === 'candidate') return '候选人'
  return item.sender_name || '未知'
}

watch(items, () => {
  if (props.autoScroll) {
    nextTick(() => {
      if (timelineRef.value) {
        timelineRef.value.scrollTop = timelineRef.value.scrollHeight
      }
    })
  }
}, { deep: true })
</script>

<style scoped>
.timeline-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.timeline-loading,
.timeline-error,
.timeline-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.timeline-loading {
  gap: 8px;
}

.timeline-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  background: #fafafa;
}

.timeline-item {
  display: flex;
  margin-bottom: 20px;
  gap: 12px;
}

.timeline-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  font-size: 16px;
}

.timeline-item.system .timeline-icon {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
}

.timeline-item.message.recruiter .timeline-icon {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.timeline-item.message.candidate .timeline-icon {
  background: linear-gradient(135deg, #10b981, #34d399);
}

.timeline-item.interview .timeline-icon {
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
}

.timeline-item.offer .timeline-icon {
  background: linear-gradient(135deg, #9333ea, #c084fc);
}

.timeline-content {
  flex: 1;
  min-width: 0;
}

.timeline-meta {
  font-size: 12px;
  color: #9ca3af;
  margin-bottom: 4px;
  display: flex;
  gap: 12px;
}

.timeline-role {
  font-weight: 600;
  color: #6b7280;
}

.timeline-text {
  padding: 10px 14px;
  border-radius: 10px;
  line-height: 1.5;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
  background: #fff;
  border: 1px solid #e5e7eb;
  display: inline-block;
}

.timeline-text.system-text {
  background: #fef3c7;
  border: 1px solid #fde68a;
  color: #92400e;
  font-size: 13px;
}

.timeline-item.message.recruiter .timeline-text {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.timeline-tag {
  margin-top: 6px;
}
</style>
