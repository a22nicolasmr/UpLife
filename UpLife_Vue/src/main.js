import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Importa el router configurado

const app = createApp(App);
app.use(router); // Usa el router
app.mount("#app");
