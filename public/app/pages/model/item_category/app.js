import {
  Vue,
} from "../../../assets/js/util.js"


import 'element-ui/lib/theme-default/index.css'
import App from './app.vue'

import RegionPicker from 'vue-region-picker'
import REGION_DATA from 'china-area-data'

Vue.use(RegionPicker, {
  region: REGION_DATA
})




/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App)
})
