<template>
  <q-page padding>
    <div class="q-pa-md">
      <q-card class="q-mb-md">
        <q-card-section class="bg-primary text-white">
          <h5 class="q-ma-none">🎉 내가 만든 가계부 앱!</h5>
        </q-card-section>
        
        <q-card-section>
          <q-list bordered>
            <q-item>
              <q-item-section>
                <q-item-label>현재 환경: {{ config.getEnvironment() }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label>앱 제목: {{ config.app.title }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label>API URL: {{ config.api.baseURL }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label>디버그: {{ config.app.debug ? 'ON' : 'OFF' }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label>로그 레벨: {{ config.app.logLevel }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label>🎯 학습 진도: Vue.js 기초 학습중!</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <q-card class="q-mb-md">
        <q-card-section>
          <q-btn @click="testApi" label="API 테스트" color="primary" />
          <div v-if="response" class="q-mt-md">
            <pre>{{ response }}</pre>
          </div>
        </q-card-section>
      </q-card>

      <q-card>
        <q-card-section>
          <h6>환경별 실행 명령어:</h6>
          <p><code>npm run dev</code> → .env 사용</p>
          <p><code>npm run dev:staging</code> → .env.staging 사용</p>
          <p><code>npm run build:production</code> → .env.production 사용</p>
        </q-card-section>
      </q-card>

      <!-- 간단한 가계부 기능 추가 -->
      <q-card class="q-mt-md">
        <q-card-section class="bg-green-1">
          <h6>💰 간단 가계부 체험</h6>
        </q-card-section>
        <q-card-section>
          <div class="q-gutter-md">
            <q-input 
              v-model="expense.name" 
              label="지출 항목" 
              placeholder="예: 점심값"
            />
            <q-input 
              v-model.number="expense.amount" 
              label="금액" 
              type="number"
              placeholder="예: 8000"
            />
            <q-btn 
              @click="addExpense" 
              label="추가하기" 
              color="green"
              :disable="!expense.name || !expense.amount"
            />
          </div>
          
          <div v-if="expenses.length > 0" class="q-mt-md">
            <h6>📋 지출 목록:</h6>
            <q-list bordered>
              <q-item v-for="(item, index) in expenses" :key="index">
                <q-item-section>
                  <q-item-label>{{ item.name }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label>{{ item.amount.toLocaleString() }}원</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
            <div class="q-mt-md text-h6 text-center">
              💸 총 지출: {{ totalExpense.toLocaleString() }}원
            </div>
          </div>
        </q-card-section>
      </q-card>

      <div v-if="auth.isAuthenticated">
        <p>로그인: {{ auth.user.username }} ({{ auth.user.email }})</p>
        <q-btn label="로그아웃" color="negative" @click="handleLogout" :loading="auth.loading" />
      </div>
      <div v-else>
        <p>로그인하지 않았습니다.</p>
        <q-btn label="로그인" color="primary" @click="goToLogin" />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import config from '../config'
import apiService from '../services/api'
import { useAuthStore } from 'src/stores/auth'
import { useRouter } from 'vue-router'
// 환경 설정 데모 실행
import '../demo/env-demo.js'

const response = ref(null)
const auth = useAuthStore()
const router = useRouter()

// 간단한 가계부 기능을 위한 데이터
const expense = ref({
  name: '',
  amount: 0
})

const expenses = ref([])

// 총 지출 계산 (자동 계산)
const totalExpense = ref(0)

// expenses가 변경될 때마다 총합 다시 계산
const updateTotal = () => {
  totalExpense.value = expenses.value.reduce((sum, item) => sum + item.amount, 0)
}

const testApi = async () => {
  try {
    const data = await apiService.get(config.api.endpoints.test)
    response.value = JSON.stringify(data, null, 2)
  } catch (error) {
    response.value = `Error: ${error.message}`
  }
}

// 지출 추가 함수
const addExpense = () => {
  if (expense.value.name && expense.value.amount > 0) {
    expenses.value.push({
      name: expense.value.name,
      amount: expense.value.amount,
      date: new Date().toLocaleDateString()
    })
    
    // 총합 업데이트
    updateTotal()
    
    // 입력 필드 초기화
    expense.value.name = ''
    expense.value.amount = 0
    
    console.log('✅ 지출 추가됨:', expenses.value)
  }
}

function goToLogin() {
  router.push('/login')
}

function handleLogout() {
  auth.logoutAction()
}

onMounted(() => {
  auth.fetchUser()
})
</script>
