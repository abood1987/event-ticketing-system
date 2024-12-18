import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios"
import 'vuetify/styles'
import * as components from 'vuetify/components'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader

const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi', // This is already the default value - only for display purposes
  },
  components,
})

axios.defaults.baseURL = "https://webapp-72128148177.europe-west3.run.app";

const app = createApp(App);
app.config.globalProperties.$http = axios;
app.use(router);
app.use(vuetify);
app.mount('#app');