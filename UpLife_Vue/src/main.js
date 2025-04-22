import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Importa el router configurado
import { createPinia } from "pinia";
import piniaPersistedState from "pinia-plugin-persistedstate";
const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPersistedState);
app.use(pinia);
app.use(router); // Usa el router
app.mount("#app");
