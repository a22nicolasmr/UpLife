<script>
import BarraNavegacion from "./components/BarraNavegacion.vue";

export default {
  components: {
    BarraNavegacion,
  },
  computed: {
    // Computado para la ruta actual
    rutaActual() {
      return this.$route.path;
    },
  },
};
</script>

<template>
  <body>
    <BarraNavegacion />

    <router-view></router-view>
  </body>
</template>

<style>
body {
  overflow: hidden; /* Desactiva el scrollbar */
  height: 100%;
  width: 100%;
}
</style>
