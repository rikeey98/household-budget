<template>
  <q-page class="q-pa-md">
    <!-- 필터 바 -->
    <div class="row q-gutter-md items-center q-mb-md">
      <!-- 기간(날짜 범위) -->
      <q-input
        filled
        :model-value="dateRangeDisplay"
        label="기간"
        readonly
        style="width: 200px"
      >
        <template v-slot:append>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy 
              cover 
              transition-show="scale" 
              transition-hide="scale"
              v-model="showDatePicker"
            >
              <q-date
                v-model="filters.dateRange"
                range
                mask="YYYY-MM-DD"
                @update:model-value="showDatePicker = false"
              />
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
      <!-- 카테고리 -->
      <q-select
        filled
        v-model="filters.category"
        :options="categoryFilterOptions"
        label="카테고리"
        emit-value
        map-options
        style="width: 150px"
      />
      <!-- 거래 타입 -->
      <q-select
        filled
        v-model="filters.type"
        :options="typeFilterOptions"
        label="거래 타입"
        emit-value
        map-options
        style="width: 120px"
      />
      <!-- 결제수단 -->
      <q-select
        filled
        v-model="filters.paymentMethod"
        :options="paymentFilterOptions"
        label="결제수단"
        emit-value
        map-options
        style="width: 120px"
      />
      <!-- 금액 범위 -->
      <q-input filled v-model.number="filters.minAmount" label="최소금액" type="number" style="width: 100px" />
      <q-input filled v-model.number="filters.maxAmount" label="최대금액" type="number" style="width: 100px" />
      <!-- 검색어 -->
      <q-input filled v-model="filters.keyword" label="검색어" style="width: 150px" />
      <!-- 적용 버튼 -->
      <q-btn color="primary" label="적용" @click="fetchTransactions" />
    </div>
    <div class="row items-center q-mb-md">
      <div class="text-h5 text-bold">거래 내역 관리</div>
      <q-space />
      <q-btn color="primary" icon="add" label="거래 추가" @click="openAddDialog" />
    </div>
    <q-table
      :rows="transactions"
      :columns="columns"
      row-key="id"
      flat bordered
      :loading="loading"
      v-model:pagination="pagination"
      :rows-per-page-options="[10, 20, 50]"
      class="q-mb-lg"
    >
      <template v-slot:body-cell-actions="props">
        <q-td align="center">
          <q-btn dense flat icon="edit" color="primary" @click="openEditDialog(props.row)" />
          <q-btn dense flat icon="delete" color="negative" @click="openDeleteDialog(props.row)" />
        </q-td>
      </template>
    </q-table>

    <!-- 거래 추가/수정 다이얼로그 -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width:350px;max-width:95vw;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">{{ dialogMode === 'add' ? '거래 추가' : '거래 수정' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-form @submit.prevent="handleSave">
          <q-card-section>
            <q-select
              v-model="form.transaction_type"
              :options="transactionTypeOptions"
              label="거래 타입"
              dense outlined emit-value map-options
              class="q-mb-md"
              :disable="dialogMode === 'edit'"
              required
            />
            <q-select
              v-model="form.category"
              :options="categoryOptions"
              option-value="id"
              option-label="name"
              label="카테고리"
              dense outlined emit-value map-options
              class="q-mb-md"
              required
            />
            <q-input v-model.number="form.amount" label="금액" type="number" dense outlined required class="q-mb-md" min="1" />
            <q-input v-model="form.description" label="설명" dense outlined class="q-mb-md" />
            <q-select
              v-model="form.payment_method"
              :options="paymentMethodOptions"
              label="결제수단"
              dense outlined emit-value map-options
              class="q-mb-md"
              required
            />
            <q-input v-model="form.date" label="거래일" dense outlined required class="q-mb-md">
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="form.date" mask="YYYY-MM-DD" />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="취소" v-close-popup :disable="loading" />
            <q-btn color="primary" label="저장" type="submit" :loading="loading" />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <!-- 삭제 확인 다이얼로그 -->
    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section class="text-h6">거래 삭제</q-card-section>
        <q-card-section>정말로 이 거래를 삭제하시겠습니까?</q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="취소" v-close-popup :disable="loading" />
          <q-btn flat color="negative" label="삭제" @click="handleDelete" :loading="loading" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { api, postWithCSRF, deleteWithCSRF } from 'src/services/api'

