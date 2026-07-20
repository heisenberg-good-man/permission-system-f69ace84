<template>
  <div class="page-container">
    <div class="page-header card">
      <div class="page-title">
        <el-icon><Edit /></el-icon>
        职位管理
      </div>
      <div class="header-actions">
        <el-input
          v-model="keyword"
          placeholder="搜索职位"
          clearable
          style="width: 240px"
          :prefix-icon="Search"
        />
        <el-select v-model="statusFilter" placeholder="状态" clearable style="width: 140px">
          <el-option label="招聘中" value="open" />
          <el-option label="已关闭" value="closed" />
        </el-select>
        <el-button type="primary" @click="openCreateDialog">
          <el-icon><Plus /></el-icon>
          发布新职位
        </el-button>
      </div>
    </div>

    <div class="card">
      <el-table :data="filteredJobs" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="职位名称" min-width="160">
          <template #default="{ row }">
            <el-link type="primary" @click="viewJob(row.id)">{{ row.title }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="department" label="部门" width="100" />
        <el-table-column label="薪资" width="140">
          <template #default="{ row }">
            <span class="salary">{{ formatSalary(row.salary_min, row.salary_max) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="city" label="城市" width="80" />
        <el-table-column prop="experience" label="经验" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'open' ? 'success' : 'info'" size="small">
              {{ row.status === 'open' ? '招聘中' : '已关闭' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="投递数" width="80">
          <template #default="{ row }">
            <el-tag type="warning" size="small">{{ getApplyCount(row.id) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="160" />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="editJob(row)">编辑</el-button>
            <el-button link size="small" @click="toggleStatus(row)">
              {{ row.status === 'open' ? '关闭' : '开启' }}
            </el-button>
            <el-button type="danger" link size="small" @click="deleteJob(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="editingJob ? '编辑职位' : '发布新职位'"
      width="640px"
      @close="resetForm"
    >
      <el-form :model="form" label-width="100px" label-position="right">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="职位名称">
              <el-input v-model="form.title" placeholder="请输入职位名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属部门">
              <el-input v-model="form.department" placeholder="请输入部门" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="公司">
              <el-input v-model="form.company" placeholder="公司名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="工作城市">
              <el-input v-model="form.city" placeholder="城市" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="薪资下限">
              <el-input-number v-model="form.salary_min" :min="0" :step="1000" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="薪资上限">
              <el-input-number v-model="form.salary_max" :min="0" :step="1000" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="学历要求">
              <el-select v-model="form.education" placeholder="请选择" style="width: 100%">
                <el-option label="不限" value="不限" />
                <el-option label="大专" value="大专" />
                <el-option label="本科" value="本科" />
                <el-option label="硕士" value="硕士" />
                <el-option label="博士" value="博士" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="经验要求">
          <el-select v-model="form.experience" placeholder="请选择" style="width: 200px">
            <el-option label="不限" value="不限" />
            <el-option label="应届生" value="应届生" />
            <el-option label="1-3年" value="1-3年" />
            <el-option label="3-5年" value="3-5年" />
            <el-option label="5-10年" value="5-10年" />
            <el-option label="10年以上" value="10年以上" />
          </el-select>
        </el-form-item>
        <el-form-item label="职位描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="职位描述" />
        </el-form-item>
        <el-form-item label="任职要求">
          <el-input v-model="form.requirements" type="textarea" :rows="4" placeholder="任职要求" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '../api'

const router = useRouter()
const refreshStats = inject('refreshStats')

const jobs = ref([])
const applications = ref([])
const loading = ref(false)
const keyword = ref('')
const statusFilter = ref('')
const dialogVisible = ref(false)
const saving = ref(false)
const editingJob = ref(null)

const form = ref({
  title: '',
  company: '星辰科技',
  department: '',
  salary_min: 10000,
  salary_max: 20000,
  city: '',
  experience: '',
  education: '',
  description: '',
  requirements: ''
})

const filteredJobs = computed(() => {
  return jobs.value.filter(j => {
    if (keyword.value) {
      const kw = keyword.value.toLowerCase()
      if (!j.title.toLowerCase().includes(kw)) return false
    }
    if (statusFilter.value && j.status !== statusFilter.value) return false
    return true
  })
})

const fetchData = async () => {
  loading.value = true
  try {
    const [jobsData, appsData] = await Promise.all([
      api.getJobs(),
      api.getApplications()
    ])
    jobs.value = jobsData
    applications.value = appsData
  } finally {
    loading.value = false
  }
}

const formatSalary = (min, max) => {
  if (!min && !max) return '面议'
  return `${(min / 1000).toFixed(0)}K - ${(max / 1000).toFixed(0)}K`
}

const getApplyCount = (jobId) => {
  return applications.value.filter(a => a.job_id === jobId).length
}

const openCreateDialog = () => {
  editingJob.value = null
  resetForm()
  dialogVisible.value = true
}

const editJob = (row) => {
  editingJob.value = row
  form.value = { ...row }
  dialogVisible.value = true
}

const resetForm = () => {
  form.value = {
    title: '',
    company: '星辰科技',
    department: '',
    salary_min: 10000,
    salary_max: 20000,
    city: '',
    experience: '',
    education: '',
    description: '',
    requirements: ''
  }
}

const submitForm = async () => {
  if (!form.value.title) {
    ElMessage.warning('请输入职位名称')
    return
  }
  saving.value = true
  try {
    if (editingJob.value) {
      await api.updateJob(editingJob.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await api.createJob(form.value)
      ElMessage.success('发布成功')
    }
    dialogVisible.value = false
    fetchData()
    refreshStats()
  } finally {
    saving.value = false
  }
}

const toggleStatus = async (row) => {
  const newStatus = row.status === 'open' ? 'closed' : 'open'
  await api.updateJob(row.id, { status: newStatus })
  row.status = newStatus
  ElMessage.success(newStatus === 'open' ? '已开启招聘' : '已关闭招聘')
  refreshStats()
}

const deleteJob = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除职位「${row.title}」吗？`, '提示', { type: 'warning' })
    await api.deleteJob(row.id)
    ElMessage.success('删除成功')
    fetchData()
    refreshStats()
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

const viewJob = (id) => {
  router.push(`/jobs/${id}`)
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

.salary {
  color: #f56c6c;
  font-weight: 600;
}
</style>
