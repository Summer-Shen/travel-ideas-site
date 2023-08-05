import { ref } from 'vue'
import { defineStore } from 'pinia'
import Cookies from 'js-cookie'

export const useUserStore = defineStore('user', () => {
  console.log(localStorage.getItem('user_id'))

  const id = ref(Number(Cookies.get('user_id')) || 0)
  const name = ref(Cookies.get('user_name') || '')
  const email = ref(Cookies.get('user_email') || '')

  function setUser(user) {
    id.value = user.id
    Cookies.set('user_id', Number(id.value))
    name.value = user.name
    Cookies.set('user_name', name.value)
    email.value = user.email
    Cookies.set('user_email', email.value)
  }

  function clearUser() {
    id.value = ''
    Cookies.set('user_id', 0)
    name.value = ''
    Cookies.set('user_name', '')
    email.value = ''
    Cookies.set('user_email', '')
  }

  return { id, name, email, setUser, clearUser }
})
