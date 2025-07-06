<template>
  <q-page class="flex flex-center">
    <q-card>
      <q-card-section>
        <div class="text-h6">회원가입</div>
      </q-card-section>
      <q-card-section>
        <q-input v-model="username" label="아이디" />
        <q-input v-model="email" label="이메일" type="email" />
        <q-input v-model="password" label="비밀번호" type="password" />
        <q-input v-model="password2" label="비밀번호 확인" type="password" />
      </q-card-section>
      <q-card-actions align="right">
        <q-btn label="회원가입" color="primary" @click="handleRegister" :loading="loading" />
      </q-card-actions>
      <q-card-section v-if="error" class="text-negative">
        {{ error }}
      </q-card-section>
      <q-card-section v-if="success" class="text-positive">
        {{ success }}
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import { register } from 'src/services/api';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');
const password2 = ref('');
const error = ref('');
const success = ref('');
const loading = ref(false);
const router = useRouter();

async function handleRegister() {
  error.value = '';
  success.value = '';
  loading.value = true;
  try {
    await register({ username: username.value, email: email.value, password: password.value, password2: password2.value });
    success.value = '회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.';
    setTimeout(() => router.push('/login'), 1500);
  } catch (err) {
    error.value = err?.response?.data?.detail || '회원가입 실패: 입력값을 확인하세요.';
  } finally {
    loading.value = false;
  }
}
</script> 