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
      tarefaActual: null,
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
      if (this.tarefasConHora) {
        const agora = new Date();
        const horaActual = agora.toTimeString().slice(0, 5); // HH:MM

        for (const tarefa of this.tarefasConHora) {
          if (tarefa.hora && tarefa.hora.slice(0, 5) === horaActual) {
            console.log("tarefa desde comprobar horas ", tarefa);

            this.tarefaActual = tarefa;
            this.avisoActivo = true;
            return;
          }
        }
      }
    },
    cerrarAviso() {
      this.avisoActivo = false;
      this.tarefaActual = null;
    },
  },
  computed: {
    rutaActual() {
      return this.$route.path;
    },
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
    const usuarioStore = useUsuarioStore();
    usuarioStore.cargarDesdeStorage();

    if (!usuarioStore.id || !usuarioStore.nome) {
      this.$router.push("/formularios/inicio");
    }

    // Ejecutar comprobación de hora cada 30 segundos
    // this.intervalId = setInterval(this.comprobarHoras, 1000);
    // this.intervalId = setInterval(this.comprobarHoras, 5000);
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
      />
      <BarraNavegacion
        v-if="mostrarBarra"
        :rutaActual="rutaActual"
        @toggleModal="toggleModal"
      />
      <div :class="['vista', { 'sin-barras': !mostrarBarra }]">
        <router-view @emitirDatasConTarefas="emitirDatasConTarefas" />
      </div>

      <VentaPechar v-show="modalActivo" @pecharModal="toggleModal" />
      <VentaAviso
        v-if="avisoActivo && tarefaActual"
        :tarefaActual="tarefaActual"
        @cerrarAviso="cerrarAviso"
      />
    </div>
  </body>
</template>

<style>
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
