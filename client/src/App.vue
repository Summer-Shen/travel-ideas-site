<script setup>
import { RouterView } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue'
</script>

<template>
  <div class="body">
    <HeaderComponent />

    <div class="content">
      <RouterView />
    </div>
  </div>
</template>
