<template>
  <div class="page-container">
    <div class="page-header card">
      <div class="page-title">
        <el-icon><Document /></el-icon>
        我的投递
      </div>
      <div class="header-actions">
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
        <el-table-column prop="job_title" label="应聘职位" min-width="160">
          <template #default="{ row }">
            <el-link type="primary" @click="viewJob(row.job_id)">{{ row.job_title }}</el-link>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applied_at" label="投递时间" width="160" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="goComm(row.id)">
              查看沟通
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'

const router = useRouter()
const refreshStats = inject('refreshStats')

const applications = ref([])
const loading = ref(false)
const statusFilter = ref('')

const filteredApps = computed(() => {
  if (!statusFilter.value) return applications.value
  return applications.value.filter(a => a.status === statusFilter.value)
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
    applications.value = await api.getApplications()
  } finally {
    loading.value = false
  }
}

const viewJob = (id) => {
  router.push(`/jobs/${id}`)
}

const goComm = (id) => {
  router.push(`/communication/${id}`)
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
}
</style>
