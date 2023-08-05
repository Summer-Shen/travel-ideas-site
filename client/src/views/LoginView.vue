<template>
  <div class="login-wrapper">
    <t-space direction="vertical">
      <login-header />

      <div class="login-container">
        <div class="title-container">
          <h1 class="title margin-no">Login to</h1>
          <h1 class="title">Travel Ideas</h1>
          <!-- <div class="sub-title">
          <p class="tip">{{ type == 'register' ? '已有账号?' : '没有账号吗?' }}</p>
          <p class="tip" @click="switchType(type == 'register' ? 'login' : 'register')">
            {{ type == 'register' ? '登录' : '注册新账号' }}
          </p>
        </div> -->
        </div>
      </div>
      <t-form
        ref="form"
        labelWidth="120px"
        :rules="FORM_RULES"
        :data="formData"
        :colon="true"
        @reset="onReset"
        @submit="onSubmit"
      >
        <t-form-item label="Email" name="email">
          <t-input v-model="formData.email" @enter="onEnter"></t-input>
        </t-form-item>

        <t-form-item label="Password" name="password">
          <t-input v-model="formData.password" type="password" @enter="onEnter"></t-input>
        </t-form-item>

        <t-form-item>
          <t-space size="small">
            <t-button theme="primary" type="submit">Submit</t-button>
            <t-button theme="default" variant="base" type="reset">Reset</t-button>
          </t-space>
        </t-form-item>
      </t-form>
      <footer class="copyright">Copyright @ 2022-2023 Travel Ideas. All Rights Reserved</footer>
    </t-space>
  </div>
</template>
<script setup>
import { ref, reactive } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { getCurrentInstance } from 'vue'

const { proxy } = getCurrentInstance()

const FORM_RULES = {
  email: [
    { required: true, message: 'Email is required' },
    { email: { ignore_max_length: true }, message: 'Please input valid email address' }
  ],
  password: [{ required: true, message: 'Password is required' }]
}

const formData = reactive({
  email: '',
  password: ''
})
const form = ref(null)

const onReset = () => {
  MessagePlugin.success('Form reset')
}

const onSubmit = ({ validateResult, firstError }) => {
  if (validateResult === true) {
    proxy
      .$http({
        method: 'post',
        url: 'api/users/login',
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      .then(function (response) {
        // TODO
        console.log(response)
        MessagePlugin.success('login successful')
      })
      .catch(function (error) {
        console.log(error)
      })
      .finally(function () {
        // always executed
      })
  } else {
    console.log('Validate Errors: ', firstError, validateResult)
    MessagePlugin.warning(firstError)
  }
}

// eslint-disable-next-line no-unused-vars
const resetForm = () => {
  form.value.reset()
}

// disables Input component & triggers submit event when Enter key is pressed.
const onEnter = (_, { e }) => {
  e.preventDefault()
}
</script>
