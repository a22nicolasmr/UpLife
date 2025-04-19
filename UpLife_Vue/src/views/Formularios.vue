<script>
export default {
  name: "Formularios",
};
</script>

<template>
  <div class="contenedor">
    <!-- Mitad izquierda -->
    <div class="izquierda">
      <img src="../imaxes/portadaWeb.jpg" alt="" />
    </div>

    <!-- Mitad derecha -->
    <div class="derecha">
      <!-- Vista del formulario -->
      <router-view></router-view>
    </div>
  </div>
</template>

<style>
.contenedor {
  display: flex;
  height: 100vh;
}

.izquierda,
.derecha {
  width: 50%;
  padding: 40px;
  box-sizing: border-box;
}

.izquierda {
  background-color: #e6f0ff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.derecha {
  background-color: #fff;
  display: flex; /* Usamos flexbox */
  justify-content: center; /* Centra horizontalmente */
  align-items: flex-start; /* Alinea el contenido en la parte superior */
}

.navegacion {
  margin-bottom: 20px;
}
button {
  background-color: #4880ff;
  color: #ffffff;
}
</style>
