<template>
  <div class="page-container">
    <div class="page-header card">
      <div class="page-title">
        <el-icon><Document /></el-icon>
        我的投递
      </div>
      <div class="header-actions">
        <el-radio-group v-model="statusFilter" size="default" @change="fetchData">
          <el-radio-button value="">全部</el-radio-button>
          <el-radio-button value="pending">新投递</el-radio-button>
          <el-radio-button value="screening">待沟通</el-radio-button>
          <el-radio-button value="communicating">沟通中</el-radio-button>
          <el-radio-button value="rejected">不合适</el-radio-button>
        </el-radio-group>
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
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="STATUS_TYPE[row.status]" size="small">
              {{ STATUS_TEXT[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applied_at" label="投递时间" width="180" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="goComm(row.id)">
              查看沟通
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && filteredApps.length === 0" description="暂无投递记录" :image-size="80" style="padding: 40px 0" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'

const router = useRouter()
const refreshStats = inject('refreshStats')
const STATUS_TEXT = inject('STATUS_TEXT')
const STATUS_TYPE = inject('STATUS_TYPE')

const applications = ref([])
const loading = ref(false)
const statusFilter = ref('')

const filteredApps = computed(() => {
  if (!statusFilter.value) return applications.value
  return applications.value.filter(a => a.status === statusFilter.value)
})

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
}
</style>
