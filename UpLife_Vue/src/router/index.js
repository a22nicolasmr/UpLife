import { createRouter, createWebHistory } from "vue-router";

// Importa los componentes
import Formularios from "@/views/Formularios.vue"; // Componente contenedor
import Inicio from "@/components/Inicio.vue"; // Componente de inicio de sesión
import Rexistro from "@/components/Rexistro.vue"; // Componente de registro

const routes = [
  {
    path: "/formularios",
    name: "formularios",
    component: Formularios,
    redirect: "/formularios/rexistro", // Asegúrate de que coincide con la ruta de rexistro
    children: [
      {
        path: "inicio", // Acceso a /formularios/inicio
        name: "inicio",
        component: Inicio,
      },
      {
        path: "rexistro", // Acceso a /formularios/rexistro
        name: "rexistro",
        component: Rexistro,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
