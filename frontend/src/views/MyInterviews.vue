<template>
  <div class="my-interviews-page">
    <div class="page-header">
      <h2>我的面试</h2>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" @submit.prevent>
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
        <el-table-column prop="job_title" label="应聘职位" width="180" />
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
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!loading && interviews.length === 0" description="暂无面试安排" />
    </el-card>

    <el-drawer v-model="detailVisible" title="面试详情" size="480px">
      <div v-if="detailData" class="detail-content">
        <div class="detail-header">
          <h3>{{ detailData.job_title }}</h3>
          <el-tag :type="INTERVIEW_STATUS_TYPE[detailData.status]">
            {{ INTERVIEW_STATUS_TEXT[detailData.status] }}
          </el-tag>
        </div>
        <el-descriptions :column="1" border>
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
        </el-descriptions>
        <div class="detail-tip" v-if="detailData.status === 'scheduled'">
          <el-icon><InfoFilled /></el-icon>
          <span>如有调整请联系 HR，联系方式可查看投递详情中的沟通记录</span>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'
import { api, INTERVIEW_STATUS_TEXT, INTERVIEW_STATUS_TYPE, INTERVIEW_WAY_TEXT } from '../api'

const loading = ref(false)
const interviews = ref([])
const filters = reactive({
  status: '',
  start_date: '',
  end_date: ''
})
const dateRange = ref([])

const detailVisible = ref(false)
const detailData = ref(null)

const fetchList = async () => {
  loading.value = true
  try {
    const params = {
      status: filters.status || undefined,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined
    }
    const all = await api.getInterviews(params)
    interviews.value = all
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
  filters.status = ''
  filters.start_date = ''
  filters.end_date = ''
  dateRange.value = []
  fetchList()
}

const viewDetail = (row) => {
  detailData.value = row
  detailVisible.value = true
}

onMounted(() => {
  fetchList()
})
</script>

<style scoped>
.my-interviews-page {
  padding: 20px;
}

.page-header {
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

.detail-tip {
  margin-top: 20px;
  padding: 12px 16px;
  background: #ecf5ff;
  border-radius: 8px;
  color: #409eff;
  font-size: 13px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  line-height: 1.5;
}
</style>
