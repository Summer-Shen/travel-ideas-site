<template>
  <div>
    <t-space direction="vertical" size="small">
      <div>Weather: {{ weatherText }}, {{ metricTemperatureText }}</div>
    </t-space>
  </div>
</template>

<script setup>
import { getCurrentInstance } from 'vue'
import { ref } from 'vue'

const { proxy } = getCurrentInstance()

const props = defineProps(['id', 'destination'])

// eslint-disable-next-line vue/no-setup-props-destructure, no-unused-vars
const ideaId = props.id
// eslint-disable-next-line vue/no-setup-props-destructure
const ideaDestination = props.destination

const weatherText = ref('')
const metricTemperatureText = ref('')

proxy
  .$http({
    method: 'get',
    url:
      'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=lSlKMeOAekY9f4OR9ON2QnpRtAwwxYfD&q=' +
      ideaDestination
  })
  .then(function (response) {
    console.log(response)
    const locationKey = response.data[0].Key
    proxy
      .$http({
        method: 'get',
        url:
          'http://dataservice.accuweather.com/currentconditions/v1/' +
          locationKey +
          '?apikey=lSlKMeOAekY9f4OR9ON2QnpRtAwwxYfD&language=en-us&details=false'
      })
      .then(function (response) {
        console.log(response)
        weatherText.value = response.data[0].WeatherText
        const metricTemperature = response.data[0].Temperature.Metric
        metricTemperatureText.value = metricTemperature.Value + '℃'
      })
      .catch(function (error) {
        console.log(error)
        // MessagePlugin.warning(error.response.data)
      })
      .finally(function () {
        // always executed
      })
  })
  .catch(function (error) {
    console.log(error)
    // MessagePlugin.warning(error.response.data)
  })
  .finally(function () {
    // always executed
  })
</script>
