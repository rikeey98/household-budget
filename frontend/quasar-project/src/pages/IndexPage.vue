<template>
  <q-page>
    <div class="q-pa-md">
      <h4>CORS 테스트</h4>
      <q-btn @click="testCors" label="Django API 호출 테스트" color="primary" />
      <div v-if="response" class="q-mt-md">
        <h6>응답:</h6>
        <pre>{{ response }}</pre>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'IndexPage',
  setup () {
    const response = ref(null)

    const testCors = async () => {
      try {
        const result = await fetch('http://localhost:8000/api/test/')
        const data = await result.json()
        response.value = data
        console.log('CORS 테스트 성공:', data)
      } catch (error) {
        console.error('CORS 테스트 실패:', error)
        response.value = { error: error.message }
      }
    }

    return {
      response,
      testCors
    }
  }
}
</script>
