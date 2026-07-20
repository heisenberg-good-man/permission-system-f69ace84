<template>
  <div class="page-container">
    <div class="page-header card">
      <div class="page-title">
        <el-icon><User /></el-icon>
        候选人管理
      </div>
      <div class="header-actions">
        <el-input
          v-model="keyword"
          placeholder="搜索候选人姓名/职位"
          clearable
          style="width: 240px"
          :prefix-icon="Search"
        />
        <el-select v-model="jobFilter" placeholder="职位" clearable style="width: 180px">
          <el-option v-for="j in jobs" :key="j.id" :label="j.title" :value="j.id" />
        </el-select>
        <el-select v-model="statusFilter" placeholder="状态" clearable style="width: 140px">
          <el-option label="待处理" value="pending" />
          <el-option label="沟通中" value="communicating" />
          <el-option label="不合适" value="rejected" />
          <el-option label="已录用" value="hired" />
        </el-select>
      </div>
    </div>

    <div class="card">
      <el-table :data="filteredApps" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="candidate_name" label="姓名" width="100" />
        <el-table-column prop="job_title" label="应聘职位" min-width="140" />
        <el-table-column prop="education" label="学历" width="80" />
        <el-table-column prop="experience" label="经验" width="100" />
        <el-table-column prop="candidate_phone" label="手机" width="130" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applied_at" label="投递时间" width="160" />
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">查看简历</el-button>
            <el-button type="success" link size="small" @click="goComm(row)">沟通</el-button>
            <el-dropdown trigger="click" @command="(c) => changeStatus(row, c)">
              <el-button link size="small">
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
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="detailVisible" title="候选人详情" width="560px">
      <div v-if="currentApp" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">{{ currentApp.candidate_name }}</el-descriptions-item>
          <el-descriptions-item label="应聘职位">{{ currentApp.job_title }}</el-descriptions-item>
          <el-descriptions-item label="手机">{{ currentApp.candidate_phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ currentApp.candidate_email }}</el-descriptions-item>
          <el-descriptions-item label="学历">{{ currentApp.education }}</el-descriptions-item>
          <el-descriptions-item label="工作经验">{{ currentApp.experience }}</el-descriptions-item>
          <el-descriptions-item label="投递时间" :span="2">{{ currentApp.applied_at }}</el-descriptions-item>
          <el-descriptions-item label="当前状态" :span="2">
            <el-tag :type="statusType(currentApp.status)">{{ statusText(currentApp.status) }}</el-tag>
          </el-descriptions-item>
        </el-descriptions>
        <div style="margin-top: 16px">
          <h4 style="margin-bottom: 8px; color: #374151;">简历内容</h4>
          <div style="background: #f9fafb; padding: 12px; border-radius: 6px; white-space: pre-line; color: #4b5563; line-height: 1.6;">
            {{ currentApp.resume }}
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="goComm(currentApp)">去沟通</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { api } from '../api'

const router = useRouter()
const refreshStats = inject('refreshStats')

const applications = ref([])
const jobs = ref([])
const loading = ref(false)
const keyword = ref('')
const jobFilter = ref('')
const statusFilter = ref('')
const detailVisible = ref(false)
const currentApp = ref(null)

const filteredApps = computed(() => {
  return applications.value.filter(a => {
    if (keyword.value) {
      const kw = keyword.value.toLowerCase()
      if (!a.candidate_name.toLowerCase().includes(kw) && !a.job_title.toLowerCase().includes(kw)) return false
    }
    if (jobFilter.value && a.job_id !== jobFilter.value) return false
    if (statusFilter.value && a.status !== statusFilter.value) return false
    return true
  })
})

const statusText = (s) => {
  const map = { pending: '待处理', communicating: '沟通中', rejected: '不合适', hired: '已录用' }
  return map[s] || s
}

const statusType = (s) => {
  const map = { pending: 'warning', communicating: 'primary', rejected: 'danger', hired: 'success' }
  return map[s] || 'info'
}

const fetchData = async () => {
  loading.value = true
  try {
    const [appsData, jobsData] = await Promise.all([
      api.getApplications(),
      api.getJobs()
    ])
    applications.value = appsData
    jobs.value = jobsData
  } finally {
    loading.value = false
  }
}

const viewDetail = (row) => {
  currentApp.value = row
  detailVisible.value = true
}

const goComm = (row) => {
  if (!row) return
  router.push(`/communication/${row.id}`)
}

const changeStatus = async (row, status) => {
  await api.updateApplicationStatus(row.id, status)
  row.status = status
  ElMessage.success('状态已更新')
  refreshStats()
}

onMounted(() => {
  fetchData()
  refreshStats()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.header-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.detail-content {
  font-size: 14px;
}
</style>
