<template>
  <div class="my-offers-page">
    <div class="page-header">
      <h2>我的 Offer</h2>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" @submit.prevent>
        <el-form-item label="状态">
          <el-radio-group v-model="filters.status" @change="fetchList">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="sent">待处理</el-radio-button>
            <el-radio-button value="accepted">已接受</el-radio-button>
            <el-radio-button value="rejected">已拒绝</el-radio-button>
            <el-radio-button value="withdrawn">已撤回</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="list-card">
      <el-table :data="offers" v-loading="loading" stripe>
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
        <el-table-column prop="sent_at" label="发送时间" width="170" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDetail(row)">查看详情</el-button>
            <el-button link type="success" @click="handleAccept(row)" v-if="row.status === 'sent'">
              接受
            </el-button>
            <el-button link type="danger" @click="handleReject(row)" v-if="row.status === 'sent'">
              拒绝
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!loading && offers.length === 0" description="暂无 Offer 记录" />
    </el-card>

    <el-drawer v-model="detailVisible" title="Offer 详情" size="500px">
      <div v-if="currentOffer" class="offer-detail">
        <el-alert v-if="currentOffer.status === 'sent'" type="primary" :closable="false" style="margin-bottom: 20px">
          您有一份待处理的 Offer，请及时回复。如有疑问请联系 HR。
        </el-alert>
        <div class="detail-section">
          <h4>Offer 信息</h4>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="岗位">{{ currentOffer.position }}</el-descriptions-item>
            <el-descriptions-item label="应聘职位">{{ currentOffer.job_title }}</el-descriptions-item>
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
          <h4>备注说明</h4>
          <p>{{ currentOffer.remark }}</p>
        </div>
        <div class="detail-section">
          <h4>时间信息</h4>
          <el-descriptions :column="1" border>
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
        <div class="detail-actions" v-if="currentOffer.status === 'sent'">
          <el-button type="success" @click="handleAccept(currentOffer)" size="large">
            接受 Offer
          </el-button>
          <el-button type="danger" @click="handleReject(currentOffer)" size="large">
            拒绝 Offer
          </el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api, OFFER_STATUS_TEXT, OFFER_STATUS_TYPE } from '../api'

const { refreshStats } = inject('appActions', { refreshStats: () => {} })

const loading = ref(false)
const offers = ref([])

const filters = reactive({
  status: ''
})

const detailVisible = ref(false)
const currentOffer = ref(null)
const currentCandidateName = inject('currentCandidateName')

const fetchList = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.status) params.status = filters.status
    const allOffers = await api.getOffers(params)
    offers.value = allOffers.filter(o => o.candidate_name === currentCandidateName.value && o.status !== 'draft')
  } catch (e) {}
  loading.value = false
}

const resetFilters = () => {
  filters.status = ''
  fetchList()
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

const handleAccept = async (row) => {
  try {
    await ElMessageBox.confirm(
      '确认接受该 Offer？接受后请按时入职，如有特殊情况请联系 HR。',
      '接受 Offer',
      { type: 'success' }
    )
    await api.acceptOffer(row.id)
    ElMessage.success('已接受 Offer')
    detailVisible.value = false
    fetchList()
    refreshStats()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message || '操作失败')
  }
}

const handleReject = async (row) => {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      '请输入拒绝原因',
      '拒绝 Offer',
      {
        confirmButtonText: '确认拒绝',
        cancelButtonText: '取消',
        inputType: 'textarea',
        inputPlaceholder: '请输入拒绝原因',
        inputValidator: (val) => {
          if (!val || !val.trim()) {
            return '请输入拒绝原因'
          }
          return true
        }
      }
    )
    await api.rejectOffer(row.id, reason)
    ElMessage.success('已拒绝 Offer')
    detailVisible.value = false
    fetchList()
    refreshStats()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message || '操作失败')
  }
}

onMounted(() => {
  fetchList()
})
</script>

<style scoped>
.my-offers-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.filter-card {
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
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
  display: flex;
  gap: 16px;
  margin-top: 24px;
}

.detail-actions .el-button {
  flex: 1;
}
</style>
