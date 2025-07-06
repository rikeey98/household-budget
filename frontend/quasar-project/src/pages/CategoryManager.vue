<template>
  <div class="q-pa-md">
    <div class="q-mb-md row items-center justify-between">
      <h2>카테고리 관리</h2>
      <div>
        <template v-if="auth.isAuthenticated">
          <span class="q-mr-sm">{{ auth.user?.username || auth.user?.email }} 님 로그인됨</span>
          <q-btn flat size="sm" color="primary" label="로그아웃" @click="handleLogout" />
        </template>
        <template v-else>
          <span class="q-mr-sm">로그인 필요</span>
          <q-btn flat size="sm" color="primary" label="로그인" @click="goToLogin" />
        </template>
      </div>
    </div>
    <q-btn label="카테고리 추가" color="primary" @click="onAdd(null)" class="q-mb-md" />
    <div v-if="categories.length === 0">
      <!-- 카테고리가 없을 때는 아무것도 표시하지 않음 (리스트 자체도 없음) -->
    </div>
    <template v-else>
      <ul>
        <li v-for="cat in filteredCategories" :key="cat.id" class="q-mb-sm">
          {{ cat.name }}
          <q-btn flat size="sm" color="primary" label="수정" @click="onEdit(cat)" />
          <q-btn flat size="sm" color="negative" label="삭제" @click="onDelete(cat)" />
        </li>
      </ul>
    </template>
    <!-- 카테고리 추가 다이얼로그 -->
    <q-dialog v-model="showDialog" persistent>
      <q-card style="min-width:300px;">
        <q-card-section>
          <div class="text-h6">
            {{ dialogMode === 'add' ? '카테고리 추가' : '카테고리 수정' }}
          </div>
        </q-card-section>
        <q-card-section>
          <q-input v-model="newCategoryName" label="카테고리 이름" autofocus @keyup.enter="dialogMode === 'add' ? handleAddCategory() : handleEditCategory()" />
          <q-select
            v-model="newCategoryType"
            :options="categoryTypeOptions"
            label="카테고리 타입"
            class="q-mt-md"
            emit-value map-options
          />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="취소" color="primary" v-close-popup :disable="loading.value" />
          <q-btn
            flat
            label="저장"
            color="primary"
            :loading="loading.value"
            @click="dialogMode === 'add' ? handleAddCategory() : handleEditCategory()"
            :disable="!newCategoryName.trim()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">카테고리 삭제</div>
          <div>정말로 "{{ selectedCategory?.name }}" 카테고리를 삭제하시겠습니까?</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="취소" color="primary" v-close-popup :disable="loading.value" />
          <q-btn flat label="삭제" color="negative" :loading="loading.value" @click="handleDeleteCategory" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from 'src/stores/auth'
import { useRouter } from 'vue-router'
import { api, fetchCSRFToken } from 'src/services/api'

const auth = useAuthStore()
const router = useRouter()

const categories = ref([])
const showDialog = ref(false)
const dialogMode = ref('add') // 'add' | 'edit' | 'delete'
const selectedCategory = ref(null)
const newCategoryName = ref('')
const newCategoryType = ref('expense')
const categoryTypeOptions = [
  { label: '지출', value: 'expense' },
  { label: '수입', value: 'income' }
]
const showDeleteDialog = ref(false)
const loading = ref(false)

const filteredCategories = computed(() =>
  Array.isArray(categories.value)
    ? categories.value.filter(cat => !!cat.name)
    : []
)

onMounted(async () => {
  await fetchCategories()
})

async function fetchCategories() {
  try {
    const res = await api.get('categories/')
    categories.value = Array.isArray(res.data) ? res.data : []
  } catch {
    categories.value = []
  }
}

function onAdd(cat) {
  dialogMode.value = 'add'
  selectedCategory.value = cat
  newCategoryName.value = ''
  newCategoryType.value = 'expense'
  showDialog.value = true
}

async function handleAddCategory() {
  if (!newCategoryName.value.trim()) return
  try {
    const csrfToken = await fetchCSRFToken()
    console.log('[카테고리 추가] 요청 데이터:', { name: newCategoryName.value, category_type: newCategoryType.value })
    console.log('[카테고리 추가] CSRF 토큰:', csrfToken)
    const res = await api.post(
      'categories/',
      { name: newCategoryName.value, category_type: newCategoryType.value },
      { headers: { 'X-CSRFToken': csrfToken } }
    )
    console.log('[카테고리 추가] 응답:', res)
    await fetchCategories()
    showDialog.value = false
  } catch (e) {
    alert('카테고리 추가 실패')
    if (e.response) {
      console.error('[카테고리 추가] 서버 응답 에러:', e.response.data, e.response.status)
    } else {
      console.error('[카테고리 추가] 네트워크/기타 에러:', e)
    }
  }
}

function onEdit(cat) {
  dialogMode.value = 'edit'
  selectedCategory.value = cat
  newCategoryName.value = cat.name
  newCategoryType.value = cat.category_type
  showDialog.value = true
}

function onDelete(cat) {
  dialogMode.value = 'delete'
  selectedCategory.value = cat
  showDeleteDialog.value = true
}

function handleLogout() {
  auth.logoutAction()
}

function goToLogin() {
  router.push('/login')
}

async function handleEditCategory() {
  if (!newCategoryName.value.trim() || !selectedCategory.value) return
  loading.value = true
  try {
    const csrfToken = await fetchCSRFToken()
    console.log('[카테고리 수정] 요청 데이터:', { name: newCategoryName.value, category_type: newCategoryType.value })
    const res = await api.put(
      `categories/${selectedCategory.value.id}/`,
      { name: newCategoryName.value, category_type: newCategoryType.value },
      { headers: { 'X-CSRFToken': csrfToken } }
    )
    console.log('[카테고리 수정] 응답:', res)
    await fetchCategories()
    showDialog.value = false
  } catch (e) {
    alert('카테고리 수정 실패')
    if (e.response) {
      console.error('[카테고리 수정] 서버 응답 에러:', e.response.data, e.response.status)
    } else {
      console.error('[카테고리 수정] 네트워크/기타 에러:', e)
    }
  } finally {
    loading.value = false
  }
}

async function handleDeleteCategory() {
  if (!selectedCategory.value) return
  loading.value = true
  try {
    const csrfToken = await fetchCSRFToken()
    console.log('[카테고리 삭제] 요청 id:', selectedCategory.value.id)
    const res = await api.delete(
      `categories/${selectedCategory.value.id}/`,
      { headers: { 'X-CSRFToken': csrfToken } }
    )
    console.log('[카테고리 삭제] 응답:', res)
    await fetchCategories()
    showDeleteDialog.value = false
  } catch (e) {
    alert('카테고리 삭제 실패')
    if (e.response) {
      console.error('[카테고리 삭제] 서버 응답 에러:', e.response.data, e.response.status)
    } else {
      console.error('[카테고리 삭제] 네트워크/기타 에러:', e)
    }
  } finally {
    loading.value = false
  }
}
</script> 