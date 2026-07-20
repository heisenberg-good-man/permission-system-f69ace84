<template>
  <div class="interviews-page">
    <div class="page-header">
      <h2>面试安排</h2>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        安排面试
      </el-button>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" @submit.prevent>
        <el-form-item label="职位">
          <el-select v-model="filters.job_id" placeholder="全部职位" clearable style="width: 200px" @change="fetchList">
            <el-option v-for="job in jobs" :key="job.id" :label="job.title" :value="job.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="filters.status" @change="fetchList">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="scheduled">已安排</el-radio-button>
            <el-radio-button value="completed">已完成</el-radio-button>
            <el-radio-button value="cancelled">已取消</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width: 280px"
            @change="onDateChange"
          />
        </el-form-item>
        <el-form-item>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="list-card">
      <el-table :data="interviews" v-loading="loading" stripe>
        <el-table-column prop="candidate_name" label="候选人" width="100" />
        <el-table-column prop="job_title" label="应聘职位" width="160" />
        <el-table-column prop="round" label="轮次" width="80" />
        <el-table-column prop="way" label="方式" width="100">
          <template #default="{ row }">
            {{ INTERVIEW_WAY_TEXT[row.way] }}
          </template>
        </el-table-column>
        <el-table-column prop="interview_time" label="面试时间" width="170" />
        <el-table-column prop="interviewer" label="面试官" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="INTERVIEW_STATUS_TYPE[row.status]">
              {{ INTERVIEW_STATUS_TEXT[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDetail(row)">详情</el-button>
            <el-button link type="primary" @click="openEditDialog(row)" v-if="row.status === 'scheduled'">
              修改时间
            </el-button>
            <el-button link type="success" @click="openFeedbackDialog(row)" v-if="row.status === 'scheduled' || row.status === 'completed'">
              反馈
            </el-button>
            <el-button link type="danger" @click="handleCancel(row)" v-if="row.status === 'scheduled'">
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!loading && interviews.length === 0" description="暂无面试安排" />
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '修改面试' : '安排面试'"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="候选人" v-if="!isEdit">
          <el-select v-model="form.application_id" placeholder="选择候选人" filterable @change="onAppChange" style="width: 100%">
            <el-option
              v-for="app in candidateOptions"
              :key="app.id"
              :label="`${app.candidate_name} - ${app.job_title}（${STATUS_TEXT[app.status]}）`"
              :value="app.id"
              :disabled="app.status === 'rejected' || app.status === 'hired'"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="候选人" v-else>
          <span>{{ currentInterview?.candidate_name }}</span>
        </el-form-item>
        <el-form-item label="面试轮次" prop="round">
          <el-select v-model="form.round" placeholder="请选择" style="width: 100%">
            <el-option v-for="r in INTERVIEW_ROUNDS" :key="r" :label="r" :value="r" />
          </el-select>
        </el-form-item>
        <el-form-item label="面试方式" prop="way">
          <el-radio-group v-model="form.way">
            <el-radio value="onsite">现场</el-radio>
            <el-radio value="online">视频</el-radio>
            <el-radio value="phone">电话</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="面试时间" prop="interview_time">
          <el-date-picker
            v-model="form.interview_time"
            type="datetime"
            placeholder="选择面试时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="面试官" prop="interviewer">
          <el-input v-model="form.interviewer" placeholder="请输入面试官姓名" />
        </el-form-item>
        <el-form-item label="地点" v-if="form.way === 'onsite'">
          <el-input v-model="form.location" placeholder="请输入面试地点" />
        </el-form-item>
        <el-form-item label="会议链接" v-if="form.way === 'online'">
          <el-input v-model="form.meeting_link" placeholder="请输入视频会议链接" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="可选" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">确定</el-button>
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
          <span>{{ currentFeedback?.candidate_name }} - {{ currentFeedback?.round }}</span>
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

    <el-drawer v-model="detailVisible" title="面试详情" size="480px">
      <div v-if="detailData" class="detail-content">
        <div class="detail-header">
          <h3>{{ detailData.candidate_name }}</h3>
          <el-tag :type="INTERVIEW_STATUS_TYPE[detailData.status]">
            {{ INTERVIEW_STATUS_TEXT[detailData.status] }}
          </el-tag>
        </div>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="应聘职位">{{ detailData.job_title }}</el-descriptions-item>
          <el-descriptions-item label="面试轮次">{{ detailData.round }}</el-descriptions-item>
          <el-descriptions-item label="面试方式">{{ INTERVIEW_WAY_TEXT[detailData.way] }}</el-descriptions-item>
          <el-descriptions-item label="面试时间">{{ detailData.interview_time }}</el-descriptions-item>
          <el-descriptions-item label="面试官">{{ detailData.interviewer }}</el-descriptions-item>
          <el-descriptions-item label="地点" v-if="detailData.location">{{ detailData.location }}</el-descriptions-item>
          <el-descriptions-item label="会议链接" v-if="detailData.meeting_link">
            <el-link :href="detailData.meeting_link" target="_blank" type="primary">
              {{ detailData.meeting_link }}
            </el-link>
          </el-descriptions-item>
          <el-descriptions-item label="备注" v-if="detailData.remark">{{ detailData.remark }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ detailData.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ detailData.updated_at }}</el-descriptions-item>
        </el-descriptions>
        <div class="feedback-section" v-if="detailData.feedback_result">
          <h4>面试反馈</h4>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="反馈结果">
              <el-tag :type="INTERVIEW_FEEDBACK_RESULT_TYPE[detailData.feedback_result]">
                {{ INTERVIEW_FEEDBACK_RESULT_TEXT[detailData.feedback_result] }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="评分">
              <el-rate v-model="detailData.feedback_rating" disabled />
            </el-descriptions-item>
            <el-descriptions-item label="评价" v-if="detailData.feedback_comment">
              {{ detailData.feedback_comment }}
            </el-descriptions-item>
            <el-descriptions-item label="反馈时间" v-if="detailData.feedback_at">
              {{ detailData.feedback_at }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <div class="detail-actions">
          <el-button type="primary" @click="openEditDialog(detailData)" v-if="detailData.status === 'scheduled'">
            修改时间
          </el-button>
          <el-button type="success" @click="openFeedbackDialog(detailData)" v-if="detailData.status === 'scheduled' || detailData.status === 'completed'">
            提交反馈
          </el-button>
          <el-button type="danger" @click="handleCancel(detailData)" v-if="detailData.status === 'scheduled'">
            取消面试
          </el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { api, STATUS_TEXT, INTERVIEW_STATUS_TEXT, INTERVIEW_STATUS_TYPE, INTERVIEW_WAY_TEXT, INTERVIEW_ROUNDS, INTERVIEW_FEEDBACK_RESULT_TEXT, INTERVIEW_FEEDBACK_RESULT_TYPE } from '../api'

const router = useRouter()
const refreshStats = inject('refreshStats')
const refreshAll = inject('refreshAll')

const loading = ref(false)
const interviews = ref([])
const jobs = ref([])
const applications = ref([])
const filters = reactive({
  job_id: '',
  status: '',
  start_date: '',
  end_date: ''
})
const dateRange = ref([])
const selectedAppId = ref(null)

const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentInterview = ref(null)
const form = reactive({
  application_id: null,
  round: '一面',
  way: 'onsite',
  interview_time: '',
  interviewer: '',
  location: '',
  meeting_link: '',
  remark: ''
})

const rules = {
  round: [{ required: true, message: '请选择面试轮次', trigger: 'change' }],
  way: [{ required: true, message: '请选择面试方式', trigger: 'change' }],
  interview_time: [{ required: true, message: '请选择面试时间', trigger: 'change' }],
  interviewer: [{ required: true, message: '请输入面试官', trigger: 'blur' }]
}

const detailVisible = ref(false)
const detailData = ref(null)

const candidateOptions = ref([])

const fetchJobs = async () => {
  try {
    jobs.value = await api.getJobs()
  } catch (e) {}
}

const fetchApplications = async () => {
  try {
    applications.value = await api.getApplications()
    candidateOptions.value = applications.value.filter(
      a => a.status !== 'rejected' && a.status !== 'hired'
    )
  } catch (e) {}
}

const fetchList = async () => {
  loading.value = true
  try {
    const params = {
      job_id: filters.job_id || undefined,
      status: filters.status || undefined,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined
    }
    interviews.value = await api.getInterviews(params)
  } catch (e) {
  } finally {
    loading.value = false
  }
}

const onDateChange = (val) => {
  if (val && val.length === 2) {
    filters.start_date = val[0]
    filters.end_date = val[1]
  } else {
    filters.start_date = ''
    filters.end_date = ''
  }
  fetchList()
}

const resetFilters = () => {
  filters.job_id = ''
  filters.status = ''
  filters.start_date = ''
  filters.end_date = ''
  dateRange.value = []
  fetchList()
}

const openCreateDialog = () => {
  isEdit.value = false
  currentInterview.value = null
  Object.assign(form, {
    application_id: selectedAppId.value,
    round: '一面',
    way: 'onsite',
    interview_time: '',
    interviewer: '',
    location: '',
    meeting_link: '',
    remark: ''
  })
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  currentInterview.value = row
  Object.assign(form, {
    application_id: row.application_id,
    round: row.round,
    way: row.way,
    interview_time: row.interview_time,
    interviewer: row.interviewer,
    location: row.location,
    meeting_link: row.meeting_link,
    remark: row.remark
  })
  dialogVisible.value = true
  detailVisible.value = false
}

const onAppChange = () => {
  const app = applications.value.find(a => a.id === form.application_id)
  if (app) {
    form.candidate_name = app.candidate_name
  }
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      if (isEdit.value) {
        await api.updateInterview(currentInterview.value.id, {
          round: form.round,
          way: form.way,
          interview_time: form.interview_time,
          interviewer: form.interviewer,
          location: form.location,
          meeting_link: form.meeting_link,
          remark: form.remark
        })
        ElMessage.success('面试已更新')
      } else {
        await api.createInterview(form.application_id, {
          round: form.round,
          way: form.way,
          interview_time: form.interview_time,
          interviewer: form.interviewer,
          location: form.location,
          meeting_link: form.meeting_link,
          remark: form.remark
        })
        ElMessage.success('面试安排成功')
      }
      dialogVisible.value = false
      fetchList()
      fetchApplications()
      refreshStats()
    } catch (e) {
    } finally {
      submitting.value = false
    }
  })
}

const handleCancel = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要取消 ${row.round} 吗？`, '提示', {
      type: 'warning'
    })
    const { value: reason } = await ElMessageBox.prompt('请输入取消原因（可选）', '取消面试', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputPlaceholder: '可选',
      type: 'warning'
    })
    await api.cancelInterview(row.id, reason || '')
    ElMessage.success('已取消面试')
    fetchList()
    refreshStats()
    if (detailVisible.value && detailData.value?.id === row.id) {
      detailData.value.status = 'cancelled'
    }
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

const viewDetail = (row) => {
  detailData.value = row
  detailVisible.value = true
}

const feedbackDialogVisible = ref(false)
const currentFeedback = ref(null)
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

const openFeedbackDialog = (row) => {
  currentFeedback.value = row
  feedbackForm.value = {
    result: row.feedback_result || 'pass',
    comment: row.feedback_comment || '',
    rating: row.feedback_rating || 3
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
    await api.submitInterviewFeedback(currentFeedback.value.id, feedbackForm.value)
    ElMessage.success('面试反馈已提交')
    feedbackDialogVisible.value = false
    fetchList()
    refreshStats()
    if (detailVisible.value && detailData.value?.id === currentFeedback.value.id) {
      detailData.value = { ...detailData.value, ...feedbackForm.value, status: 'completed' }
    }
  } catch (e) {}
}

onMounted(() => {
  fetchJobs()
  fetchApplications()
  fetchList()
})
</script>

<style scoped>
.interviews-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  color: #1f2937;
}

.filter-card {
  margin-bottom: 16px;
}

.list-card {
  background: #fff;
  border-radius: 8px;
}

.detail-content {
  padding: 0 8px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.detail-header h3 {
  margin: 0;
  font-size: 18px;
}

.detail-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.feedback-section {
  margin-top: 20px;
}

.feedback-section h4 {
  margin: 0 0 12px 0;
  font-size: 15px;
  color: #303133;
}
</style>
