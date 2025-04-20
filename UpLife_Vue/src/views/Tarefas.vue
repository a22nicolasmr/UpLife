<script>
import ListaTarefas from "@/components/ListaTarefas.vue";
import EngadirTarefas from "@/components/EngadirTarefas.vue";
export default {
  components: {
    ListaTarefas,
    EngadirTarefas,
  },
  data() {
    return {
      componenteActivo: "lista",
    };
  },
};
</script>

<template>
  <div class="tarxetas-container">
    <h1>Tarefas</h1>

    <!-- Tarjetas de selección -->
    <div class="tarxetas">
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'lista' }"
        @click="componenteActivo = 'lista'"
      >
        Ver tarefas
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadir' }"
        @click="componenteActivo = 'engadir'"
      >
        Engadir tarefa
      </div>
    </div>

    <!-- Mostramos o compoñente activo -->
    <div class="compoñente-activo">
      <ListaTarefas v-if="componenteActivo === 'lista'" />
      <EngadirTarefas v-if="componenteActivo === 'engadir'" />
    </div>
  </div>
</template>

<style scoped>
.tarxetas-container {
  text-align: center;
  padding: 20px;
}

.tarxetas {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.tarxeta {
  background-color: #4880ff;
  color: white;
  padding: 20px 30px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.inactiva {
  background-color: #d8d8d8;
  color: white;
}

.compoñente-activo {
  margin-top: 20px;
}
</style>
