<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Quasar App
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>

        <q-space />

        <!-- 로그인/회원가입 또는 프로필 (Pinia 연동) -->
        <template v-if="!auth.isAuthenticated">
          <q-btn flat label="로그인" @click="goToLogin" />
          <q-btn flat label="회원가입" @click="goToRegister" />
        </template>
        <template v-else>
          <q-btn flat round dense icon="account_circle">
            <q-menu>
              <q-list style="min-width: 120px">
                <q-item>
                  <q-item-section>{{ auth.user?.username || '사용자' }}</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable @click="logout">
                  <q-item-section>로그아웃</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </template>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-1"
    >
      <div class="q-pa-md flex flex-center">
        <q-avatar size="42px" class="q-mr-sm" color="primary" text-color="white">
          <q-icon name="account_balance_wallet" size="28px" />
        </q-avatar>
        <div class="text-h6 text-primary">가계부</div>
      </div>
      <q-separator spaced />
      <q-list padding>
        <q-item clickable @click="goToHome" :active="isActive('/')" active-class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>홈</q-item-section>
        </q-item>
        <q-item clickable @click="goToTransactionManager" :active="isActive('/transaction-manager')" active-class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="receipt_long" />
          </q-item-section>
          <q-item-section>거래 관리</q-item-section>
        </q-item>
        <q-item clickable @click="goToCategoryManager" :active="isActive('/category-manager')" active-class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="category" />
          </q-item-section>
          <q-item-section>카테고리 관리</q-item-section>
        </q-item>
      </q-list>
      <q-separator spaced />
      <div class="q-pa-sm text-caption text-grey-7 flex flex-center">v{{ $q.version }}</div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from 'src/stores/auth'

const leftDrawerOpen = ref(false)
const router = useRouter()
const auth = useAuthStore()
const route = useRoute()

function goToHome() {
  router.push('/')
}

function goToCategoryManager() {
  router.push('/category-manager')
}

function goToLogin() {
  router.push('/login')
}

function goToRegister() {
  router.push('/register')
}

function goToTransactionManager() {
  router.push('/transaction-manager')
}

async function logout() {
  await auth.logoutAction()
  router.push('/')
}

function isActive(path) {
  return route.path === path
}

// 앱 시작 시 로그인 상태/사용자 정보 fetch
onMounted(() => {
  auth.fetchUser()
})
</script>
