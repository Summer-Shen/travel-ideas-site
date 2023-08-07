<template>
  <div>
    <t-space direction="vertical" size="small">
      <t-loading size="small" :loading="isCommentsLoading" show-overlay>
        <t-list>
          <t-list-item v-for="(item, index) in comments" :key="index">
            <template #content>
              <t-comment
                :author="item.user_name"
                :datetime="dayjs(item.created_at).fromNow()"
                :content="item.content"
              >
              </t-comment>
            </template>
          </t-list-item>
        </t-list>
      </t-loading>

      <div class="form-container">
        <t-textarea
          v-model="appendedComment"
          placeholder="Write your comment..."
          :maxlength="255"
        />
        <t-button class="form-submit" @click="submitReply">Submit</t-button>
      </div>
    </t-space>
  </div>
</template>

<script setup>
import { getCurrentInstance } from 'vue'
import { ref } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import pinia from '@/stores/index'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

const { proxy } = getCurrentInstance()

const userStore = useUserStore(pinia)

dayjs.extend(relativeTime)

const props = defineProps(['id'])

// eslint-disable-next-line vue/no-setup-props-destructure, no-unused-vars
const ideaId = props.id

const isCommentsLoading = ref(true)

const comments = ref([])
const appendedComment = ref('')

proxy
  .$http({
    method: 'get',
    url: 'api/comments/get_by_idea?q=' + ideaId
  })
  .then(function (response) {
    console.log(response)
    comments.value = response.data
    isCommentsLoading.value = false
  })
  .catch(function (error) {
    console.log(error)
    MessagePlugin.warning(error.response.data)
  })
  .finally(function () {
    // always executed
  })

const submitReply = () => {
  const formData = new FormData()
  formData.append('idea_id', ideaId)
  formData.append('user_id', userStore.id)
  formData.append('content', appendedComment.value)
  proxy
    .$http({
      method: 'post',
      url: 'api/comments/create',
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then(function (response) {
      console.log(response)
      MessagePlugin.success('Comment sent successfully')
      comments.value = [response.data, ...comments.value]
      appendedComment.value = ''
    })
    .catch(function (error) {
      console.log(error)
      MessagePlugin.warning(error.response.data)
    })
    .finally(function () {
      // always executed
    })
}
</script>

<style scoped>
.t-list-item {
  padding-left: 0;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.form-submit {
  margin-top: 8px;
}

.t-space {
  display: flex;
}
</style>
