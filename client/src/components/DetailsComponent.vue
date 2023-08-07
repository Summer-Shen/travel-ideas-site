<template>
  <div>
    <t-loading size="small" :loading="isWeatherLoading || isLocationLoading" show-overlay>
      <t-space direction="vertical" size="small">
        <div v-if="!isWeatherLoading">Weather: {{ weatherText }}, {{ metricTemperatureText }}</div>
        <div v-if="!isLocationLoading">Location: {{ locationText.lat }} {{ locationText.lng }}</div>
      </t-space>
    </t-loading>
  </div>
</template>

<script setup>
import { getCurrentInstance } from 'vue'
import { ref } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'

const { proxy } = getCurrentInstance()

const props = defineProps(['id', 'destination'])

// eslint-disable-next-line vue/no-setup-props-destructure, no-unused-vars
const ideaId = props.id
// eslint-disable-next-line vue/no-setup-props-destructure
const ideaDestination = props.destination

const isWeatherLoading = ref(true)
const isLocationLoading = ref(true)

const weatherText = ref('')
const metricTemperatureText = ref('')
const locationText = ref({
  lat: '',
  lng: ''
})

proxy
  .$http({
    method: 'get',
    url:
      'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=lSlKMeOAekY9f4OR9ON2QnpRtAwwxYfD&q=' +
      ideaDestination
  })
  .then(function (response) {
    console.log('AccuWeather API response')
    console.log(response)
    if (response.data.length === 0) {
      return new Error('Weather information unavailable for this destination')
    }
    const locationKey = response.data[0].Key
    return proxy.$http({
      method: 'get',
      url:
        'http://dataservice.accuweather.com/currentconditions/v1/' +
        locationKey +
        '?apikey=lSlKMeOAekY9f4OR9ON2QnpRtAwwxYfD&language=en-us&details=false'
    })
  })
  .then(function (response) {
    console.log(response)
    weatherText.value = response.data[0].WeatherText
    const metricTemperature = response.data[0].Temperature.Metric
    metricTemperatureText.value = metricTemperature.Value + '℃'
    isWeatherLoading.value = false
  })
  .catch(function (error) {
    console.log(error)
    MessagePlugin.warning('An error occurred, please try again later')
  })
  .finally(function () {
    // always executed
  })

proxy
  .$http({
    method: 'get',
    url:
      'https://maps.googleapis.com/maps/api/geocode/json?address=' +
      ideaDestination.replace(' ', '+') +
      '&key=AIzaSyBhOCNz-pC7TCc-VVZBC_MuhYVTK-eBsKE'
  })
  .then(function (response) {
    console.log('Google Maps API response')
    console.log(response)
    if (response.data.results.length === 0) {
      return new Error('Google Maps location unavailable for this destination')
    }
    const location = response.data.results[0].geometry.location
    locationText.value = {
      lat: location.lat.toFixed(2) + '° ' + (location.lat > 0 ? 'N' : 'S'),
      lng: location.lng.toFixed(2) + '° ' + (location.lng > 0 ? 'E' : 'W')
    }
    isLocationLoading.value = false
  })
  .catch(function (error) {
    console.log(error)
    MessagePlugin.warning('An error occurred, please try again later')
  })
  .finally(function () {
    // always executed
  })
</script>
