<template>
  <ul>
    <li v-for="cat in categories" :key="cat.id">
      {{ cat.name }}
      <button @click="$emit('add', cat)">추가</button>
      <button @click="$emit('edit', cat)">수정</button>
      <button @click="$emit('delete', cat)">삭제</button>
      <CategoryTree v-if="cat.children && cat.children.length" :categories="cat.children" @add="$emit('add', $event)" @edit="$emit('edit', $event)" @delete="$emit('delete', $event)" />
    </li>
  </ul>
</template>

<script setup>
defineProps({
  categories: {
    type: Array,
    required: true
  }
})
</script> 