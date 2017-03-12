// import Vue from 'vue'
// import ElementUI from 'element-ui'
// Vue.use(ElementUI)

import {
  Vue
} from "../../../assets/js/util.js"

import 'element-ui/lib/theme-default/index.css'
import "../../../assets/css/normalize.css"
import App from './app.vue'




new Vue({
  el: '#app',
  render: h => h(App)
})