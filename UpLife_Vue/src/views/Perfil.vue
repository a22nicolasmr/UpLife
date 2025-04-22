<script>
export default {
  data() {
    return { name: "Apples", message: "I like apples" };
  },
};
</script>

<template>
  <div class="container">
    <h1>Perfil</h1>
    <div class="datos">
      <h2>Detalles da conta</h2>
      <h4>Nome:</h4>
      <h4>Email:</h4>
      <h4>Nome de usuario:</h4>
      <h4>Imaxe de usuario:</h4>
      <img src="" alt="Imaxe de usuario" />
      <h2>Datos do usuario</h2>
      <h4>Peso:</h4>
      <h4>Obxectivo:</h4>
      <h4>Actividade:</h4>
      <h4>Idade:</h4>
      <h4>Calorías diarias:</h4>
      <h4>Cantidade de auga diaria:</h4>
    </div>
    <div class="calculador"></div>
  </div>
</template>

<style scoped>
/* Aseguramos que el body y el html tengan 100% de altura */
html,
body {
  height: 100%;
  margin: 0;
}

.container {
  height: 80%; /* La altura del contenedor principal es 100% */
  display: flex;
  flex-direction: column;
}

.datos {
  flex: 1; /* Esto hace que el div ocupe todo el espacio disponible */
  width: 97%;
  padding: 10px;
  box-sizing: border-box;
  background-color: white;
  border-radius: 5%;
  display: flex;
  flex-direction: column; /* Organiza los elementos verticalmente */
  justify-content: flex-start; /* Alinea el contenido al principio */
  margin-right: 20px;
  margin-left: 20px; /* Añade un margen izquierdo para simetría */
  gap: 10px; /* Añade espacio entre los elementos dentro de .datos */
}

/* Estilo adicional para el contenedor principal */
h1 {
  color: #333;
}
</style>
