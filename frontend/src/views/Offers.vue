<template>
  <div class="offers-page">
    <div class="page-header">
      <h2>Offer 管理</h2>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新建 Offer
      </el-button>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" @submit.prevent>
        <el-form-item label="职位">
          <el-select v-model="filters.job_id" placeholder="全部职位" clearable style="width: 200px" @change="onFilterChange">
            <el-option v-for="job in jobs" :key="job.id" :label="job.title" :value="job.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="filters.status" @change="onFilterChange">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="draft">草稿</el-radio-button>
            <el-radio-button value="sent">已发送</el-radio-button>
            <el-radio-button value="accepted">已接受</el-radio-button>
            <el-radio-button value="rejected">已拒绝</el-radio-button>
            <el-radio-button value="withdrawn">已撤回</el-radio-button>
            <el-radio-button value="processed">已处理</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="stats-card">
      <div class="stat-item" :class="{ active: filters.status === '' }" @click="setStatusFilter('')">
        <div class="stat-num">{{ offerStats.total }}</div>
        <div class="stat-label">全部</div>
      </div>
      <div class="stat-item" :class="{ active: filters.status === 'draft' }" @click="setStatusFilter('draft')">
        <div class="stat-num">{{ offerStats.draft }}</div>
        <div class="stat-label">草稿</div>
      </div>
      <div class="stat-item" :class="{ active: filters.status === 'sent' }" @click="setStatusFilter('sent')">
        <div class="stat-num">{{ offerStats.sent }}</div>
        <div class="stat-label">已发送</div>
      </div>
      <div class="stat-item" :class="{ active: filters.status === 'accepted' }" @click="setStatusFilter('accepted')">
        <div class="stat-num">{{ offerStats.accepted }}</div>
        <div class="stat-label">已接受</div>
      </div>
      <div class="stat-item" :class="{ active: filters.status === 'rejected' }" @click="setStatusFilter('rejected')">
        <div class="stat-num">{{ offerStats.rejected }}</div>
        <div class="stat-label">已拒绝</div>
      </div>
      <div class="stat-item" :class="{ active: filters.status === 'withdrawn' }" @click="setStatusFilter('withdrawn')">
        <div class="stat-num">{{ offerStats.withdrawn }}</div>
        <div class="stat-label">已撤回</div>
      </div>
      <div class="stat-item" :class="{ active: filters.status === 'processed' }" @click="setStatusFilter('processed')">
        <div class="stat-num">{{ offerStats.processed }}</div>
        <div class="stat-label">已处理</div>
      </div>
    </el-card>

    <el-card class="list-card">
      <el-table :data="offers" v-loading="loading" stripe>
        <el-table-column prop="candidate_name" label="候选人" width="100" />
        <el-table-column prop="job_title" label="应聘职位" width="160" />
        <el-table-column prop="position" label="岗位" width="140" />
        <el-table-column label="薪资" width="140">
          <template #default="{ row }">
            {{ row.salary_min }}-{{ row.salary_max }}K
          </template>
        </el-table-column>
        <el-table-column prop="join_date" label="入职日期" width="120" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="OFFER_STATUS_TYPE[row.status]">
              {{ OFFER_STATUS_TEXT[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170" />
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDetail(row)">详情</el-button>
            <el-button link type="primary" @click="openEditDialog(row)" v-if="row.status === 'draft'">
              编辑
            </el-button>
            <el-button link type="success" @click="handleSend(row)" v-if="row.status === 'draft'">
              发送
            </el-button>
            <el-button link type="danger" @click="handleWithdraw(row)" v-if="row.status === 'draft' || row.status === 'sent'">
              撤回
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!loading && offers.length === 0" :description="emptyText" />
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑 Offer' : '新建 Offer'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="候选人" v-if="!isEdit" prop="application_id">
          <el-select v-model="form.application_id" placeholder="选择候选人" filterable style="width: 100%" no-data-text="暂无可创建 Offer 的候选人">
            <el-option
              v-for="app in candidateOptions"
              :key="app.id"
              :label="`${app.candidate_name} - ${app.job_title}（${STATUS_TEXT[app.status]}）`"
              :value="app.id"
            />
          </el-select>
          <div class="form-tip">仅显示有通过面试反馈的候选人</div>
        </el-form-item>
        <el-form-item label="候选人" v-else>
          <span>{{ currentOffer?.candidate_name }}</span>
        </el-form-item>
        <el-form-item label="岗位" prop="position">
          <el-input v-model="form.position" placeholder="请输入岗位名称" />
        </el-form-item>
        <el-form-item label="薪资范围" prop="salary_min">
          <el-input-number v-model="form.salary_min" :min="0" :step="1000" placeholder="最低" />
          <span style="margin: 0 10px">-</span>
          <el-input-number v-model="form.salary_max" :min="0" :step="1000" placeholder="最高" />
          <span style="margin-left: 8px">K</span>
        </el-form-item>
        <el-form-item label="入职日期" prop="join_date">
          <el-date-picker
            v-model="form.join_date"
            type="date"
            placeholder="选择入职日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="试用期">
          <el-input-number v-model="form.probation_months" :min="0" :max="12" />
          <span style="margin-left: 8px">个月</span>
        </el-form-item>
        <el-form-item label="福利待遇">
          <el-input v-model="form.benefits" type="textarea" :rows="2" placeholder="请输入福利待遇说明" />
        </el-form-item>
        <el-form-item label="附件说明">
          <el-input v-model="form.attachment_note" type="textarea" :rows="2" placeholder="请输入附件相关说明，如：offer letter、入职须知等" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">{{ isEdit ? '保存' : '创建草稿' }}</el-button>
      </template>
    </el-dialog>

    <el-drawer v-model="detailVisible" title="Offer 详情" size="500px">
      <div v-if="currentOffer" class="offer-detail">
        <div class="detail-section">
          <h4>基本信息</h4>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="候选人">{{ currentOffer.candidate_name }}</el-descriptions-item>
            <el-descriptions-item label="应聘职位">{{ currentOffer.job_title }}</el-descriptions-item>
            <el-descriptions-item label="岗位">{{ currentOffer.position }}</el-descriptions-item>
            <el-descriptions-item label="薪资范围">{{ currentOffer.salary_min }}-{{ currentOffer.salary_max }}K</el-descriptions-item>
            <el-descriptions-item label="入职日期">{{ currentOffer.join_date }}</el-descriptions-item>
            <el-descriptions-item label="试用期">{{ currentOffer.probation_months }}个月</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="OFFER_STATUS_TYPE[currentOffer.status]">
                {{ OFFER_STATUS_TEXT[currentOffer.status] }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <div class="detail-section" v-if="currentOffer.benefits">
          <h4>福利待遇</h4>
          <p>{{ currentOffer.benefits }}</p>
        </div>
        <div class="detail-section" v-if="currentOffer.attachment_note">
          <h4>附件说明</h4>
          <p>{{ currentOffer.attachment_note }}</p>
        </div>
        <div class="detail-section" v-if="currentOffer.remark">
          <h4>备注</h4>
          <p>{{ currentOffer.remark }}</p>
        </div>
        <div class="detail-section">
          <h4>时间线</h4>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="创建时间">{{ currentOffer.created_at }}</el-descriptions-item>
            <el-descriptions-item label="发送时间" v-if="currentOffer.sent_at">
              {{ currentOffer.sent_at }}
            </el-descriptions-item>
            <el-descriptions-item label="回复时间" v-if="currentOffer.replied_at">
              {{ currentOffer.replied_at }}
            </el-descriptions-item>
            <el-descriptions-item label="拒绝原因" v-if="currentOffer.reject_reason">
              {{ currentOffer.reject_reason }}
            </el-descriptions-item>
            <el-descriptions-item label="撤回原因" v-if="currentOffer.withdraw_reason">
              {{ currentOffer.withdraw_reason }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <div class="detail-actions">
          <el-button v-if="currentOffer.status === 'draft'" type="primary" @click="openEditDialog(currentOffer)">
            编辑
          </el-button>
          <el-button v-if="currentOffer.status === 'draft'" type="success" @click="handleSend(currentOffer)">
            发送
          </el-button>
          <el-button v-if="currentOffer.status === 'draft' || currentOffer.status === 'sent'" type="danger" @click="handleWithdraw(currentOffer)">
            撤回
          </el-button>
          <el-alert
            v-if="currentOffer.status === 'accepted'"
            type="success"
            :closable="false"
            title="该 Offer 已被候选人接受"
            description="候选人已确认接受，请注意跟进入职流程。"
            show-icon
          />
          <el-alert
            v-if="currentOffer.status === 'rejected'"
            type="error"
            :closable="false"
            title="该 Offer 已被候选人拒绝"
            :description="currentOffer.reject_reason ? `拒绝原因：${currentOffer.reject_reason}` : '候选人已拒绝该 Offer'"
            show-icon
          />
          <el-alert
            v-if="currentOffer.status === 'withdrawn'"
            type="warning"
            :closable="false"
            title="该 Offer 已撤回"
            :description="currentOffer.withdraw_reason ? `撤回原因：${currentOffer.withdraw_reason}` : '该 Offer 已被撤回'"
            show-icon
          />
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api, STATUS_TEXT, OFFER_STATUS_TEXT, OFFER_STATUS_TYPE } from '../api'

const route = useRoute()
const router = useRouter()
const refreshStats = inject('refreshStats', () => {})
const refreshAll = inject('refreshAll', () => {})
const refreshDashboardStats = inject('refreshDashboardStats', () => {})

const loading = ref(false)
const offers = ref([])
const jobs = ref([])
const applications = ref([])

const filters = reactive({
  job_id: '',
  status: ''
})

const dialogVisible = ref(false)
const detailVisible = ref(false)
const isEdit = ref(false)
const currentOffer = ref(null)
const formRef = ref(null)

const form = reactive({
  application_id: null,
  position: '',
  salary_min: null,
  salary_max: null,
  join_date: '',
  probation_months: 3,
  benefits: '',
  attachment_note: '',
  remark: ''
})

const rules = {
  application_id: [{ required: true, message: '请选择候选人', trigger: 'change' }],
  position: [{ required: true, message: '请输入岗位名称', trigger: 'blur' }],
  salary_min: [{ required: true, message: '请输入最低薪资', trigger: 'blur' }],
  salary_max: [{ required: true, message: '请输入最高薪资', trigger: 'blur' }],
  join_date: [{ required: true, message: '请选择入职日期', trigger: 'change' }]
}

const candidateOptions = ref([])

const allOffers = ref([])

const offerStats = computed(() => {
  const list = allOffers.value
  const draft = list.filter(o => o.status === 'draft').length
  const sent = list.filter(o => o.status === 'sent').length
  const accepted = list.filter(o => o.status === 'accepted').length
  const rejected = list.filter(o => o.status === 'rejected').length
  const withdrawn = list.filter(o => o.status === 'withdrawn').length
  const processed = accepted + rejected + withdrawn
  return {
    total: list.length,
    draft,
    sent,
    accepted,
    rejected,
    withdrawn,
    processed
  }
})

const canCreateOffer = (app) => {
  return app.passed_interviews && app.passed_interviews > 0
}

const fetchJobs = async () => {
  try {
    jobs.value = await api.getJobs()
  } catch (e) {}
}

const fetchApplications = async () => {
  try {
    const apps = await api.getApplications()
    const interviews = await api.getInterviews()
    apps.forEach(app => {
      const passed = interviews.filter(i => 
        i.application_id === app.id && 
        i.status === 'completed' && 
        i.feedback_result === 'pass'
      )
      app.passed_interviews = passed.length
    })
    applications.value = apps
    candidateOptions.value = apps.filter(a => canCreateOffer(a))
  } catch (e) {}
}

const emptyText = computed(() => {
  const map = {
    '': '暂无 Offer 记录',
    'draft': '暂无草稿状态的 Offer',
    'sent': '暂无已发送的 Offer',
    'accepted': '暂无已接受的 Offer',
    'rejected': '暂无已拒绝的 Offer',
    'withdrawn': '暂无已撤回的 Offer',
    'processed': '暂无已处理的 Offer'
  }
  return map[filters.status] || '暂无 Offer 记录'
})

const fetchList = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.job_id) params.job_id = filters.job_id
    let list = await api.getOffers(params)
    allOffers.value = list
    if (filters.status === 'processed') {
      offers.value = list.filter(o =>
        o.status === 'accepted' || o.status === 'rejected' || o.status === 'withdrawn'
      )
    } else if (filters.status) {
      offers.value = list.filter(o => o.status === filters.status)
    } else {
      offers.value = list
    }
  } catch (e) {}
  loading.value = false
}

const setStatusFilter = (status) => {
  filters.status = status
  onFilterChange()
}

const onFilterChange = () => {
  const query = {}
  if (filters.status) query.status = filters.status
  if (filters.job_id) query.job_id = filters.job_id
  router.replace({ path: '/offers', query })
  fetchList()
}

const resetFilters = () => {
  filters.job_id = ''
  filters.status = ''
  router.replace({ path: '/offers' })
  fetchList()
}

const initFromRoute = () => {
  filters.status = route.query.status || ''
  filters.job_id = route.query.job_id || ''
}

watch(() => route.query, (newQuery) => {
  const newStatus = newQuery.status || ''
  const newJobId = newQuery.job_id || ''
  let changed = false
  if (newStatus !== filters.status) {
    filters.status = newStatus
    changed = true
  }
  if (newJobId !== filters.job_id) {
    filters.job_id = newJobId
    changed = true
  }
  if (changed) {
    fetchList()
  }
}, { immediate: true })

const resetForm = () => {
  form.application_id = null
  form.position = ''
  form.salary_min = null
  form.salary_max = null
  form.join_date = ''
  form.probation_months = 3
  form.benefits = ''
  form.attachment_note = ''
  form.remark = ''
  formRef.value?.clearValidate()
}

const openCreateDialog = async () => {
  isEdit.value = false
  currentOffer.value = null
  resetForm()
  await fetchApplications()
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  currentOffer.value = row
  form.position = row.position
  form.salary_min = row.salary_min
  form.salary_max = row.salary_max
  form.join_date = row.join_date
  form.probation_months = row.probation_months
  form.benefits = row.benefits
  form.attachment_note = row.attachment_note || ''
  form.remark = row.remark
  dialogVisible.value = true
}

const viewDetail = async (row) => {
  try {
    const res = await api.getOffer(row.id)
    currentOffer.value = res.offer
  } catch (e) {
    currentOffer.value = row
  }
  detailVisible.value = true
}

const handleSave = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }
  try {
    if (isEdit.value) {
      await api.updateOffer(currentOffer.value.id, {
        position: form.position,
        salary_min: form.salary_min,
        salary_max: form.salary_max,
        join_date: form.join_date,
        probation_months: form.probation_months,
        benefits: form.benefits,
        attachment_note: form.attachment_note,
        remark: form.remark
      })
      ElMessage.success('Offer 已更新')
    } else {
      await api.createOffer(form.application_id, {
        position: form.position,
        salary_min: form.salary_min,
        salary_max: form.salary_max,
        join_date: form.join_date,
        probation_months: form.probation_months,
        benefits: form.benefits,
        attachment_note: form.attachment_note,
        remark: form.remark
      })
      ElMessage.success('Offer 草稿已创建')
    }
    dialogVisible.value = false
    fetchList()
    refreshStats()
    refreshDashboardStats()
  } catch (e) {
    ElMessage.error(e.message || '操作失败')
  }
}

