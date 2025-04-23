import { createRouter, createWebHistory } from "vue-router";

// Importa los componentes
import Formularios from "@/views/Formularios.vue"; // Componente contenedor
import Inicio from "@/components/Inicio.vue"; // Componente de inicio de sesión
import Rexistro from "@/components/Rexistro.vue"; // Componente de registro
import Tarefas from "@/views/Tarefas.vue";
import ListaTarefas from "@/components/ListaTarefas.vue";
import EngadirTarefas from "@/components/EngadirTarefas.vue";
import Auga from "@/views/Auga.vue";
import Comidas from "@/views/Comidas.vue";
import Exercicios from "@/views/Exercicios.vue";
import Medallas from "@/views/Medallas.vue";
import Perfil from "@/views/Perfil.vue";
import Plantillas from "@/views/Plantillas.vue";
import Calculadora from "@/components/Calculadora.vue";

const routes = [
  {
    path: "/",
    redirect: "/tarefas", // o cualquier ruta principal
  },
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
  {
    path: "/tarefas",
    name: "tarefas",
    component: Tarefas,
    children: [
      {
        path: "lista",
        name: "lista",
        component: ListaTarefas,
      },
      {
        path: "engadirTarefas",
        name: "engadirTarefas",
        component: EngadirTarefas,
      },
    ],
  },
  {
    path: "/auga",
    name: "auga",
    component: Auga,
  },
  {
    path: "/comidas",
    name: "comidas",
    component: Comidas,
  },
  {
    path: "/exercicios",
    name: "exercicios",
    component: Exercicios,
  },
  {
    path: "/medallas",
    name: "medallas",
    component: Medallas,
  },
  {
    path: "/perfil",
    name: "perfil",
    component: Perfil,
    children: [
      {
        path: "calculadora",
        name: "calculadora",
        component: Calculadora,
      },
    ],
  },
  {
    path: "/plantillas",
    name: "plantillas",
    component: Plantillas,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
