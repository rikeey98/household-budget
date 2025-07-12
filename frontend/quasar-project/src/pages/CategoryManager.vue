<template>
  <div class="layout">
    <!-- 좌측 카테고리 목록 -->
    <div class="category-list">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">카테고리 설정</h1>
      </div>
      <div class="tabs mb-6">
        <button class="tab" :class="{ active: tab === 'expense' }" @click="tab = 'expense'">지출</button>
        <button class="tab" :class="{ active: tab === 'income' }" @click="tab = 'income'">수입</button>
      </div>
      <div class="category-items">
        <CategoryTree :categories="filteredCategoryTree" @add="onAdd" @edit="onEdit" @delete="onDelete" />
      </div>
      <div class="add-category">
        <button class="add-button" @click="onAdd(null)">
          <i class="q-icon notranslate material-icons" aria-hidden="true">add</i>
          <span>새 카테고리 추가</span>
        </button>
      </div>
    </div>
    <!-- 상세 패널 오버레이 -->
    <div class="detail-overlay" :class="{ active: showPanel }" @click="closePanel" />
    <!-- 상세 패널 (오른쪽 고정, 슬라이드 인/아웃) -->
    <div class="detail-panel" :class="{ active: showPanel }">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold">{{ dialogMode === 'add' ? '새 카테고리 추가' : '카테고리 수정' }}</h2>
        <button @click="closePanel">
          <i class="q-icon notranslate material-icons" aria-hidden="true">close</i>
        </button>
      </div>
      <div class="form-group">
        <label class="form-label">아이콘 선택</label>
        <div class="emoji-picker">
          <div v-for="emoji in emojis" :key="emoji" class="emoji-item" :class="{ selected: selectedEmoji === emoji }" @click="selectedEmoji = emoji">{{ emoji }}</div>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">이름</label>
        <input type="text" class="form-input" v-model="newCategoryName" />
      </div>
      <div class="form-group">
        <label class="form-label">설명</label>
        <input type="text" class="form-input" v-model="newCategoryDesc" />
      </div>
      <div class="form-group">
        <label class="form-label">상위 카테고리</label>
        <select class="form-input" v-model="newCategoryParent">
          <option :value="null">없음</option>
          <option v-for="cat in parentCategoryOptions" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">예산 설정</label>
        <div class="space-y-2">
          <label class="flex items-center gap-2">
            <input type="radio" name="budget" value="none" v-model="budgetOption" />
            <span>예산 제외</span>
          </label>
          <label class="flex items-center gap-2">
            <input type="radio" name="budget" value="monthly" v-model="budgetOption" />
            <span>월 예산 설정</span>
          </label>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">알림 설정</label>
        <div class="space-y-2">
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="notifyOnTransaction" />
            <span>새 거래 발생시 알림</span>
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="notifyOnBudgetExceed" />
            <span>예산 초과시 알림</span>
          </label>
        </div>
      </div>
      <div class="flex gap-3 mt-8">
        <button class="bg-primary text-white px-6 py-2 rounded-lg flex-1" :disabled="loading" @click="handleSaveCategory">
          <span v-if="loading">저장중...</span>
          <span v-else>저장</span>
        </button>
        <button class="border border-gray-300 px-6 py-2 rounded-lg" :disabled="loading" @click="closePanel">
          취소
        </button>
        <button v-if="dialogMode === 'edit'" class="border border-red-400 text-red-600 px-6 py-2 rounded-lg" :disabled="loading" @click="onDelete(selectedCategory)">
          삭제
        </button>
      </div>
    </div>
    <!-- 삭제 확인 다이얼로그 -->
    <div v-if="showDeleteDialog" class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-30">
      <div class="bg-white rounded-lg p-6 shadow-lg">
        <div class="mb-4 text-lg font-semibold">카테고리 삭제</div>
        <div class="mb-6">정말로 "{{ selectedCategory?.name }}" 카테고리를 삭제하시겠습니까?</div>
        <div class="flex gap-3 justify-end">
          <button class="border border-gray-300 px-6 py-2 rounded-lg" :disabled="loading" @click="showDeleteDialog = false">취소</button>
          <button class="bg-red-500 text-white px-6 py-2 rounded-lg" :disabled="loading" @click="handleDeleteCategory">
            <span v-if="loading">삭제중...</span>
            <span v-else>삭제</span>
          </button>
        </div>
      </div>
    </div>
    <!-- 토스트 메시지 -->
    <div v-if="toastMessage" class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white px-4 py-2 rounded-lg">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import CategoryTree from 'components/CategoryTree.vue'
import { api, fetchCSRFToken } from 'src/services/api'