const handleSend = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认将 Offer 发送给 ${row.candidate_name}？发送后候选人将收到通知。`,
      '发送 Offer',
      { type: 'warning' }
    )
    await api.sendOffer(row.id)
    ElMessage.success('Offer 已发送')
    fetchList()
    refreshStats()
    refreshDashboardStats()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message || '发送失败')
  }
}

const handleWithdraw = async (row) => {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      '请输入撤回原因',
      '撤回 Offer',
      {
        confirmButtonText: '确认撤回',
        cancelButtonText: '取消',
        inputType: 'textarea',
        inputPlaceholder: '请输入撤回原因',
        inputValidator: (val) => {
          if (!val || !val.trim()) {
            return '请输入撤回原因'
          }
          return true
        }
      }
    )
    await api.withdrawOffer(row.id, reason)
    ElMessage.success('Offer 已撤回')
    fetchList()
    refreshStats()
    refreshDashboardStats()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message || '撤回失败')
  }
}

onMounted(() => {
  fetchJobs()
  initFromRoute()
  fetchList()
})
</script>

<style scoped>
.offers-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.filter-card {
  margin-bottom: 16px;
}

.stats-card {
  margin-bottom: 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.stat-item {
  flex: 1;
  min-width: 80px;
  text-align: center;
  padding: 12px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  background: #f5f7fa;
}

.stat-item:hover {
  background: #ecf5ff;
}

.stat-item.active {
  background: #ecf5ff;
  border: 1px solid #409eff;
}

.stat-item.active .stat-num {
  color: #409eff;
}

.stat-num {
  font-size: 22px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.list-card {
  margin-bottom: 20px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.offer-detail .detail-section {
  margin-bottom: 20px;
}

.offer-detail .detail-section h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.offer-detail p {
  margin: 0;
  line-height: 1.6;
  color: #606266;
}

.detail-actions {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
</style>
