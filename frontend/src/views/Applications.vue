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
            <el-button type="success" @click="openInterviewDialog" v-if="canScheduleInterview">
              <el-icon><Calendar /></el-icon>
              安排面试
            </el-button>
            <el-button type="warning" @click="openOfferDialog()" v-if="canCreateOffer">
              <el-icon><Present /></el-icon>
              发 Offer
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

          <el-tab-pane label="面试记录" name="interviews">
            <div class="interview-list">
              <div v-if="interviews.length === 0" class="no-interviews">
                <el-empty description="暂无面试记录" :image-size="60" />
                <el-button type="primary" @click="openInterviewDialog" v-if="canScheduleInterview">
                  安排面试
                </el-button>
              </div>
              <div v-else class="interview-items">
                <div v-for="iv in interviews" :key="iv.id" class="interview-item">
                  <div class="interview-top">
                    <span class="interview-round">{{ iv.round }}</span>
                    <el-tag :type="INTERVIEW_STATUS_TYPE[iv.status]" size="small">
                      {{ INTERVIEW_STATUS_TEXT[iv.status] }}
                    </el-tag>
                  </div>
                  <div class="interview-info">
                    <div class="info-row">
                      <el-icon><Calendar /></el-icon>
                      <span>{{ INTERVIEW_WAY_TEXT[iv.way] }} · {{ iv.interview_time }}</span>
                    </div>
                    <div class="info-row">
                      <el-icon><User /></el-icon>
                      <span>面试官：{{ iv.interviewer }}</span>
                    </div>
                    <div class="info-row" v-if="iv.location">
                      <el-icon><Location /></el-icon>
                      <span>{{ iv.location }}</span>
                    </div>
                    <div class="info-row" v-if="iv.meeting_link">
                      <el-icon><Link /></el-icon>
                      <span>{{ iv.meeting_link }}</span>
                    </div>
                    <div class="info-row remark" v-if="iv.remark">
                      <span>备注：{{ iv.remark }}</span>
                    </div>
                  </div>
                  <div class="interview-actions">
                    <el-button link type="primary" size="small" @click="openEditInterviewDialog(iv)" v-if="iv.status === 'scheduled'">
                      修改时间
                    </el-button>
                    <el-button link type="success" size="small" @click="openFeedbackDialog(iv)" v-if="iv.status === 'scheduled' || iv.status === 'completed'">
                      反馈
                    </el-button>
                    <el-button link type="danger" size="small" @click="cancelInterview(iv)" v-if="iv.status === 'scheduled'">
                      取消
                    </el-button>
                  </div>
                  <div class="interview-feedback" v-if="iv.feedback_result">
                    <div class="feedback-header">
                      <span class="feedback-label">面试反馈</span>
                      <el-tag :type="INTERVIEW_FEEDBACK_RESULT_TYPE[iv.feedback_result]" size="small">
                        {{ INTERVIEW_FEEDBACK_RESULT_TEXT[iv.feedback_result] }}
                      </el-tag>
                    </div>
                    <div class="feedback-info">
                      <span>评分：{{ iv.feedback_rating || '-' }} 分</span>
                      <span v-if="iv.feedback_comment">评价：{{ iv.feedback_comment }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="Offer 记录" name="offers">
            <div class="offer-list">
              <div v-if="offers.length === 0" class="no-offers">
                <el-empty description="暂无 Offer 记录" :image-size="60" />
                <el-button type="primary" @click="openOfferDialog()" v-if="canCreateOffer">
                  创建 Offer
                </el-button>
                <p v-else class="empty-tip">候选人需通过面试后才能创建 Offer</p>
              </div>
              <div v-else class="offer-items">
                <div v-for="offer in offers" :key="offer.id" class="offer-item">
                  <div class="offer-top">
                    <span class="offer-position">{{ offer.position }}</span>
                    <el-tag :type="OFFER_STATUS_TYPE[offer.status]" size="small">
                      {{ OFFER_STATUS_TEXT[offer.status] }}
                    </el-tag>
                  </div>
                  <div class="offer-info">
                    <div class="info-row">
                      <el-icon><Money /></el-icon>
                      <span>薪资：{{ offer.salary_min }}-{{ offer.salary_max }}K</span>
                    </div>
                    <div class="info-row">
                      <el-icon><Calendar /></el-icon>
                      <span>入职日期：{{ offer.join_date }}</span>
                    </div>
                    <div class="info-row">
                      <el-icon><Clock /></el-icon>
                      <span>试用期：{{ offer.probation_months }}个月</span>
                    </div>
                    <div class="info-row remark" v-if="offer.remark">
                      <span>备注：{{ offer.remark }}</span>
                    </div>
                  </div>
                  <div class="offer-actions" v-if="offer.status === 'draft'">
                    <el-button link type="primary" size="small" @click="openOfferDialog(true, offer)">
                      编辑
                    </el-button>
                    <el-button link type="success" size="small" @click="sendOffer(offer)">
                      发送
                    </el-button>
                  </div>
                  <div class="offer-actions" v-else-if="offer.status === 'sent'">
                    <el-button link type="danger" size="small" @click="withdrawOffer(offer)">
                      撤回
                    </el-button>
                  </div>
                </div>
              </div>
              <div class="offer-add-btn" v-if="offers.length > 0 && canCreateOffer">
                <el-button type="primary" plain @click="openOfferDialog()">
                  + 新建 Offer
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

    <el-dialog
      v-model="interviewDialogVisible"
      :title="isEditInterview ? '修改面试' : '安排面试'"
      width="520px"
      :close-on-click-modal="false"
    >
      <el-form :model="interviewForm" :rules="interviewRules" ref="interviewFormRef" label-width="90px">
        <el-form-item label="候选人">
          <span>{{ selectedApp?.candidate_name }} - {{ selectedApp?.job_title }}</span>
        </el-form-item>
        <el-form-item label="面试轮次" prop="round">
          <el-select v-model="interviewForm.round" placeholder="请选择" style="width: 100%">
            <el-option v-for="r in INTERVIEW_ROUNDS" :key="r" :label="r" :value="r" />
          </el-select>
        </el-form-item>
        <el-form-item label="面试方式" prop="way">
          <el-radio-group v-model="interviewForm.way">
            <el-radio value="onsite">现场</el-radio>
            <el-radio value="online">视频</el-radio>
            <el-radio value="phone">电话</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="面试时间" prop="interview_time">
          <el-date-picker
            v-model="interviewForm.interview_time"
            type="datetime"
            placeholder="选择面试时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="面试官" prop="interviewer">
          <el-input v-model="interviewForm.interviewer" placeholder="请输入面试官姓名" />
        </el-form-item>
        <el-form-item label="地点" v-if="interviewForm.way === 'onsite'">
          <el-input v-model="interviewForm.location" placeholder="请输入面试地点" />
        </el-form-item>
        <el-form-item label="会议链接" v-if="interviewForm.way === 'online'">
          <el-input v-model="interviewForm.meeting_link" placeholder="请输入视频会议链接" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="interviewForm.remark" type="textarea" :rows="2" placeholder="可选" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="interviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitInterview" :loading="submittingInterview">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="feedbackDialogVisible"
      title="面试反馈"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="feedbackForm" :rules="feedbackRules" ref="feedbackFormRef" label-width="90px">
        <el-form-item label="候选人">
          <span>{{ currentFeedbackInterview?.candidate_name }} - {{ currentFeedbackInterview?.round }}</span>
        </el-form-item>
        <el-form-item label="反馈结果" prop="result">
          <el-radio-group v-model="feedbackForm.result">
            <el-radio value="pass">
              <el-tag type="success">通过</el-tag>
            </el-radio>
            <el-radio value="fail">
              <el-tag type="danger">未通过</el-tag>
            </el-radio>
            <el-radio value="pending">
              <el-tag type="warning">待定</el-tag>
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="评分" prop="rating">
          <el-rate v-model="feedbackForm.rating" :max="5" />
        </el-form-item>
        <el-form-item label="评价">
          <el-input v-model="feedbackForm.comment" type="textarea" :rows="4" placeholder="请输入面试评价" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="feedbackDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitFeedback">提交反馈</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="offerDialogVisible"
      :title="isEditOffer ? '编辑 Offer' : '创建 Offer'"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-form :model="offerForm" :rules="offerRules" ref="offerFormRef" label-width="100px">
        <el-form-item label="候选人">
          <span>{{ selectedApp?.candidate_name }} - {{ selectedApp?.job_title }}</span>
        </el-form-item>
        <el-form-item label="岗位" prop="position">
          <el-input v-model="offerForm.position" placeholder="请输入岗位名称" />
        </el-form-item>
        <el-form-item label="薪资范围" prop="salary_min">
          <el-input-number v-model="offerForm.salary_min" :min="0" :step="1000" placeholder="最低" />
          <span style="margin: 0 10px">-</span>
          <el-input-number v-model="offerForm.salary_max" :min="0" :step="1000" placeholder="最高" />
          <span style="margin-left: 8px">K</span>
        </el-form-item>
        <el-form-item label="入职日期" prop="join_date">
          <el-date-picker
            v-model="offerForm.join_date"
            type="date"
            placeholder="选择入职日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="试用期">
          <el-input-number v-model="offerForm.probation_months" :min="0" :max="12" />
          <span style="margin-left: 8px">个月</span>
        </el-form-item>
        <el-form-item label="福利待遇">
          <el-input v-model="offerForm.benefits" type="textarea" :rows="2" placeholder="请输入福利待遇说明" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="offerForm.remark" type="textarea" :rows="3" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="offerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitOffer">{{ isEditOffer ? '保存' : '创建草稿' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api, INTERVIEW_STATUS_TEXT, INTERVIEW_STATUS_TYPE, INTERVIEW_WAY_TEXT, INTERVIEW_ROUNDS, INTERVIEW_FEEDBACK_RESULT_TEXT, INTERVIEW_FEEDBACK_RESULT_TYPE, OFFER_STATUS_TEXT, OFFER_STATUS_TYPE } from '../api'

const router = useRouter()
const route = useRoute()
const refreshStats = inject('refreshStats')
const STATUS_TEXT = inject('STATUS_TEXT')
const STATUS_TYPE = inject('STATUS_TYPE')

const jobs = ref([])
const applications = ref([])
const messages = ref([])
const interviews = ref([])
const jobFilter = ref('')
const statusFilter = ref('')
const selectedId = ref(null)
const activeTab = ref('resume')

const interviewDialogVisible = ref(false)
const isEditInterview = ref(false)
const currentEditInterview = ref(null)
const submittingInterview = ref(false)
const interviewFormRef = ref(null)
const interviewForm = ref({
  round: '一面',
  way: 'onsite',
  interview_time: '',
  interviewer: '',
  location: '',
  meeting_link: '',
  remark: ''
})

const interviewRules = {
  round: [{ required: true, message: '请选择面试轮次', trigger: 'change' }],
  way: [{ required: true, message: '请选择面试方式', trigger: 'change' }],
  interview_time: [{ required: true, message: '请选择面试时间', trigger: 'change' }],
  interviewer: [{ required: true, message: '请输入面试官', trigger: 'blur' }]
}

const feedbackDialogVisible = ref(false)
const currentFeedbackInterview = ref(null)
const feedbackForm = ref({
  result: 'pass',
  comment: '',
  rating: 3
})
const feedbackFormRef = ref(null)
const feedbackRules = {
  result: [{ required: true, message: '请选择反馈结果', trigger: 'change' }],
  rating: [{ required: true, message: '请输入评分', trigger: 'blur' }]
}

const offers = ref([])
const offerDialogVisible = ref(false)
const currentEditOffer = ref(null)
const isEditOffer = ref(false)
const offerFormRef = ref(null)
const offerForm = ref({
  position: '',
  salary_min: null,
  salary_max: null,
  join_date: '',
  probation_months: 3,
  benefits: '',
  remark: ''
})
const offerRules = {
  position: [{ required: true, message: '请输入岗位名称', trigger: 'blur' }],
  salary_min: [{ required: true, message: '请输入最低薪资', trigger: 'blur' }],
  salary_max: [{ required: true, message: '请输入最高薪资', trigger: 'blur' }],
  join_date: [{ required: true, message: '请选择入职日期', trigger: 'change' }]
}

const hasPassedInterview = computed(() => {
  return interviews.value.some(i => 
    i.status === 'completed' && i.feedback_result === 'pass'
  )
})

const canCreateOffer = computed(() => {
  if (!selectedApp.value) return false
  if (selectedApp.value.status === 'rejected') return false
  return hasPassedInterview.value
})

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

const canScheduleInterview = computed(() => {
  if (!selectedApp.value) return false
  const status = selectedApp.value.status
  return status === 'screening' || status === 'communicating'
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
  try {
    interviews.value = await api.getApplicationInterviews(app.id)
  } catch (e) {
    interviews.value = []
  }
  try {
    offers.value = await api.getOffers({ application_id: app.id })
  } catch (e) {
    offers.value = []
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

const openInterviewDialog = () => {
  isEditInterview.value = false
  currentEditInterview.value = null
  interviewForm.value = {
    round: '一面',
    way: 'onsite',
    interview_time: '',
    interviewer: '',
    location: '',
    meeting_link: '',
    remark: ''
  }
  interviewDialogVisible.value = true
}

const openEditInterviewDialog = (iv) => {
  isEditInterview.value = true
  currentEditInterview.value = iv
  interviewForm.value = {
    round: iv.round,
    way: iv.way,
    interview_time: iv.interview_time,
    interviewer: iv.interviewer,
    location: iv.location || '',
    meeting_link: iv.meeting_link || '',
    remark: iv.remark || ''
  }
  interviewDialogVisible.value = true
}

const submitInterview = async () => {
  if (!interviewFormRef.value) return
  await interviewFormRef.value.validate(async (valid) => {
    if (!valid) return
    submittingInterview.value = true
    try {
      if (isEditInterview.value) {
        await api.updateInterview(currentEditInterview.value.id, interviewForm.value)
        ElMessage.success('面试已更新')
      } else {
        await api.createInterview(selectedId.value, interviewForm.value)
        ElMessage.success('面试安排成功')
      }
      interviewDialogVisible.value = false
      interviews.value = await api.getApplicationInterviews(selectedId.value)
      fetchData()
      refreshStats()
      try {
        messages.value = await api.getMessages(selectedId.value)
      } catch (e) {}
    } catch (e) {
    } finally {
      submittingInterview.value = false
    }
  })
}

const cancelInterview = async (iv) => {
  try {
    await ElMessageBox.confirm(`确定要取消 ${iv.round} 吗？`, '提示', {
      type: 'warning'
    })
    const { value: reason } = await ElMessageBox.prompt('请输入取消原因（可选）', '取消面试', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputPlaceholder: '可选',
      type: 'warning'
    })
    await api.cancelInterview(iv.id, reason || '')
    ElMessage.success('已取消面试')
    interviews.value = await api.getApplicationInterviews(selectedId.value)
    refreshStats()
    try {
      messages.value = await api.getMessages(selectedId.value)
    } catch (e) {}
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

const openFeedbackDialog = (iv) => {
  currentFeedbackInterview.value = iv
  feedbackForm.value = {
    result: iv.feedback_result || 'pass',
    comment: iv.feedback_comment || '',
    rating: iv.feedback_rating || 3
  }
  feedbackDialogVisible.value = true
}

const submitFeedback = async () => {
  if (!feedbackFormRef.value) return
  try {
    await feedbackFormRef.value.validate()
  } catch (e) {
    return
  }
  try {
    await api.submitInterviewFeedback(currentFeedbackInterview.value.id, feedbackForm.value)
    ElMessage.success('面试反馈已提交')
    feedbackDialogVisible.value = false
    interviews.value = await api.getApplicationInterviews(selectedId.value)
    fetchData()
    refreshStats()
    if (activeTab.value === 'messages') {
      messages.value = await api.getMessages(selectedId.value)
    }
  } catch (e) {}
}

const openOfferDialog = (isEdit = false, offer = null) => {
  isEditOffer.value = isEdit
  currentEditOffer.value = offer
  if (isEdit && offer) {
    offerForm.value = {
      position: offer.position,
      salary_min: offer.salary_min,
      salary_max: offer.salary_max,
      join_date: offer.join_date,
      probation_months: offer.probation_months,
      benefits: offer.benefits,
      remark: offer.remark
    }
  } else {
    offerForm.value = {
      position: selectedApp.value?.job_title || '',
      salary_min: null,
      salary_max: null,
      join_date: '',
      probation_months: 3,
      benefits: '',
      remark: ''
    }
  }
  offerDialogVisible.value = true
}

const submitOffer = async () => {
  if (!offerFormRef.value) return
  try {
    await offerFormRef.value.validate()
  } catch (e) {
    return
  }
  try {
    if (isEditOffer.value) {
      await api.updateOffer(currentEditOffer.value.id, offerForm.value)
      ElMessage.success('Offer 已更新')
    } else {
      await api.createOffer(selectedId.value, offerForm.value)
      ElMessage.success('Offer 草稿已创建')
    }
    offerDialogVisible.value = false
    offers.value = await api.getOffers({ application_id: selectedId.value })
    fetchData()
    refreshStats()
    try {
      messages.value = await api.getMessages(selectedId.value)
    } catch (e) {}
  } catch (e) {
    ElMessage.error(e.message || '操作失败')
  }
}

const sendOffer = async (offer) => {
  try {
    await ElMessageBox.confirm(
      `确认将 Offer 发送给 ${offer.candidate_name}？发送后候选人将收到通知。`,
      '发送 Offer',
      { type: 'warning' }
    )
    await api.sendOffer(offer.id)
    ElMessage.success('Offer 已发送')
    offers.value = await api.getOffers({ application_id: selectedId.value })
    fetchData()
    refreshStats()
    try {
      messages.value = await api.getMessages(selectedId.value)
    } catch (e) {}
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message || '发送失败')
  }
}

const withdrawOffer = async (offer) => {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      '请输入撤回原因',
      '撤回 Offer',
      {
        confirmButtonText: '确认撤回',
        cancelButtonText: '取消',
        inputType: 'textarea',
        inputPlaceholder: '请输入撤回原因（可选）',
        inputValidator: () => true
      }
    )
    await api.withdrawOffer(offer.id, reason || '')
    ElMessage.success('Offer 已撤回')
    offers.value = await api.getOffers({ application_id: selectedId.value })
    fetchData()
    refreshStats()
    try {
      messages.value = await api.getMessages(selectedId.value)
    } catch (e) {}
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message || '撤回失败')
  }
}

onMounted(async () => {
  await fetchData()
  const appId = route.query.appId
  const action = route.query.action
  if (appId) {
    const id = Number(appId)
    const app = applications.value.find(a => a.id === id)
    if (app) {
      selectCandidate(app)
      if (action === 'schedule' && canScheduleInterview.value) {
        openInterviewDialog()
      }
    }
  }
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

.interview-list {
  padding: 8px 0;
}

.no-interviews {
  text-align: center;
  padding: 40px 0;
}

.no-interviews .el-button {
  margin-top: 16px;
}

.interview-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.interview-item {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.interview-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.interview-round {
  font-weight: 600;
  color: #1f2937;
  font-size: 15px;
}

.interview-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: #6b7280;
  font-size: 13px;
}

.interview-info .info-row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
}

.interview-info .info-row .el-icon {
  margin-top: 2px;
  flex-shrink: 0;
}

.interview-info .remark {
  color: #9ca3af;
  font-size: 12px;
}

.interview-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e5e7eb;
}

.interview-feedback {
  margin-top: 12px;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 6px;
  border-left: 3px solid #409eff;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.feedback-label {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.feedback-info {
  font-size: 12px;
  color: #6b7280;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.offer-list {
  padding: 8px 0;
}

.no-offers {
  text-align: center;
  padding: 40px 0;
}

.no-offers .el-button {
  margin-top: 16px;
}

.no-offers .empty-tip {
  margin-top: 12px;
  color: #909399;
  font-size: 13px;
}

.offer-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.offer-item {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.offer-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.offer-position {
  font-weight: 600;
  color: #1f2937;
  font-size: 15px;
}

.offer-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: #6b7280;
  font-size: 13px;
}

.offer-info .info-row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
}

.offer-info .info-row .el-icon {
  margin-top: 2px;
  flex-shrink: 0;
}

.offer-info .remark {
  color: #9ca3af;
  font-size: 12px;
}

.offer-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e5e7eb;
}

.offer-add-btn {
  margin-top: 16px;
  text-align: center;
}

.empty-detail {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
