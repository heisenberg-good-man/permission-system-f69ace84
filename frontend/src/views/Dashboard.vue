<template>
  <div class="dashboard-page">
    <div class="page-header">
      <div>
        <h2>招聘工作台</h2>
        <p class="subtitle">快速查看待办事项与数据概览</p>
      </div>
    </div>

    <div class="filter-bar">
      <el-form :inline="true" :model="filters" @submit.prevent>
        <el-form-item label="职位">
          <el-select v-model="filters.job_id" placeholder="全部职位" clearable style="width: 200px" @change="fetchDashboardStats">
            <el-option v-for="job in jobList" :key="job.id" :label="job.title" :value="job.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-radio-group v-model="filters.timeRange" @change="fetchDashboardStats">
            <el-radio-button value="all">全部</el-radio-button>
            <el-radio-button value="today">今日</el-radio-button>
            <el-radio-button value="week">本周</el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </div>

    <div class="section-title">
      <h3>待办事项</h3>
      <span class="section-desc">点击卡片进入对应页面处理</span>
    </div>

    <div class="stats-grid">
      <div class="stat-card stat-card-interview" @click="goToInterviews">
        <div class="stat-icon">
          <el-icon><Calendar /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.scheduled_interviews || 0 }}</div>
          <div class="stat-label">待安排面试</div>
          <div class="stat-desc">已安排未完成</div>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>

      <div class="stat-card stat-card-offer" @click="goToOffers('draft')">
        <div class="stat-icon">
          <el-icon><Document /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.draft_offers || 0 }}</div>
          <div class="stat-label">待发送 Offer</div>
          <div class="stat-desc">草稿状态</div>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>

      <div class="stat-card stat-card-sent" @click="goToOffers('sent')">
        <div class="stat-icon">
          <el-icon><Promotion /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.sent_offers || 0 }}</div>
          <div class="stat-label">待候选人回复</div>
          <div class="stat-desc">已发送待处理</div>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>

      <div class="stat-card stat-card-processed" @click="goToOffers('processed')">
        <div class="stat-icon">
          <el-icon><Check /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.processed_offers || 0 }}</div>
          <div class="stat-label">已处理 Offer</div>
          <div class="stat-desc">接受/拒绝/撤回</div>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>
    </div>

    <div class="section-title">
      <h3>核心指标</h3>
    </div>

    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-header">
          <span class="metric-label">职位</span>
        </div>
        <div class="metric-value">{{ stats.open_jobs || 0 }}</div>
        <div class="metric-sub">招聘中 / 共 {{ stats.total_jobs || 0 }} 个</div>
      </div>

      <div class="metric-card">
        <div class="metric-header">
          <span class="metric-label">活跃投递</span>
        </div>
        <div class="metric-value">{{ stats.active_applications || 0 }}</div>
        <div class="metric-sub">新投递+待沟通+沟通中</div>
      </div>

      <div class="metric-card">
        <div class="metric-header">
          <span class="metric-label">今日面试</span>
        </div>
        <div class="metric-value">{{ stats.today_interviews || 0 }}</div>
        <div class="metric-sub">本周 {{ stats.week_interviews || 0 }} 场</div>
      </div>

      <div class="metric-card">
        <div class="metric-header">
          <span class="metric-label">Offer 总数</span>
        </div>
        <div class="metric-value">{{ stats.total_offers || 0 }}</div>
        <div class="metric-sub">已录用 {{ stats.hired || 0 }} 人</div>
      </div>
    </div>

    <div class="section-title">
      <h3>候选人转化漏斗</h3>
    </div>

    <div class="funnel-card">
      <div class="funnel-item" style="width: 100%">
        <div class="funnel-label">总投递</div>
        <div class="funnel-value">{{ stats.conversion?.applications || 0 }}</div>
      </div>
      <div class="funnel-arrow">
        <el-icon><Bottom /></el-icon>
      </div>
      <div class="funnel-item" style="width: 75%">
        <div class="funnel-label">进入面试</div>
        <div class="funnel-value">{{ stats.conversion?.to_interview || 0 }} 场</div>
      </div>
      <div class="funnel-arrow">
        <el-icon><Bottom /></el-icon>
        <span class="funnel-rate">通过率 {{ stats.conversion?.interview_pass_rate || 0 }}%</span>
      </div>
      <div class="funnel-item" style="width: 50%">
        <div class="funnel-label">发出 Offer</div>
        <div class="funnel-value">{{ stats.conversion?.to_offer || 0 }} 份</div>
      </div>
      <div class="funnel-arrow">
        <el-icon><Bottom /></el-icon>
        <span class="funnel-rate">接受率 {{ stats.conversion?.offer_accept_rate || 0 }}%</span>
      </div>
      <div class="funnel-item funnel-item-final" style="width: 30%">
        <div class="funnel-label">已录用</div>
        <div class="funnel-value">{{ stats.conversion?.to_hire || 0 }} 人</div>
      </div>
    </div>

    <div class="section-title">
      <h3>投递状态分布</h3>
    </div>

    <div class="status-grid">
      <div class="status-item status-pending">
        <div class="status-value">{{ stats.pending_applications || 0 }}</div>
        <div class="status-label">新投递</div>
      </div>
      <div class="status-item status-screening">
        <div class="status-value">{{ stats.screening || 0 }}</div>
        <div class="status-label">待沟通</div>
      </div>
      <div class="status-item status-communicating">
        <div class="status-value">{{ stats.communicating || 0 }}</div>
        <div class="status-label">沟通中</div>
      </div>
      <div class="status-item status-rejected">
        <div class="status-value">{{ stats.rejected || 0 }}</div>
        <div class="status-label">不合适</div>
      </div>
      <div class="status-item status-hired">
        <div class="status-value">{{ stats.hired || 0 }}</div>
        <div class="status-label">已录用</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Calendar, Document, Check, ArrowRight, Bottom, Promotion } from '@element-plus/icons-vue'
