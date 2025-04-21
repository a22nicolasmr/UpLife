<script>
export default {
  computed: {
    rutaActual() {
      return this.$route.path;
    },
  },
};
</script>

<template>
  <nav>
    <div class="menu-superior">
      <ul>
        <li
          :class="{ activo: rutaActual === '/tarefas' }"
          @click="$router.push('/tarefas')"
        >
          Tarefas
        </li>
        <li
          :class="{ activo: rutaActual === '/exercicios' }"
          @click="$router.push('/exercicios')"
        >
          Exercicios
        </li>
        <li
          :class="{ activo: rutaActual === '/comidas' }"
          @click="$router.push('/comidas')"
        >
          Comidas
        </li>
        <li
          :class="{ activo: rutaActual === '/plantillas' }"
          @click="$router.push('/plantillas')"
        >
          Plantillas
        </li>
        <li
          :class="{ activo: rutaActual === '/auga' }"
          @click="$router.push('/auga')"
        >
          Auga
        </li>
        <li
          :class="{ activo: rutaActual === '/medallas' }"
          @click="$router.push('/medallas')"
        >
          Medallas
        </li>
      </ul>
    </div>

    <div class="menu-inferior">
      <hr />
      <ul>
        <li
          :class="{ activo: rutaActual === '/perfil' }"
          @click="$router.push('/perfil')"
        >
          Perfil
        </li>
        <li
          :class="{ activo: rutaActual === '/formularios/rexistro' }"
          @click="$router.push('/formularios/rexistro')"
        >
          Pechar sesión
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
nav {
  background-color: white;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  min-width: 180px;
  border-right: 1px solid #ccc;
  position: relative; /* Añadido para mejor control */
}

.menu-superior {
  height: calc(100% - 120px); /* Restamos el espacio del menú inferior */
}

.menu-inferior {
  position: absolute;
  bottom: 60px;
  left: 10px;
  right: 10px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center; /* Centra los elementos */
  align-items: center; /* Centra los elementos */
}

li {
  padding: 10px;
  color: black;
  cursor: pointer;
  border-radius: 5px;
  display: flex;
  justify-content: center; /* Centra el contenido de cada li */
  transition: background-color 0.3s; /* Transición para suavizar el cambio de color */
}

li.activo {
  color: white;
  background-color: #4880ff;
  padding-left: 40px; /* Añadimos más espacio a la izquierda */
  padding-right: 40px; /* Añadimos más espacio a la derecha */
}

hr {
  margin: 10px 0;
  border: none;
  border-top: 1px solid #ccc;
}
</style>
