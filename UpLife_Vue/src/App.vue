<script>
import BarraNavegacion from "./components/BarraNavegacion.vue";
import BarraSuperior from "./components/BarraSuperior.vue";
import VentaAviso from "./components/VentaAviso.vue";
import VentaPechar from "./components/VentaPechar.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      modalActivo: false,
      avisoActivo: false,
      tarefasConHora: [],
      intervalId: null,
    };
  },
  components: {
    BarraNavegacion,
    BarraSuperior,
    VentaPechar,
    VentaAviso,
  },
  methods: {
    toggleModal() {
      this.modalActivo = !this.modalActivo;
    },
    emitirDatasConTarefas(tarefas) {
      this.tarefasConHora = tarefas;
    },
    comprobarHoras() {
      const agora = new Date();
      const horaActual = agora.toTimeString().slice(0, 5); // "HH:MM"
      console.log(this.tarefasConHora);

      // Recorrer tarefas
      for (const tarefa of this.tarefasConHora) {
        console.log("Hora tarefa", tarefa.hora);
        if (tarefa.hora && tarefa.hora.slice(0, 5) === horaActual) {
          this.avisoActivo = true;
          return; // Solo activar una vez por coincidencia
        }
      }
    },
  },
  computed: {
    rutaActual() {
      return this.$route.path;
    },

    //se a ruta actual e calquera dos formularios de rexistro , oculta a barra de navegación
    mostrarBarra() {
      return (
        this.$route.path !== "/formularios/rexistro" &&
        this.$route.path !== "/formularios/inicio"
      );
    },
    nombreUsuario() {
      return this.$route.query.nome;
    },
  },
  mounted() {
    // Cada 30 segundos (o 10s para testear más rápido)
    // this.intervalId = setInterval(this.comprobarHoras, 1000);

    // Comprobar también que el usuario esté cargado
    const usuarioStore = useUsuarioStore();
    usuarioStore.cargarDesdeStorage();
    if (!usuarioStore.id || !usuarioStore.nome) {
      this.$router.push("/formularios/inicio");
    }
  },
  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
};
</script>

<template>
  <body>
    <div class="layout">
      <BarraSuperior
        v-if="mostrarBarra"
        :nome="nombreUsuario"
        :key="nombreUsuario"
      ></BarraSuperior>
      <BarraNavegacion
        v-if="mostrarBarra"
        :rutaActual="rutaActual"
        @toggleModal="toggleModal"
      />
      <div :class="['vista', { 'sin-barras': !mostrarBarra }]">
        <router-view @emitirDatasConTarefas="emitirDatasConTarefas" />
      </div>
      <VentaPechar
        v-show="modalActivo"
        @pecharModal="toggleModal"
      ></VentaPechar>
      <VentaAviso
        v-show="avisoActivo"
        :tarefasConHora="tarefasConHora"
      ></VentaAviso>
    </div>
  </body>
</template>

<style>
/* fonte de Google nunito sans */
@import url("https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,wght@0,200;0,300;0,400;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,600;1,700;1,800;1,900&display=swap");
body {
  margin: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
  background-color: #eff0f2;
}
* {
  font-family: "Nunito Sans", sans-serif !important;
}

.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
}
.vista {
  margin-top: 10vh;
  margin-left: 220px;
  width: calc(100% - 180px);
  height: 100vh;
  overflow-y: hidden;
}

.sin-barras {
  margin: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
}
</style>
