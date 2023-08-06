<template>
  <header>
    <t-head-menu v-model="menuValue" theme="light" @change="changeHandler">
      <template #logo> Travel Ideas </template>
      <t-menu-item value="search"> Search </t-menu-item>
      <t-menu-item value="create"> Create </t-menu-item>
      <t-menu-item value="more" disabled> More to come... </t-menu-item>
      <template #operations>
        <div v-if="userStore.id === 0">
          <t-button variant="text" shape="square" @click="handleLogin">
            <template #icon><t-icon name="login" /></template>
          </t-button>
          <t-button variant="text" shape="square" @click="handleRegister">
            <template #icon><t-icon name="user-add" /></template>
          </t-button>
        </div>
        <div v-else>
          <t-button variant="text" shape="square" @click="handleLogout">
            <template #icon><t-icon name="logout" /></template>
          </t-button>
        </div>
      </template>
    </t-head-menu>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { getCurrentInstance } from 'vue'
import pinia from '@/stores/index'
import { useUserStore } from '@/stores/user'

const { proxy } = getCurrentInstance()

// const isLoggedIn = ref(false)
const userStore = useUserStore(pinia)

const menuValue = ref('search')

const changeHandler = (active) => {
  if (active === 'search') {
    proxy.$router.push({
      path: '/search'
    })
  } else if (active === 'create') {
    proxy.$router.push({
      path: '/create'
    })
  }
  console.log('change', active)
}

const handleLogin = () => {
  proxy.$router.push({
    path: '/login'
  })
}

const handleRegister = () => {
  proxy.$router.push({
    path: '/register'
  })
}

const handleLogout = () => {
  userStore.clearUser()
  MessagePlugin.info('Logout successful')
  proxy.$router.push({
    path: '/login'
  })
}
</script>

<style scoped></style>