const categories = ref([])
const tab = ref('expense')
const showPanel = ref(false)
const dialogMode = ref('add')
const selectedCategory = ref(null)
const newCategoryName = ref('')
const newCategoryDesc = ref('')
const newCategoryParent = ref(null)
const selectedEmoji = ref('🎨')
const emojis = ['🎨', '💰', '🏠', '🎮', '🍔', '🚗', '✨', '📱']
const budgetOption = ref('none')
const notifyOnTransaction = ref(false)
const notifyOnBudgetExceed = ref(false)
const toastMessage = ref('')
const loading = ref(false)
const showDeleteDialog = ref(false)

const parentCategoryOptions = computed(() =>
  categories.value.filter(cat => !cat.parent && cat.category_type === tab.value)
)
const filteredCategoryTree = computed(() => {
  // 트리 구조 변환 및 탭 필터링
  const map = {}
  const roots = []
  categories.value.forEach(cat => {
    if (cat.category_type !== tab.value) return
    map[cat.id] = { ...cat, children: [] }
  })
  categories.value.forEach(cat => {
    if (cat.category_type !== tab.value) return
    if (cat.parent && map[cat.parent]) {
      map[cat.parent].children.push(map[cat.id])
    } else if (map[cat.id]) {
      roots.push(map[cat.id])
    }
  })
  return roots
})

onMounted(fetchCategories)

async function fetchCategories() {
  try {
    const res = await api.get('categories/')
    categories.value = Array.isArray(res.data) ? res.data : []
  } catch {
    categories.value = []
  }
}

function onAdd(parentCat) {
  dialogMode.value = 'add'
  selectedCategory.value = null
  newCategoryName.value = ''
  newCategoryDesc.value = ''
  newCategoryParent.value = parentCat ? parentCat.id : null
  selectedEmoji.value = '🎨'
  budgetOption.value = 'none'
  notifyOnTransaction.value = false
  notifyOnBudgetExceed.value = false
  showPanel.value = true
}

function onEdit(cat) {
  dialogMode.value = 'edit'
  selectedCategory.value = cat
  newCategoryName.value = cat.name
  newCategoryDesc.value = cat.desc || ''
  newCategoryParent.value = cat.parent || null
  selectedEmoji.value = cat.emoji || '🎨'
  budgetOption.value = cat.budget_option || 'none'
  notifyOnTransaction.value = !!cat.notify_on_transaction
  notifyOnBudgetExceed.value = !!cat.notify_on_budget_exceed
  showPanel.value = true
}

function onDelete(cat) {
  selectedCategory.value = cat
  showDeleteDialog.value = true
}

function closePanel() {
  showPanel.value = false
}

async function handleSaveCategory() {
  if (!newCategoryName.value.trim()) return
  loading.value = true
  try {
    const csrfToken = await fetchCSRFToken()
    const payload = {
      name: newCategoryName.value,
      desc: newCategoryDesc.value,
      parent: newCategoryParent.value,
      emoji: selectedEmoji.value,
      budget_option: budgetOption.value,
      notify_on_transaction: notifyOnTransaction.value,
      notify_on_budget_exceed: notifyOnBudgetExceed.value,
      category_type: tab.value
    }
    if (dialogMode.value === 'add') {
      await api.post('categories/', payload, { headers: { 'X-CSRFToken': csrfToken } })
      showToast('카테고리가 저장되었습니다')
    } else if (dialogMode.value === 'edit' && selectedCategory.value) {
      await api.put(`categories/${selectedCategory.value.id}/`, payload, { headers: { 'X-CSRFToken': csrfToken } })
      showToast('카테고리가 수정되었습니다')
    }
    await fetchCategories()
    showPanel.value = false
  } catch (e) {
    showToast('저장 실패')
    if (e.response) {
      console.error('[카테고리 저장/수정] 서버 응답 에러:', e.response.data, e.response.status)
    } else {
      console.error('[카테고리 저장/수정] 네트워크/기타 에러:', e)
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
    await api.delete(`categories/${selectedCategory.value.id}/`, { headers: { 'X-CSRFToken': csrfToken } })
    await fetchCategories()
    showToast('카테고리가 삭제되었습니다')
    showDeleteDialog.value = false
    showPanel.value = false
  } catch (e) {
    showToast('삭제 실패')
    if (e.response) {
      console.error('[카테고리 삭제] 서버 응답 에러:', e.response.data, e.response.status)
    } else {
      console.error('[카테고리 삭제] 네트워크/기타 에러:', e)
    }
  } finally {
    loading.value = false
  }
}

function showToast(message) {
  toastMessage.value = message
  setTimeout(() => {
    toastMessage.value = ''
  }, 3000)
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}
</style> 