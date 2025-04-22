<script setup>
import { useUsuarioStore } from "@/stores/useUsuario";
import { onMounted, watch } from "vue";
import { useRoute } from "vue-router";

const usuarioStore = useUsuarioStore();
const route = useRoute();

watch(
  () => route.query.nome,
  (novoNome) => {
    if (novoNome) usuarioStore.cargarUsuario(novoNome);
  },
  { immediate: true }
);
</script>

<template>
  <div class="barra-superior">
    <div class="usuario-info">
      <img :src="usuarioStore.imagen" alt="Usuario" class="usuario-imagen" />
      <div class="usuario-nombre" @click="$router.push('/perfil')">
        {{ usuarioStore.nome }}
      </div>
      <div class="usuario-medallas" @click="$router.push('/medallas')">
        {{ usuarioStore.medallas }} Medallas
      </div>
    </div>
  </div>
</template>

<style scoped>
.barra-superior {
  background-color: #4880ff; /* Azul */
  color: white;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  position: fixed;
  top: 0;
  left: 200px; /* Alineado con la barra lateral, ajusta según el ancho de tu barra lateral */
  width: calc(
    100% - 200px
  ); /* Asegura que la barra superior ocupe todo el espacio menos la barra lateral */
  z-index: 1000;
}

.usuario-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 20px;
  margin-right: 20px;
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
