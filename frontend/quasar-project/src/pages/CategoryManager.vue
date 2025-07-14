<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="q-pa-md">
        <q-row class="q-col-gutter-xl" gutter="xl" wrap>
          <!-- 좌측: 카테고리 목록 및 탭 -->
          <q-col cols="12" md="5">
            <div class="q-mb-md">
              <div class="text-h5 text-bold">카테고리 설정</div>
            </div>
            <q-tabs v-model="tab" class="q-mb-md" dense align="left" active-color="primary" indicator-color="primary">
              <q-tab name="expense" label="지출" />
              <q-tab name="income" label="수입" />
            </q-tabs>
            <q-card flat bordered>
              <q-card-section>
                <CategoryTree :categories="filteredCategoryTree" @add="onAdd" @edit="onEdit" @delete="onDelete" />
              </q-card-section>
            </q-card>
            <div class="q-mt-md flex flex-center">
              <q-btn color="primary" icon="add" label="새 카테고리 추가" @click="onAdd(null)" class="full-width" />
            </div>
          </q-col>
          <!-- 삭제 확인 다이얼로그 -->
          <q-dialog v-model="showDeleteDialog">
            <q-card>
              <q-card-section class="text-h6">카테고리 삭제</q-card-section>
              <q-card-section>정말로 "{{ selectedCategory?.name }}" 카테고리를 삭제하시겠습니까?</q-card-section>
              <q-card-actions align="right">
                <q-btn flat label="취소" v-close-popup :disable="loading" />
                <q-btn flat color="negative" label="삭제" @click="handleDeleteCategory" :loading="loading" :disable="loading" v-close-popup />
              </q-card-actions>
            </q-card>
          </q-dialog>
        </q-row>
        <!-- q-drawer를 q-layout의 직계 자식으로 이동 -->
        <q-drawer v-model="showPanel" side="right" overlay bordered :width="400" :breakpoint="700" class="q-pa-md">
          <q-form @submit.prevent="handleSaveCategory">
            <div class="row items-center q-mb-md">
              <div class="text-h6">{{ dialogMode === 'add' ? '새 카테고리 추가' : '카테고리 수정' }}</div>
              <q-space />
              <q-btn icon="close" flat round dense @click="closePanel" />
            </div>
            <div class="q-mb-md">
              <div class="text-subtitle2 q-mb-xs">아이콘 선택</div>
              <q-row class="q-gutter-xs" wrap>
                <q-col v-for="emoji in emojis" :key="emoji" cols="3" sm="2" md="2">
                  <q-btn :label="emoji" flat round :color="selectedEmoji === emoji ? 'primary' : 'grey-4'" @click="selectedEmoji = emoji" class="full-width" />
                </q-col>
              </q-row>
            </div>
            <q-input v-model="newCategoryName" label="이름" dense outlined required class="q-mb-md" />
            <q-input v-model="newCategoryDesc" label="설명" dense outlined class="q-mb-md" />
            <q-select
              v-model="newCategoryParent"
              :options="parentCategoryOptions"
              option-value="id"
              option-label="name"
              label="상위 카테고리"
              dense outlined emit-value map-options
              class="q-mb-md"
              :clearable="true"
              :placeholder="'없음'"
            />
            <div class="q-mb-md">
              <div class="text-subtitle2 q-mb-xs">예산 설정</div>
              <q-option-group
                v-model="budgetOption"
                :options="budgetOptions"
                type="radio"
                inline
              />
            </div>
            <div class="q-mb-md">
              <div class="text-subtitle2 q-mb-xs">알림 설정</div>
              <q-checkbox v-model="notifyOnTransaction" label="새 거래 발생시 알림" />
              <q-checkbox v-model="notifyOnBudgetExceed" label="예산 초과시 알림" />
            </div>
            <q-row class="q-gutter-sm q-mt-lg">
              <q-col cols="12" sm="4">
                <q-btn type="submit" color="primary" label="저장" :loading="loading" class="full-width" />
              </q-col>
              <q-col cols="12" sm="4">
                <q-btn flat label="취소" @click="closePanel" class="full-width" :disable="loading" />
              </q-col>
              <q-col cols="12" sm="4" v-if="dialogMode === 'edit'">
                <q-btn flat color="negative" label="삭제" @click="showDeleteDialog = true" class="full-width" :disable="loading" />
              </q-col>
            </q-row>
          </q-form>
        </q-drawer>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import CategoryTree from 'components/CategoryTree.vue'
import { api, postWithCSRF, deleteWithCSRF } from 'src/services/api'
import { useQuasar } from 'quasar'

const categories = ref([])
const tab = ref('expense')
const showPanel = ref(false)
const dialogMode = ref('add')
const selectedCategory = ref(null)

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

function onAdd(parentCategory = null) {
  dialogMode.value = 'add'
  selectedCategory.value = null
  newCategoryName.value = ''
  newCategoryDesc.value = ''
  newCategoryParent.value = parentCategory?.id || null
  selectedEmoji.value = emojis[0]
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
  selectedEmoji.value = cat.emoji || emojis[0]
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

// script setup 내부에 아래 변수/로직 추가 및 복원
const newCategoryName = ref('')
const newCategoryDesc = ref('')
const newCategoryParent = ref(null)
const selectedEmoji = ref('🎨')
const emojis = ['🎨', '💰', '🏠', '🎮', '🍔', '🚗', '✨', '📱']
const budgetOption = ref('none')
const budgetOptions = [
  { label: '예산 제외', value: 'none' },
  { label: '월 예산 설정', value: 'monthly' }
]
const notifyOnTransaction = ref(false)
const notifyOnBudgetExceed = ref(false)
const loading = ref(false)
const showDeleteDialog = ref(false)

const parentCategoryOptions = computed(() =>
  categories.value.filter(cat => !cat.parent && cat.category_type === tab.value && (!selectedCategory.value || cat.id !== selectedCategory.value.id))
)

const $q = useQuasar()

// PUT 요청용 CSRF 헬퍼 (TransactionManager.vue와 동일)
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

async function handleSaveCategory() {
  console.log('$q:', $q)
  if (!newCategoryName.value.trim()) return $q.notify({ type: 'negative', message: '이름을 입력하세요.' })
  loading.value = true
  try {
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
      const res = await postWithCSRF('categories/', payload)
      $q.notify({ type: 'positive', message: '카테고리가 저장되었습니다.' })
      categories.value.push(res.data)
    } else if (dialogMode.value === 'edit' && selectedCategory.value) {
      await putWithCSRF(`categories/${selectedCategory.value.id}/`, payload)
      $q.notify({ type: 'positive', message: '카테고리가 수정되었습니다.' })
      await fetchCategories()
    }
    showPanel.value = false
  } catch {
    $q.notify({ type: 'negative', message: '저장 실패' })
  } finally {
    loading.value = false
  }
}

async function handleDeleteCategory() {
  if (!selectedCategory.value) return
  loading.value = true
  try {
    console.log('삭제 시도:', selectedCategory.value.id)
    await deleteWithCSRF(`categories/${selectedCategory.value.id}/`)
    await fetchCategories()
    $q.notify({ type: 'positive', message: '카테고리가 삭제되었습니다.' })
    showDeleteDialog.value = false
    showPanel.value = false
  } catch (err) {
    console.error('삭제 실패:', err)
    $q.notify({ type: 'negative', message: `삭제 실패: ${err?.response?.data?.detail || err.message || err}` })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}
</style> 