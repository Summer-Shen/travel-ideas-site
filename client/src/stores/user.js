import { ref } from 'vue'
import { defineStore } from 'pinia'
import Cookies from 'js-cookie'

export const useUserStore = defineStore('user', () => {
  console.log(localStorage.getItem('user_id'))

  const id = ref(Number(Cookies.get('user_id')) || 0)
  const name = ref(Cookies.get('user_name') || '')
  const email = ref(Cookies.get('user_email') || '')

  // set user info in store and in Cookies
  function setUser(user) {
    id.value = user.id
    Cookies.set('user_id', Number(id.value))
    name.value = user.name
    Cookies.set('user_name', name.value)
    email.value = user.email
    Cookies.set('user_email', email.value)
  }

  // clear user info in store and in Cookies
  function clearUser() {
    id.value = 0
    Cookies.remove('user_id')
    name.value = ''
    Cookies.remove('user_name')
    email.value = ''
    Cookies.remove('user_email')
  }

  return { id, name, email, setUser, clearUser }
})
