import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import dataV from '@jiaminghi/data-view'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'jquery'
import 'bootstrap'

Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.use(dataV);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
