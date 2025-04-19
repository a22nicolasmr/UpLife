<script>
export default {
  mounted() {
    // Redirige automáticamente a la vista de los formularios
    this.$router.push("/formularios");
  },
};
</script>
<template>
  <body>
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
