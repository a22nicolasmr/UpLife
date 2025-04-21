<script>
export default {
  data() {
    return {
      // Aquí puedes usar datos de tu usuario, ya sea de un API o del estado global (Vuex)
      user: {
        image: "../imaxes/usuario.jpg", // Ruta a la imagen del usuario
        name: "Usuario Ejemplo", // Nombre del usuario
        medals: 5, // Número de medallas
      },
    };
  },
};
</script>
<template>
  <div class="barra-superior">
    <div class="usuario-info">
      <img :src="user.image" alt="Usuario" class="usuario-imagen" />
      <div class="usuario-nombre">{{ user.name }}</div>
      <div class="usuario-medallas">{{ user.medals }} Medallas</div>
    </div>
  </div>
</template>

<style scoped>
.barra-superior {
  background-color: #4880ff; /* Azul */
  color: white;
  padding: 20px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  position: fixed;
  top: 0;
  left: 180px; /* Alineado con la barra lateral, ajusta según el ancho de tu barra lateral */
  width: calc(
    100% - 180px
  ); /* Asegura que la barra superior ocupe todo el espacio menos la barra lateral */
  z-index: 1000;
}

.usuario-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 20px;
}

.usuario-imagen {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.usuario-nombre {
  font-weight: bold;
}

.usuario-medallas {
  font-size: 14px;
  color: #d8d8d8;
}
</style>
