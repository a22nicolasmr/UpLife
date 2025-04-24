<script>
export default {
  props: {
    dataSeleccionada: {
      type: Date,
      required: true,
    },
  },
  data() {
    return {
      tarefas: [],
    };
  },
  watch: {
    dataSeleccionada: {
      immediate: true,
      handler(novaData) {
        this.cargarTarefas(novaData);
      },
    },
  },
  methods: {
    async cargarTarefas(data) {
      if (!data) return;
      const dataISO = new Date(data).toISOString().split("T")[0];
      console.log(dataISO);

      try {
        const response = await fetch(
          `http://localhost:8001/api/tarefas/?data=${dataISO}`
        );
        if (!response.ok) throw new Error("Erro ao cargar tarefas");
        this.tarefas = await response.json();
      } catch (error) {
        console.error("Erro cargando tarefas:", error);
      }
    },

    async borrarTarefa(id) {
      try {
        await fetch(`http://localhost:8001/api/tarefas/${id}/`, {
          method: "DELETE",
        });
        this.tarefas = this.tarefas.filter((t) => t.id_tarefa !== id);
      } catch (error) {
        console.error("Erro ao borrar tarefa:", error);
      }
    },
    async marcarCompletado(tarefa) {
      try {
        const updated = {
          completado: !tarefa.completado,
        };
        const response = await fetch(
          `http://localhost:8001/api/tarefas/${tarefa.id_tarefa}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updated),
          }
        );
        if (!response.ok) throw new Error("Erro ao actualizar tarefa");
        tarefa.completado = !tarefa.completado;
      } catch (error) {
        console.error("Erro ao marcar como completada:", error);
      }
    },
  },
};
</script>

<template>
  <div class="lista-container">
    <h2>Tarefas do día</h2>
    <ul v-if="tarefas.length > 0">
      <li v-for="tarefa in tarefas" :key="tarefa.id_tarefa" class="tarefa-item">
        <input
          type="checkbox"
          :checked="tarefa.completado"
          @change="marcarCompletado(tarefa)"
        />
        <span :class="{ feito: tarefa.completado }"
          >{{ tarefa.hora || "--:--" }} - {{ tarefa.titulo }}</span
        >
        <button @click="borrarTarefa(tarefa.id_tarefa)">
          <img src="/imaxes/trash.png" alt="borrar" />
        </button>
      </li>
    </ul>
    <p v-else>Non hai tarefas para esta data.</p>
  </div>
</template>

<style scoped>
.lista-container {
  color: white;
  background-color: black;
  padding: 20px;
  border-radius: 12px;
}

h2 {
  color: #7f5af0;
}

ul {
  list-style: none;
  padding: 0;
}

.tarefa-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #222;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.tarefa-item span {
  flex: 1;
  margin-left: 10px;
}

.tarefa-item button {
  background: none;
  border: none;
  font-size: 18px;
  color: red;
  cursor: pointer;
}

.feito {
  text-decoration: line-through;
  color: #aaa;
}
</style>
