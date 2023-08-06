import { createRouter, createWebHistory } from 'vue-router'
import pinia from '@/stores/index'
import { useUserStore } from '@/stores/user'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import SearchIdeasView from '../views/SearchIdeasView.vue'
import CreateIdeasView from '../views/CreateIdeaView.vue'
import ModifyIdeasView from '../views/ModifyIdeaView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: SearchIdeasView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchIdeasView
    },
    {
      path: '/create',
      name: 'create',
      component: CreateIdeasView
    },
    {
      path: '/modify/:id',
      name: 'modify',
      component: ModifyIdeasView
    }
  ]
})

const userStore = useUserStore(pinia)

// eslint-disable-next-line no-unused-vars
router.beforeEach(async (to, from) => {
  if (
    // make sure the user is authenticated
    userStore.id === 0 &&
    // avoid an infinite redirect
    to.name !== 'login' &&
    to.name !== 'register'
  ) {
    // redirect the user to the login page
    return { name: 'login' }
  }
})

export default router
