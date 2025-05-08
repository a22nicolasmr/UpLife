import { createRouter, createWebHistory } from "vue-router";

import Formularios from "@/views/Formularios.vue";
import Inicio from "@/components/Formularios/Inicio.vue";
import Rexistro from "@/components/Formularios/Rexistro.vue";
import Tarefas from "@/views/Tarefas.vue";
import ListaTarefas from "@/components/Tarefas/ListaTarefas.vue";
import EngadirTarefas from "@/components/Tarefas/EngadirTarefas.vue";
import Auga from "@/views/Auga.vue";
import Comidas from "@/views/Comidas.vue";
import Exercicios from "@/views/Exercicios.vue";
import Medallas from "@/views/Medallas.vue";
import Perfil from "@/views/Perfil.vue";
import Plantillas from "@/views/Plantillas.vue";
import Calculadora from "@/components/Perfil/Calculadora.vue";
import Calculador from "@/components/Perfil/Calculador.vue";

const routes = [
  {
    // redirixir a tarefas cando se abre a aplicacion
    path: "/",
    redirect: "/tarefas",
    // redirect: "/formularios/rexistro",
  },
  {
    path: "/formularios",
    name: "formularios",
    component: Formularios,
    redirect: "/formularios/rexistro",
    children: [
      {
        path: "inicio",
        name: "inicio",
        component: Inicio,
      },
      {
        path: "rexistro",
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
        children: [
          {
            path: "calculador",
            name: "calculador",
            component: Calculador,
          },
        ],
      },
    ],
  },
  {
    path: "/plantillas",
    name: "plantillas",
    component: Plantillas,
  },
];

// creacion do router coas rutas
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