const $q = useQuasar()
const loading = ref(false)
const transactions = ref([])
const categories = ref([])
const showDialog = ref(false)
const showDeleteDialog = ref(false)
const dialogMode = ref('add') // 'add' | 'edit'
const selectedRow = ref(null)
const pagination = ref({ page: 1, rowsPerPage: 10 })

const form = ref({
  transaction_type: '',
  category: null,
  amount: '',
  description: '',
  payment_method: '',
  date: '',
})

const filters = ref({
  dateRange: null, // {from, to} or null
  category: null,       // 카테고리 id
  type: '',             // 'expense'/'income'/''
  paymentMethod: '',    // 'card'/'cash'/'account'/''
  minAmount: null,
  maxAmount: null,
  keyword: ''
})

const dateRangeDisplay = computed({
  get() {
    if (!filters.value.dateRange) return ''
    if (typeof filters.value.dateRange === 'string') return filters.value.dateRange
    if (filters.value.dateRange.from && filters.value.dateRange.to)
      return `${filters.value.dateRange.from} ~ ${filters.value.dateRange.to}`
    if (filters.value.dateRange.from)
      return filters.value.dateRange.from
    return ''
  },
  set() {
    // 사용자가 직접 입력하는 경우는 없으므로 무시
  }
})
const showDatePicker = ref(false)

const columns = [
  { name: 'date', label: '날짜', field: 'date', align: 'left', sortable: true },
  { name: 'transaction_type', label: '타입', field: 'transaction_type', align: 'left', sortable: true },
  { name: 'category', label: '카테고리', field: row => row.category_name, align: 'left' },
  { name: 'amount', label: '금액', field: 'amount', align: 'right', sortable: true },
  { name: 'payment_method', label: '결제수단', field: 'payment_method', align: 'left' },
  { name: 'description', label: '설명', field: 'description', align: 'left' },
  { name: 'actions', label: '액션', field: 'actions', align: 'center' },
]

const transactionTypeOptions = [
  { label: '지출', value: 'expense' },
  { label: '수입', value: 'income' },
]
const paymentMethodOptions = [
  { label: '현금', value: 'cash' },
  { label: '카드', value: 'card' },
  { label: '계좌이체', value: 'account' },
]

const categoryOptions = computed(() => {
  if (!form.value.transaction_type) return []
  return categories.value.filter(cat => cat.category_type === form.value.transaction_type)
})

const categoryFilterOptions = computed(() => [
  { label: '전체', value: null },
  ...categories.value.map(cat => ({ label: cat.name, value: cat.id }))
])
const typeFilterOptions = [
  { label: '전체', value: '' },
  { label: '지출', value: 'expense' },
  { label: '수입', value: 'income' }
]
const paymentFilterOptions = [
  { label: '전체', value: '' },
  { label: '카드', value: 'card' },
  { label: '현금', value: 'cash' },
  { label: '계좌이체', value: 'account' }
]

onMounted(async () => {
  await fetchCategories()
  await fetchTransactions()
})

async function fetchCategories() {
  try {
    const res = await api.get('categories/')
    categories.value = Array.isArray(res.data) ? res.data : []
  } catch {
    categories.value = []
  }
}

