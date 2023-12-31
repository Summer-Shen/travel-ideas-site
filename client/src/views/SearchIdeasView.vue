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

      <div>{{ results.length }} matched records</div>

      <div class="cards">
        <div v-for="result in results" :key="result.id" class="card">
          <t-card :title="result.title" size="small" hoverShadow>
            <div>Destination: {{ result.destination }}</div>
            <div>
              Date: {{ dayjs(result.start_date).format('MM/YYYY') }} to
              {{ dayjs(result.end_date).format('MM/YYYY') }}
            </div>
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
                      <t-button variant="text" shape="square" @click="handleEdit(result.id)">
                        <edit-icon />
                      </t-button>
                    </div>
                    <t-button
                      variant="text"
                      shape="square"
                      @click="showDetails(result.id, result.destination)"
                    >
                      <bulletpoint-icon />
                    </t-button>
                    <t-badge
                      :count="result.comments_count"
                      show-zero
                      size="small"
                      :offset="[4, 4]"
                      :color="result.comments_count ? '#0052D9' : '#a6a6a6'"
                    >
                      <t-button
                        variant="text"
                        shape="square"
                        @click="showComments(result.id, result.title)"
                      >
                        <chat-icon />
                      </t-button>
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

  <t-config-provider :global-config="globalConfig">
    <t-dialog
      v-model:visible="isDetailsVisible"
      attach="body"
      :header="'Details: ' + currIdeaDestination"
      destroy-on-close
      :on-confirm="
        () => {
          isDetailsVisible = false
          currIdeaId = 0
          currIdeaDestination = ''
        }
      "
      :cancelBtn="null"
    >
      <template #body>
        <details-component :id="currIdeaId" :destination="currIdeaDestination"></details-component>
      </template>
    </t-dialog>

    <t-dialog
      v-model:visible="isCommentsVisible"
      attach="body"
      :header="'Comments: ' + currIdeaTitle"
      destroy-on-close
      :on-confirm="
        () => {
          isCommentsVisible = false
          currIdeaId = 0
          currIdeaTitle = ''
        }
      "
      :confirmBtn="null"
      :cancelBtn="null"
    >
      <template #body>
        <comments-component :id="currIdeaId"></comments-component>
      </template>
    </t-dialog>
  </t-config-provider>
</template>
<script setup>
import { ref, reactive } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { getCurrentInstance } from 'vue'
import pinia from '@/stores/index'
import { useUserStore } from '@/stores/user'

import { BulletpointIcon, DeleteIcon, EditIcon, ChatIcon } from 'tdesign-icons-vue-next'
import DetailsComponent from '../components/DetailsComponent.vue'
import CommentsComponent from '../components/CommentsComponent.vue'
import dayjs from 'dayjs'

const globalConfig = {
  dialog: {
    confirm: 'Confirm',
    // cancel: 'cancel',
    cancel: {
      theme: 'default',
      variant: 'outline',
      content: 'Cancel'
    },
    confirmBtnTheme: {
      default: 'primary',
      info: 'primary',
      warning: 'warning',
      danger: 'danger',
      success: 'success'
    }
  }
}

const { proxy } = getCurrentInstance()

const userStore = useUserStore(pinia)

const results = ref([])
const isDetailsVisible = ref(false)
const isCommentsVisible = ref(false)
const currIdeaId = ref(0)
const currIdeaTitle = ref('')
const currIdeaDestination = ref('')

proxy
  .$http({
    method: 'get',
    url: 'api/ideas/search_by_dest?q='
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

const handleEdit = (idea_id) => {
  proxy.$router.push({
    path: '/' + idea_id
  })
}

const showDetails = (idea_id, idea_destination) => {
  currIdeaId.value = idea_id
  currIdeaDestination.value = idea_destination
  isDetailsVisible.value = true
}

const showComments = (idea_id, idea_title) => {
  currIdeaId.value = idea_id
  currIdeaTitle.value = idea_title
  isCommentsVisible.value = true
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

:global(.t-dialog__body) {
  padding-bottom: 0 !important;
}

:global(.t-dialog__footer) {
  display: none !important;
}
</style>
