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
            <t-radio value="destination">By Destination</t-radio>
            <t-radio value="tag">By Tags</t-radio>
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
          <t-card :title="result.title" size="small" hoverShadow="true">
            <div>Destination: {{ result.destination }}</div>
            <div>Date: {{ result.start_date }} to {{ result.end_date }}</div>
            <template #footer>
              <t-row :align="'middle'" justify="center" style="gap: 24px">
                <t-col flex="auto" style="display: inline-flex; justify-content: right">
                  <t-space size="small">
                    <div v-if="result.user_id === userStore.id">
                      <t-button variant="text" shape="square" @click="handleDelete(result.id)">
                        <delete-icon />
                      </t-button>
                    </div>
                    <div v-if="result.user_id === userStore.id">
                      <t-button variant="text" shape="square"> <edit-icon /> </t-button>
                    </div>
                    <t-button variant="text" shape="square"> <bulletpoint-icon /> </t-button>
                    <t-badge
                      :count="result.comments_count"
                      show-zero
                      size="small"
                      :offset="[4, 4]"
                      :color="result.comments_count ? '#0052D9' : '#a6a6a6'"
                    >
                      <t-button variant="text" shape="square"> <chat-icon /> </t-button>
                    </t-badge>
                  </t-space>
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
import pinia from '@/stores/index'
import { useUserStore } from '@/stores/user'

import { BulletpointIcon, DeleteIcon, EditIcon, ChatIcon } from 'tdesign-icons-vue-next'

const { proxy } = getCurrentInstance()

const userStore = useUserStore(pinia)

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

const handleDelete = (idea_id) => {
  const formData = new FormData()
  formData.append('idea_id', idea_id)
  proxy
    .$http({
      method: 'post',
      url: 'api/ideas/delete',
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then(function (response) {
      console.log(response)
      results.value = results.value.filter((result) => result.id !== idea_id)
      MessagePlugin.info('Idea deleted')
    })
    .catch(function (error) {
      console.log(error)
      MessagePlugin.warning(error.response.data)
    })
    .finally(function () {
      // always executed
    })
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
  row-gap: 4px;
}

.card {
  margin: 6px;
  width: calc(33.33% - 12px);
}
</style>
