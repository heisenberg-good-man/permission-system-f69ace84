<template>
  <div class="dashboard-page">
    <div class="page-header">
      <h2>招聘工作台</h2>
      <p class="subtitle">快速查看待办事项，点击卡片进入对应页面</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card stat-card-interview" @click="goToInterviews">
        <div class="stat-icon">
          <el-icon><Calendar /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.scheduled_interviews || 0 }}</div>
          <div class="stat-label">待安排面试</div>
          <div class="stat-desc">已安排未完成的面试</div>
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
          <div class="stat-value">{{ draftOfferCount }}</div>
          <div class="stat-label">待发送 Offer</div>
          <div class="stat-desc">草稿状态的 Offer</div>
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
          <div class="stat-value">{{ processedOfferCount }}</div>
          <div class="stat-label">候选人已处理 Offer</div>
          <div class="stat-desc">已接受/已拒绝的 Offer</div>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="panel">
        <div class="panel-header">
          <h3>招聘概览</h3>
        </div>
        <div class="overview-grid">
          <div class="overview-item">
            <div class="overview-value">{{ stats.total_applications || 0 }}</div>
            <div class="overview-label">总投递数</div>
          </div>
          <div class="overview-item">
            <div class="overview-value">{{ stats.pending_applications || 0 }}</div>
            <div class="overview-label">新投递</div>
          </div>
          <div class="overview-item">
            <div class="overview-value">{{ stats.screening || 0 }}</div>
            <div class="overview-label">待沟通</div>
          </div>
          <div class="overview-item">
            <div class="overview-value">{{ stats.communicating || 0 }}</div>
            <div class="overview-label">沟通中</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Calendar, Document, Check, ArrowRight } from '@element-plus/icons-vue'
import { api } from '../api'

const router = useRouter()
const route = useRoute()
const stats = ref({})
const offers = ref([])
const refreshStats = inject('refreshStats')

const draftOfferCount = computed(() => {
  return offers.value.filter(o => o.status === 'draft').length
})

const processedOfferCount = computed(() => {
  return offers.value.filter(o => o.status === 'accepted' || o.status === 'rejected').length
})

const fetchStats = async () => {
  try {
    const data = await api.getStats()
    stats.value = data
  } catch (e) {}
}

const fetchOffers = async () => {
  try {
    offers.value = await api.getOffers()
  } catch (e) {}
}

const goToInterviews = () => {
  router.push('/interviews')
}

const goToOffers = (tab) => {
  router.push({ path: '/offers', query: { tab } })
}

const loadData = () => {
  fetchStats()
  fetchOffers()
}

watch(() => route.path, (newPath) => {
  if (newPath === '/dashboard') {
    loadData()
  }
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard-page {
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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

.stat-card-interview::before {
  background: #409eff;
}

.stat-card-offer::before {
  background: #e6a23c;
}

.stat-card-processed::before {
  background: #67c23a;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  margin-right: 20px;
  flex-shrink: 0;
}

.stat-card-interview .stat-icon {
  background: #409eff;
}

.stat-card-offer .stat-icon {
  background: #e6a23c;
}

.stat-card-processed .stat-icon {
  background: #67c23a;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 16px;
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
  font-size: 20px;
  margin-left: 12px;
  transition: transform 0.3s;
}

.stat-card:hover .stat-arrow {
  transform: translateX(4px);
  color: #909399;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.panel-header {
  margin-bottom: 16px;
}

.panel-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.overview-item {
  text-align: center;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.overview-value {
  font-size: 28px;
  font-weight: 600;
  color: #409eff;
}

.overview-label {
  font-size: 14px;
  color: #606266;
  margin-top: 4px;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .overview-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .overview-grid {
    grid-template-columns: 1fr;
  }
}
</style>
