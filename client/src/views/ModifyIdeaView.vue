<template>
  <t-config-provider :global-config="globalConfig">
    <div>
      <t-space direction="vertical" style="display: flex">
        <div>
          <div>
            <h1>Modify Your Travel Idea</h1>
          </div>
        </div>
        <t-row>
          <t-col :span="6">
            <t-form
              ref="form"
              labelWidth="120px"
              :rules="FORM_RULES"
              :data="formData"
              :colon="true"
              @reset="onReset"
              @submit="onSubmit"
            >
              <t-form-item label="Title" name="title">
                <t-input v-model="formData.title" placeholder="" @enter="onEnter"></t-input>
              </t-form-item>

              <t-form-item label="Destination" name="destination">
                <t-input v-model="formData.destination" placeholder="" @enter="onEnter"></t-input>
              </t-form-item>

              <t-form-item label="Start date" name="start_date">
                <t-date-picker v-model="formData.start_date" valueType="Date" />
              </t-form-item>

              <t-form-item label="End date" name="end_date">
                <t-date-picker v-model="formData.end_date" valueType="Date" />
              </t-form-item>

              <t-form-item label="Tags" name="tags">
                <t-tag-input
                  v-model="formData.tags"
                  placeholder="Please type & use backspace to add new tags"
                  excess-tags-display-type="scroll"
                />
              </t-form-item>

              <t-form-item>
                <t-space size="small">
                  <t-button theme="primary" type="submit">Submit</t-button>
                  <t-button theme="default" variant="base" type="reset">Reset</t-button>
                </t-space>
              </t-form-item>
            </t-form>
          </t-col>
        </t-row>
        <footer class="copyright">Copyright @ 2022-2023 Travel Ideas. All Rights Reserved</footer>
      </t-space>
    </div>
  </t-config-provider>
</template>
<script setup>
import { ref, reactive } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { getCurrentInstance } from 'vue'
import pinia from '@/stores/index'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'

const { proxy } = getCurrentInstance()

const userStore = useUserStore(pinia)

const DATE_PICK_CONFIGS = {
  placeholder: {
    date: 'Select date',
    month: 'Select month',
    year: 'Select year'
  },
  weekdays: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  rangeSeparator: ' ~ ',
  format: 'YYYYMMDD',
  yearAriaLabel: '',
  now: 'Now',
  selectTime: 'Select Time',
  selectDate: 'Select Date'
}

const globalConfig = {
  datePicker: DATE_PICK_CONFIGS
}

// data validation rules
const FORM_RULES = {
  title: [{ required: true, message: 'Title is required' }],
  destination: [{ required: true, message: 'Destination is required' }],
  start_date: [
    { required: true, message: 'Start date is required' },
    {
      validator: (val) => val <= formData.end_date,
      message: 'Start date should be earlier or the same as end date'
    }
  ],
  end_date: [
    { required: true, message: 'End date is required' },
    {
      validator: (val) => val >= formData.start_date,
      message: 'End date should be later or the same as start date'
    }
  ],
  tags: [{ required: true, message: 'Tags are required' }]
}

proxy
  .$http({
    method: 'get',
    url: 'api/ideas/get?q=' + proxy.$router.currentRoute.value.params.id
  })
  .then(function (response) {
    console.log(response)
    formData.title = response.data.title
    formData.destination = response.data.destination
    formData.start_date = response.data.start_date
    formData.end_date = response.data.end_date
  })
  .catch(function (error) {
    console.log(error)
    MessagePlugin.warning(error.response.data)
  })
  .finally(function () {
    // always executed
  })

proxy
  .$http({
    method: 'get',
    url: 'api/tags/get_by_idea?q=' + proxy.$router.currentRoute.value.params.id
  })
  .then(function (response) {
    console.log(response)
    formData.tags = response.data.map((tag) => tag.name)
  })
  .catch(function (error) {
    console.log(error)
    MessagePlugin.warning(error.response.data)
  })
  .finally(function () {
    // always executed
  })

const formData = reactive({
  user_id: userStore.id,
  title: '',
  destination: '',
  start_date: dayjs().toDate(),
  end_date: dayjs().toDate(),
  tags: []
})
const form = ref(null)

const onReset = () => {
  MessagePlugin.success('Form reset')
}

const onSubmit = ({ validateResult, firstError }) => {
  // console.log(formData)
  const stringifiedFormData = {}
  for (let key in formData) {
    if (Array.isArray(formData[key])) {
      // stringify array data s.t. backend can parse array items
      stringifiedFormData[key] = JSON.stringify(formData[key])
    } else {
      stringifiedFormData[key] = formData[key]
    }
  }
  console.log(stringifiedFormData)
  if (validateResult === true) {
    proxy
      .$http({
        method: 'post',
        url: 'api/ideas/create',
        data: stringifiedFormData,
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      .then(function (response) {
        console.log(response)
        MessagePlugin.success('New idea "' + response.data.title + '" created.')
        proxy.$router.push({
          path: '/search'
        })
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
