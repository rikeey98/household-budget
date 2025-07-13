<template>
  <q-tree
    :nodes="categories"
    node-key="id"
    label-key="name"
    :default-expand-all="true"
  >
    <template v-slot:default-header="props">
      <div class="row items-center q-gutter-sm">
        <q-icon v-if="props.node.emoji" :name="props.node.emoji" size="md" />
        <span>{{ props.node.name }}</span>
        <q-btn dense flat icon="edit" @click.stop="$emit('edit', props.node)" size="sm" />
        <q-btn dense flat icon="delete" color="negative" @click.stop="$emit('delete', props.node)" size="sm" />
      </div>
    </template>
  </q-tree>
</template>

<script setup>
import { QTree, QBtn, QIcon } from 'quasar'
defineProps({
  categories: {
    type: Array,
    required: true
  }
})
</script> 