import { api } from '../api'

const router = useRouter()
const route = useRoute()
const globalDashboardStats = inject('dashboardStats')
const refreshDashboardStats = inject('refreshDashboardStats')
const refreshStats = inject('refreshStats')

const jobList = ref([])

const filters = reactive({
  job_id: null,
  timeRange: 'all'
})

const stats = computed(() => {
  if (filters.job_id || filters.timeRange !== 'all') {
    return localStats.value
  }
  return globalDashboardStats?.data || {}
})

const localStats = ref({})

const formatLocalDate = (date) => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

const getDateRange = () => {
  const now = new Date()
  let start_date = ''
  let end_date = ''
  if (filters.timeRange === 'today') {
    const today = formatLocalDate(now)
    start_date = today
    end_date = today
  } else if (filters.timeRange === 'week') {
    const day = now.getDay()
    const diff = now.getDate() - day + (day === 0 ? -6 : 1)
    const monday = new Date(now.getFullYear(), now.getMonth(), diff)
    start_date = formatLocalDate(monday)
    const sunday = new Date(monday.getFullYear(), monday.getMonth(), monday.getDate() + 6)
    end_date = formatLocalDate(sunday)
  }
  return { start_date, end_date }
}

const fetchDashboardStats = async () => {
  try {
    const params = {}
    if (filters.job_id) params.job_id = filters.job_id
    const { start_date, end_date } = getDateRange()
    if (start_date) params.start_date = start_date
    if (end_date) params.end_date = end_date
    const data = await api.getDashboardStats(params)
    localStats.value = data
    if (data.job_list) {
      jobList.value = data.job_list
    }
    if (!filters.job_id && filters.timeRange === 'all') {
      Object.assign(globalDashboardStats.data, data)
    }
  } catch (e) {}
}

const goToInterviews = () => {
  const query = {}
  if (filters.job_id) query.job_id = filters.job_id
  router.push({ path: '/interviews', query })
}

const goToOffers = (status) => {
  const query = {}
  if (status) query.status = status
  if (filters.job_id) query.job_id = filters.job_id
  router.push({ path: '/offers', query })
}

const loadData = () => {
  fetchDashboardStats()
}

watch(() => route.path, (newPath) => {
  if (newPath === '/dashboard') {
    loadData()
  }
})

onMounted(() => {
  if (globalDashboardStats?.data?.job_list) {
    jobList.value = globalDashboardStats.data.job_list
  }
  loadData()
})

defineExpose({
  refresh: loadData
})
</script>

<style scoped>
.dashboard-page {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100%;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 4px 0;
  font-size: 24px;
  color: #303133;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.filter-bar {
  background: #fff;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.section-title {
  display: flex;
  align-items: baseline;
  margin: 24px 0 16px 0;
}

.section-title h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  font-weight: 600;
}

.section-desc {
  margin-left: 12px;
  font-size: 13px;
  color: #909399;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
}

.stat-card-interview::before { background: #409eff; }
.stat-card-offer::before { background: #e6a23c; }
.stat-card-sent::before { background: #9b59b6; }
.stat-card-processed::before { background: #67c23a; }

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #fff;
  margin-right: 16px;
  flex-shrink: 0;
}

.stat-card-interview .stat-icon { background: #409eff; }
.stat-card-offer .stat-icon { background: #e6a23c; }
.stat-card-sent .stat-icon { background: #9b59b6; }
.stat-card-processed .stat-icon { background: #67c23a; }

.stat-content { flex: 1; }

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-top: 4px;
}

.stat-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.stat-arrow {
  color: #c0c4cc;
  font-size: 18px;
  margin-left: 8px;
  transition: transform 0.3s;
}

.stat-card:hover .stat-arrow {
  transform: translateX(4px);
  color: #909399;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.metric-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.metric-header {
  margin-bottom: 8px;
}

.metric-label {
  font-size: 14px;
  color: #909399;
}

.metric-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.metric-sub {
  font-size: 13px;
  color: #909399;
  margin-top: 6px;
}

.funnel-card {
  background: #fff;
  padding: 30px 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.funnel-item {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: #fff;
  padding: 16px 24px;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 50px;
  transition: all 0.3s;
}

.funnel-item:hover {
  transform: scale(1.02);
}

.funnel-label {
  font-size: 15px;
  font-weight: 500;
}

.funnel-value {
  font-size: 20px;
  font-weight: 600;
}

.funnel-item-final {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.funnel-arrow {
  color: #c0c4cc;
  font-size: 18px;
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
}

.funnel-rate {
  font-size: 12px;
  color: #909399;
  font-weight: 500;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.status-item {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border-top: 3px solid transparent;
}

.status-pending { border-top-color: #f56c6c; }
.status-screening { border-top-color: #e6a23c; }
.status-communicating { border-top-color: #409eff; }
.status-rejected { border-top-color: #909399; }
.status-hired { border-top-color: #67c23a; }

.status-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.status-label {
  font-size: 14px;
  color: #606266;
  margin-top: 6px;
}

@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .status-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .funnel-card {
    padding: 20px;
  }
}
</style>
