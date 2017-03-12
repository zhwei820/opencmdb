import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import App from './app.vue'

import RegionPicker from 'vue-region-picker'
import REGION_DATA from 'china-area-data'

Vue.use(RegionPicker, {
  region: REGION_DATA
})


import VueResource from 'vue-resource';
Vue.use(VueResource);

Vue.use(ElementUI)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App)
})
