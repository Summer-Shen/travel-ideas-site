import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const id = ref(0)
  const name = ref('')
  const email = ref('')

  function setUser(user) {
    id.value = user.id
    name.value = user.name
    email.value = user.email
  }

  function clearUser() {
    id.value = ''
    name.value = ''
    email.value = ''
  }

  return { id, name, email, setUser, clearUser }
})
