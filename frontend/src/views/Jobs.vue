<template>
  <div class="page-container">
    <div class="page-header card">
      <div class="page-title">
        <el-icon><Search /></el-icon>
        职位列表
      </div>
      <div class="filter-bar">
        <el-input
          v-model="keyword"
          placeholder="搜索职位名称/公司"
          clearable
          style="width: 280px"
          :prefix-icon="Search"
          @input="fetchJobs"
        />
        <el-select v-model="cityFilter" placeholder="城市" clearable style="width: 140px" @change="fetchJobs">
          <el-option v-for="c in cities" :key="c" :label="c" :value="c" />
        </el-select>
        <el-select v-model="statusFilter" placeholder="状态" clearable style="width: 140px" @change="fetchJobs">
          <el-option label="招聘中" value="open" />
          <el-option label="已关闭" value="closed" />
        </el-select>
      </div>
    </div>

    <div class="job-list">
      <div v-if="loading" class="loading">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
        <p>加载中...</p>
      </div>
      <div v-else-if="filteredJobs.length === 0" class="empty">
        <el-empty description="暂无职位" />
      </div>
      <div v-else class="job-grid">
        <div
          v-for="job in filteredJobs"
          :key="job.id"
          class="job-card"
          @click="goToDetail(job.id)"
        >
          <div class="job-card-header">
            <h3 class="job-title">{{ job.title }}</h3>
            <el-tag :type="job.status === 'open' ? 'success' : 'info'" size="small">
              {{ job.status === 'open' ? '招聘中' : '已关闭' }}
            </el-tag>
          </div>
          <div class="job-salary">
            {{ formatSalary(job.salary_min, job.salary_max) }}
          </div>
          <div class="job-meta">
            <span><el-icon><OfficeBuilding /></el-icon> {{ job.company }}</span>
            <span><el-icon><Location /></el-icon> {{ job.city }}</span>
            <span><el-icon><Clock /></el-icon> {{ job.experience }}</span>
            <span><el-icon><Reading /></el-icon> {{ job.education }}</span>
          </div>
          <div class="job-desc">{{ job.description }}</div>
          <div class="job-card-footer">
            <span class="hr-name">HR: {{ job.hr_name }}</span>
            <span class="post-time">{{ job.created_at }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Loading } from '@element-plus/icons-vue'
import { api } from '../api'

const router = useRouter()
const refreshStats = inject('refreshStats')

const jobs = ref([])
const loading = ref(false)
const keyword = ref('')
const cityFilter = ref('')
const statusFilter = ref('open')

const cities = computed(() => {
  const set = new Set(jobs.value.map(j => j.city).filter(Boolean))
  return Array.from(set)
})

const filteredJobs = computed(() => {
  return jobs.value.filter(j => {
    if (keyword.value) {
      const kw = keyword.value.toLowerCase()
      if (!j.title.toLowerCase().includes(kw) && !j.company.toLowerCase().includes(kw)) {
        return false
      }
    }
    if (cityFilter.value && j.city !== cityFilter.value) return false
    if (statusFilter.value && j.status !== statusFilter.value) return false
    return true
  })
})

const fetchJobs = async () => {
  loading.value = true
  try {
    jobs.value = await api.getJobs()
  } finally {
    loading.value = false
  }
}

const formatSalary = (min, max) => {
  if (!min && !max) return '面议'
  return `${(min / 1000).toFixed(0)}K - ${(max / 1000).toFixed(0)}K`
}

const goToDetail = (id) => {
  router.push(`/jobs/${id}`)
}

onMounted(() => {
  fetchJobs()
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

.filter-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.job-list {
  min-height: 400px;
}

.loading, .empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #909399;
}

.loading p {
  margin-top: 12px;
}

.job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}

.job-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  border: 1px solid transparent;
}

.job-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  transform: translateY(-2px);
  border-color: #3b82f6;
}

.job-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.job-title {
  font-size: 17px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  line-height: 1.4;
}

.job-salary {
  font-size: 18px;
  font-weight: 700;
  color: #f56c6c;
  margin-bottom: 12px;
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 12px;
}

.job-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.job-desc {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.job-card-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #9ca3af;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}
</style>
