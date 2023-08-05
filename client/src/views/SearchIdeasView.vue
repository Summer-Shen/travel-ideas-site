<template>
  <div>
    <t-space direction="vertical" style="display: flex">
      <div>
        <div>
          <h1>Search for Travel Ideas</h1>
        </div>
      </div>
      <t-form
        ref="form"
        layout="inline"
        labelWidth="0"
        :rules="FORM_RULES"
        :data="formData"
        :colon="true"
        @reset="onReset"
        @submit="onSubmit"
      >
        <t-form-item name="searchBy">
          <t-radio-group v-model="formData.searchBy">
            <t-radio value="destination">By destination</t-radio>
            <t-radio value="tag">By tags</t-radio>
          </t-radio-group>
        </t-form-item>

        <t-form-item name="keyword">
          <t-input v-model="formData.keyword" placeholder="" @enter="onEnter"></t-input>
        </t-form-item>

        <t-form-item>
          <t-space size="small">
            <t-button theme="primary" type="submit">Submit</t-button>
          </t-space>
        </t-form-item>
      </t-form>

      <div class="cards">
        <div v-for="result in results" :key="result.id" class="card">
          <t-card :title="result.title">
            <div>Destination: {{ result.destination }}</div>
            <div>Date: {{ result.start_date }} to {{ result.end_date }}</div>
            <template #footer>
              <t-row :align="'middle'" justify="center">
                <t-col flex="auto" style="display: inline-flex; justify-content: right">
                  <t-badge :count="result.comments_count" show-zero>
                    <t-button variant="text" shape="square"> <chat-icon /> </t-button
                  ></t-badge>
                </t-col>
              </t-row>
            </template>
          </t-card>
        </div>
      </div>

      <footer class="copyright">Copyright @ 2022-2023 Travel Ideas. All Rights Reserved</footer>
    </t-space>
  </div>
</template>
<script setup>
import { ref, reactive } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { getCurrentInstance } from 'vue'
// import { useUserStore } from '@/stores/user'

import { ChatIcon } from 'tdesign-icons-vue-next'

const { proxy } = getCurrentInstance()

// const userStore = useUserStore()

const results = ref([])

const FORM_RULES = {
  keyword: [{ required: true, message: 'Please input search keyword' }]
}

const formData = reactive({
  searchBy: 'destination',
  keyword: ''
})
const form = ref(null)

const onReset = () => {
  MessagePlugin.success('Form reset')
}

const onSubmit = ({ validateResult, firstError }) => {
  if (validateResult === true) {
    proxy
      .$http({
        method: 'get',
        url:
          'api/ideas/search_by_' +
          (formData.searchBy === 'destination' ? 'dest' : 'tag') +
          '?q=' +
          formData.keyword
      })
      .then(function (response) {
        console.log(response)
        results.value = response.data
      })
      .catch(function (error) {
        console.log(error)
        MessagePlugin.warning(error.response.data)
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

<style scoped>
.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  row-gap: 4px;
}

.card {
  margin: 6px;
  width: calc(33.33% - 12px);
}
</style>
