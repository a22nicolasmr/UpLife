<script>
import BarraNavegacion from "./components/BarraNavegacion.vue";
import BarraSuperior from "./components/BarraSuperior.vue";

export default {
  components: {
    BarraNavegacion,
    BarraSuperior,
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
    mounted() {
      const usuarioStore = useUsuarioStore();
      usuarioStore.cargarDesdeStorage(); // Cargar los datos del usuario

      // Esperar a que los datos se carguen
      if (!usuarioStore.id || !usuarioStore.nome) {
        this.$router.push("/formularios/inicio");
      }
    },
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
      <BarraNavegacion v-if="mostrarBarra" :rutaActual="rutaActual" />
      <div :class="['vista', { 'sin-barras': !mostrarBarra }]">
        <router-view />
      </div>
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
  font-family: "Nunito Sans", sans-serif !important; /* !important asegura que prevalezca */
}

.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
}
.vista {
  margin-top: 10vh;
  margin-left: 220px; /* Igual al ancho de tu barra */
  width: calc(100% - 180px);
  height: 100vh;
  overflow-y: hidden; /* Para scroll si el contenido es largo */
}

/* quitar barras en los formularios */
.sin-barras {
  margin: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
}
</style>
