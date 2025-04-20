<script>
export default {};
</script>
<template>
  <nav>
    <li :class="{ activo: rutaActual === '/tarefas' }">Tarefas</li>
    <li>Exercicios</li>
    <li>Comidas</li>
    <li>Plantillas</li>
    <li>Auga</li>
    <li>Medallas</li>
    <li>Perfil</li>
    <li>Pechar sesión</li>
  </nav>
</template>
<style scoped>
nav {
  background-color: #333;
  padding: 10px;
  display: flex;
  justify-content: center;
}

ul {
  display: flex;
  list-style: none;
  gap: 20px;
}

li {
  padding: 10px;
  color: white;
  cursor: pointer;
}

li.activo {
  background-color: #4880ff;
  color: white;
  border-radius: 5px;
}

a {
  text-decoration: none;
  color: inherit;
}
</style>
