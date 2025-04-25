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
      tarefasPorData: {},
    };
  },
  watch: {
    dataSeleccionada: {
      immediate: true,
      handler(novaData) {
        this.cargarTarefas(novaData).then(() => {
          const dataISO = new Date(novaData).toLocaleDateString("en-CA");
          this.$nextTick(() => {
            const el = this.$refs["data-" + dataISO];
            const target = Array.isArray(el) ? el[0] : el;

            if (target && scrollContainer) {
              const targetRect = target.getBoundingClientRect();
              const containerRect = scrollContainer.getBoundingClientRect();
              const offset =
                targetRect.top - containerRect.top + scrollContainer.scrollTop;

              scrollContainer.scrollTo({ top: offset, behavior: "smooth" });
            }
          });
        });
      },
    },
  },
  methods: {
    scrollAtaData(data) {
      this.$nextTick(() => {
        const dataISO = new Date(data).toLocaleDateString("en-CA");
        const refs = this.$refs["data-" + dataISO];
        const scrollContainer = this.$refs.scrollArea;

        const bloque = Array.isArray(refs) ? refs[0] : refs;

        if (bloque && scrollContainer) {
          const bloqueRect = bloque.getBoundingClientRect();
          const containerRect = scrollContainer.getBoundingClientRect();

          const offset =
            bloqueRect.top - containerRect.top + scrollContainer.scrollTop;

          scrollContainer.scrollTo({
            top: offset,
            behavior: "smooth",
          });
        }
      });
    },

    async cargarTarefas(data) {
      if (!data) return;
      const dataISO = new Date(data).toLocaleDateString("en-CA");

      try {
        const response = await fetch(
          `http://localhost:8001/api/tarefas/?data=${dataISO}`
        );

        if (!response.ok) throw new Error("Erro ao cargar tarefas");
        const tarefas = await response.json();

        const agrupadas = {};
        for (const tarefa of tarefas) {
          if (!agrupadas[tarefa.data]) agrupadas[tarefa.data] = [];
          agrupadas[tarefa.data].push(tarefa);
        }

        this.tarefasPorData = agrupadas;
      } catch (error) {
        console.error("Erro cargando tarefas:", error);
      }
    },

    async borrarTarefa(id) {
      try {
        await fetch(`http://localhost:8001/api/tarefas/${id}/`, {
          method: "DELETE",
        });

        for (const data in this.tarefasPorData) {
          this.tarefasPorData[data] = this.tarefasPorData[data].filter(
            (t) => t.id_tarefa !== id
          );

          // Si después de filtrar el array está vacío, lo eliminamos del objeto
          if (this.tarefasPorData[data].length === 0) {
            delete this.tarefasPorData[data];
          }
        }
      } catch (error) {
        console.error("Erro ao borrar tarefa:", error);
      }
    },

    async marcarCompletado(tarefa) {
      try {
        const updated = { completado: !tarefa.completado };
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

    formatoData(dataISO) {
      const [ano, mes, dia] = dataISO.split("-");
      return `${dia}/${mes}/${ano}`;
    },
  },
};
</script>

<template>
  <div class="lista-container">
    <h2 class="data-header">Tarefas pendentes</h2>

    <div class="scroll-area" ref="scrollArea">
      <div v-if="Object.keys(tarefasPorData).length > 0">
        <div
          v-for="(tarefas, data) in tarefasPorData"
          :key="data"
          :ref="'data-' + data"
        >
          <h3 class="data-header">{{ formatoData(data) }}</h3>
          <ul>
            <li
              v-for="tarefa in tarefas"
              :key="tarefa.id_tarefa"
              class="tarefa-item"
            >
              <input
                type="checkbox"
                :checked="tarefa.completado"
                @change="marcarCompletado(tarefa)"
              />
              <span :class="{ feito: tarefa.completado }">
                {{ tarefa.hora?.slice(0, 5) || "--:--" }} - {{ tarefa.titulo }}
              </span>
              <button @click="borrarTarefa(tarefa.id_tarefa)">
                <img src="/imaxes/trash.png" alt="borrar" />
              </button>
            </li>
          </ul>
        </div>
      </div>
      <p v-else>Non hai tarefas para esta data.</p>
    </div>
  </div>
</template>

<style scoped>
.lista-container {
  color: white;
  background-color: black;
  padding: 20px;
  border-radius: 12px;
  max-height: 400px;
  overflow: hidden;
}

.scroll-area {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 10px;
}

.data-header {
  color: #7f5af0;
  margin-top: 15px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
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
