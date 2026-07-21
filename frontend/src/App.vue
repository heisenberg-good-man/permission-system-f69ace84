<template>
  <el-container class="app-layout">
    <el-header class="app-header">
      <div class="header-left">
        <el-icon class="logo-icon"><Briefcase /></el-icon>
        <span class="app-title">招聘平台工作台</span>
      </div>
      <div class="header-center">
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          router
          class="nav-menu"
          background-color="transparent"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item v-if="role === 'candidate'" index="/jobs">
            <el-icon><OfficeBuilding /></el-icon>
            <span>职位浏览</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'candidate'" index="/my-applications">
            <el-icon><Document /></el-icon>
            <span>我的投递</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'candidate'" index="/my-interviews">
            <el-icon><Calendar /></el-icon>
            <span>我的面试</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'candidate'" index="/my-offers">
            <el-icon><Present /></el-icon>
            <span>我的 Offer</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'recruiter'" index="/dashboard">
            <el-icon><DataBoard /></el-icon>
            <span>工作台</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'recruiter'" index="/job-manage">
            <el-icon><Edit /></el-icon>
            <span>职位管理</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'recruiter'" index="/applications">
            <el-icon><User /></el-icon>
            <span>候选人</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'recruiter'" index="/interviews">
            <el-icon><Calendar /></el-icon>
            <span>面试安排</span>
          </el-menu-item>
          <el-menu-item v-if="role === 'recruiter'" index="/offers">
            <el-icon><Present /></el-icon>
            <span>Offer 管理</span>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="header-right">
        <el-radio-group v-model="role" size="default" @change="onRoleChange">
          <el-radio-button label="candidate">
            <el-icon><Avatar /></el-icon>
            应聘方
          </el-radio-button>
          <el-radio-button label="recruiter">
            <el-icon><OfficeBuilding /></el-icon>
            招聘方
          </el-radio-button>
        </el-radio-group>
        <el-button type="danger" plain size="small" @click="handleReset">
          <el-icon><RefreshLeft /></el-icon>
          重置数据
        </el-button>
      </div>
    </el-header>

    <div class="stats-bar">
      <div class="stats-container">
        <div class="stat-card" v-for="item in statItems" :key="item.label">
          <div class="stat-icon" :style="{ background: item.color }">
            <el-icon :size="24"><component :is="item.icon" /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ item.value }}</div>
            <div class="stat-label">{{ item.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <el-main class="app-main">
      <div v-if="!appReady" class="init-loading">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
        <p>初始化中...</p>
      </div>
      <router-view v-else :key="$route.fullPath + '-' + role + '-' + dataVersion" />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, provide, watch, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import { api, STATUS_TEXT, STATUS_TYPE, INTERVIEW_STATUS_TEXT, INTERVIEW_STATUS_TYPE, INTERVIEW_WAY_TEXT, INTERVIEW_ROUNDS } from './api'
import request from './api'

const route = useRoute()
const router = useRouter()
const role = ref(localStorage.getItem('role') || 'candidate')
const stats = ref({})
const dashboardStats = reactive({ data: {} })
const dataVersion = ref(0)
const appReady = ref(false)
const currentCandidateName = ref('李四')

const activeMenu = computed(() => route.path)

const statItems = computed(() => {
  if (role.value === 'recruiter') {
    return [
      { label: '职位总数', value: stats.value.total_jobs || 0, icon: 'Briefcase', color: '#409eff' },
      { label: '招聘中', value: stats.value.open_jobs || 0, icon: 'CircleCheck', color: '#67c23a' },
      { label: '总投递', value: stats.value.total_applications || 0, icon: 'Document', color: '#e6a23c' },
      { label: '新投递', value: stats.value.pending_applications || 0, icon: 'Bell', color: '#f56c6c' },
      { label: '待沟通', value: stats.value.screening || 0, icon: 'Clock', color: '#909399' },
      { label: '沟通中', value: stats.value.communicating || 0, icon: 'ChatDotRound', color: '#67c23a' },
      { label: '待面试', value: stats.value.scheduled_interviews || 0, icon: 'Calendar', color: '#e6a23c' },
      { label: '待发Offer', value: stats.value.sent_offers || 0, icon: 'Present', color: '#9b59b6' },
      { label: '已录用', value: stats.value.hired || 0, icon: 'CircleCheckFilled', color: '#67c23a' }
    ]
  } else {
    return [
      { label: '在招职位', value: stats.value.open_jobs || 0, icon: 'Briefcase', color: '#409eff' },
      { label: '总投递', value: stats.value.total_applications || 0, icon: 'Document', color: '#67c23a' },
      { label: '待沟通', value: stats.value.screening || 0, icon: 'Clock', color: '#e6a23c' },
      { label: '沟通中', value: stats.value.communicating || 0, icon: 'ChatDotRound', color: '#909399' },
      { label: '待面试', value: stats.value.scheduled_interviews || 0, icon: 'Calendar', color: '#e6a23c' },
      { label: '待处理Offer', value: stats.value.sent_offers || 0, icon: 'Present', color: '#9b59b6' },
      { label: '不合适', value: stats.value.rejected || 0, icon: 'Close', color: '#f56c6c' }
    ]
  }
})

const fetchStats = async () => {
  try {
    stats.value = await api.getStats()
  } catch (e) {}
}

const refreshAll = async () => {
  dataVersion.value++
  await fetchStats()
  await refreshDashboardStats()
}

const refreshDashboardStats = async () => {
  try {
    const data = await api.getDashboardStats()
    Object.assign(dashboardStats.data, data)
  } catch (e) {}
}

const onRoleChange = () => {
  localStorage.setItem('role', role.value)
  localStorage.setItem('candidateName', currentCandidateName.value)
  request.defaults.headers.common['x-role'] = role.value
  request.defaults.headers.common['x-candidate-name'] = currentCandidateName.value
  if (role.value === 'recruiter') {
    router.push('/job-manage')
  } else {
    router.push('/jobs')
  }
  fetchStats()
}

const handleReset = async () => {
  try {
    await ElMessageBox.confirm('确定要重置所有数据到初始状态吗？', '提示', {
      type: 'warning'
    })
    await api.resetData()
    ElMessage.success('数据已重置为初始状态')
    dataVersion.value++
    fetchStats()
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

const initData = async () => {
  if (appReady.value) return
  request.defaults.headers.common['x-role'] = role.value
  request.defaults.headers.common['x-candidate-name'] = currentCandidateName.value
  try {
    await api.resetData()
  } catch (e) {}
  await fetchStats()
  await refreshDashboardStats()
  dataVersion.value++
  appReady.value = true
}

provide('refreshStats', fetchStats)
provide('refreshAll', refreshAll)
provide('dashboardStats', dashboardStats)
provide('refreshDashboardStats', refreshDashboardStats)
provide('role', role)
provide('currentCandidateName', currentCandidateName)
provide('STATUS_TEXT', STATUS_TEXT)
provide('STATUS_TYPE', STATUS_TYPE)
provide('INTERVIEW_STATUS_TEXT', INTERVIEW_STATUS_TEXT)
provide('INTERVIEW_STATUS_TYPE', INTERVIEW_STATUS_TYPE)
provide('INTERVIEW_WAY_TEXT', INTERVIEW_WAY_TEXT)
provide('INTERVIEW_ROUNDS', INTERVIEW_ROUNDS)

const appActions = {
  refreshStats: fetchStats,
  refreshAll,
  refreshDashboardStats
}
provide('appActions', appActions)

onMounted(() => {
  initData()
})

watch(() => route.path, () => {
  fetchStats()
})
</script>

<style scoped>
.app-layout {
  height: 100%;
}

.app-header {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: #fff;
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.header-left {
  display: flex;
  align-items: center;
  margin-right: 40px;
}

.logo-icon {
  font-size: 28px;
  margin-right: 12px;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  white-space: nowrap;
}

.header-center {
  flex: 1;
}

.nav-menu {
  border-bottom: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stats-bar {
  background: #fff;
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.stats-container {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.stat-card {
  display: flex;
  align-items: center;
  background: #f9fafb;
  border-radius: 8px;
  padding: 12px 20px;
  min-width: 140px;
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 12px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.app-main {
  background: #f0f2f5;
  padding: 0;
  overflow-y: auto;
}

.init-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  gap: 12px;
}

.init-loading p {
  margin: 0;
}
</style>
