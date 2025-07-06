<template>
  <q-page class="flex flex-center">
    <q-card>
      <q-card-section>
        <div class="text-h6">로그인</div>
      </q-card-section>
      <q-card-section>
        <q-input v-model="username" label="아이디" />
        <q-input v-model="password" label="비밀번호" type="password" />
      </q-card-section>
      <q-card-actions align="right">
        <q-btn label="로그인" color="primary" @click="handleLogin" :loading="auth.loading" />
        <q-btn label="회원가입" color="secondary" flat @click="goToRegister" />
      </q-card-actions>
      <q-card-section v-if="auth.error" class="text-negative">
        {{ auth.error }}
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const auth = useAuthStore();
const router = useRouter();

async function handleLogin() {
  await auth.loginAction(username.value, password.value);
  if (auth.isAuthenticated) {
    router.push('/');
  }
}

function goToRegister() {
  router.push('/register');
}
</script> 