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
        <li>
          <img src="/imaxes/Logo.PNG" alt="UpLife" />
        </li>
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
/* Ajustar la barra de navegación para que el tamaño no cambie al cambiar de vista */
/* Barra de navegación (nav) */
nav {
  background-color: white;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  height: 96vh;
  min-width: 180px;
  border-right: 1px solid #ccc;
  position: fixed; /* Fija la barra de navegación */
  width: 180px;
}

/* Menú superior que ocupará el espacio restante */
.menu-superior {
  flex-grow: 1; /* Hace que ocupe el espacio disponible */
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Menú inferior */
.menu-inferior {
  display: flex;
  flex-direction: column;
  margin-top: auto; /* Esto asegura que se quede en el fondo */
}

/* Estilos generales de la lista (ul) */
ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  align-items: center;
}

/* Estilos de cada elemento de la lista (li) */
li {
  padding: 10px;
  color: black;
  cursor: pointer;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  transition: background-color 0.3s;
}

/* Estado de los elementos activos */
li.activo {
  color: white;
  background-color: #4880ff;
  padding-left: 40px;
  padding-right: 40px;
}

/* Línea horizontal */
hr {
  margin: 10px 0;
  border: none;
  border-top: 1px solid #ccc;
}
</style>
