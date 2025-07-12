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
    >
      <q-list>
        <q-item clickable @click="goToHome">
          <q-item-section>홈</q-item-section>
        </q-item>
        <q-item clickable @click="goToCategoryManager">
          <q-item-section>카테고리 관리</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'src/stores/auth'

const leftDrawerOpen = ref(false)
const router = useRouter()
const auth = useAuthStore()

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

async function logout() {
  await auth.logoutAction()
  router.push('/')
}

// 앱 시작 시 로그인 상태/사용자 정보 fetch
onMounted(() => {
  auth.fetchUser()
})
</script>
