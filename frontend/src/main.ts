import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import "./assets/main.css";

const app = createApp(App); // Create a Pinia instance
const pinia = createPinia(); // Use the Pinia instance in the Vue app

app.use(pinia); // Mount the Vue app to the DOM
app.mount("#app"); //mount the Vue app to the DOM element with id 'app'