async function fetchTransactions() {
  loading.value = true
  try {
    const params = {}
    // 날짜 범위 파싱
    if (filters.value.dateRange) {
      let start, end
      if (typeof filters.value.dateRange === 'string' && filters.value.dateRange.includes('~')) {
        [start, end] = filters.value.dateRange.split('~').map(s => s.trim())
      } else if (typeof filters.value.dateRange === 'object' && filters.value.dateRange.from && filters.value.dateRange.to) {
        start = filters.value.dateRange.from
        end = filters.value.dateRange.to
      }
      if (start) params.start_date = start
      if (end) params.end_date = end
    }
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.type) params.type = filters.value.type
    if (filters.value.paymentMethod) params.payment_method = filters.value.paymentMethod
    if (filters.value.minAmount) params.min_amount = filters.value.minAmount
    if (filters.value.maxAmount) params.max_amount = filters.value.maxAmount
    if (filters.value.keyword) params.description = filters.value.keyword

    const res = await api.get('transactions/transactions/', { params })
    transactions.value = (Array.isArray(res.data) ? res.data : []).map(row => ({
      ...row,
      category_name: getCategoryName(row.category)
    }))
  } catch {
    transactions.value = []
  } finally {
    loading.value = false
  }
}

function getCategoryName(categoryId) {
  const cat = categories.value.find(c => c.id === categoryId)
  return cat ? cat.name : ''
}

function openAddDialog() {
  dialogMode.value = 'add'
  Object.assign(form.value, {
    transaction_type: 'expense', // 디폴트값을 '지출'로 설정
    category: null,
    amount: '',
    description: '',
    payment_method: '',
    date: '',
  })
  showDialog.value = true
}

function openEditDialog(row) {
  dialogMode.value = 'edit'
  selectedRow.value = row
  Object.assign(form.value, {
    transaction_type: row.transaction_type,
    category: row.category,
    amount: row.amount,
    description: row.description,
    payment_method: row.payment_method,
    date: row.date,
  })
  showDialog.value = true
}

function openDeleteDialog(row) {
  selectedRow.value = row
  showDeleteDialog.value = true
}

// PUT 요청용 CSRF 헬퍼 (임시)
async function putWithCSRF(url, data, config = {}) {
  const csrfToken = await api.get('accounts/auth/csrf/').then(res => res.data.csrfToken)
  return api.put(url, data, {
    ...config,
    headers: {
      ...(config.headers || {}),
      'X-CSRFToken': csrfToken,
    },
  })
}

async function handleSave() {
  // 필수값 및 타입 검증
  if (!form.value.transaction_type) return $q.notify({ type: 'negative', message: '거래 타입을 선택하세요.' })
  if (!form.value.category) return $q.notify({ type: 'negative', message: '카테고리를 선택하세요.' })
  if (!form.value.amount || isNaN(Number(form.value.amount)) || Number(form.value.amount) <= 0) return $q.notify({ type: 'negative', message: '금액을 올바르게 입력하세요.' })
  if (!form.value.payment_method) return $q.notify({ type: 'negative', message: '결제수단을 선택하세요.' })
  if (!form.value.date) return $q.notify({ type: 'negative', message: '거래일을 입력하세요.' })

  // 데이터 타입 변환
  const payload = {
    transaction_type: form.value.transaction_type,
    category: typeof form.value.category === 'object' ? form.value.category.id : Number(form.value.category),
    amount: Number(form.value.amount),
    description: form.value.description || '',
    payment_method: form.value.payment_method,
    date: form.value.date
  }
  loading.value = true
  try {
    if (dialogMode.value === 'add') {
      await postWithCSRF('transactions/transactions/', payload)
      $q.notify({ type: 'positive', message: '거래가 추가되었습니다.' })
    } else if (dialogMode.value === 'edit' && selectedRow.value) {
      await putWithCSRF(`transactions/transactions/${selectedRow.value.id}/`, payload)
      $q.notify({ type: 'positive', message: '거래가 수정되었습니다.' })
    }
    await fetchTransactions()
    showDialog.value = false
  } catch {
    $q.notify({ type: 'negative', message: '저장 실패' })
  } finally {
    loading.value = false
  }
}

async function handleDelete() {
  loading.value = true
  try {
    if (selectedRow.value) {
      await deleteWithCSRF(`transactions/transactions/${selectedRow.value.id}/`)
      $q.notify({ type: 'positive', message: '거래가 삭제되었습니다.' })
      await fetchTransactions()
    }
    showDeleteDialog.value = false
  } catch {
    $q.notify({ type: 'negative', message: '삭제 실패' })
  } finally {
    loading.value = false
  }
}
</script> 