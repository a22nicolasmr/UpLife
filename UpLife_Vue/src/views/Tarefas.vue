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
      dataSeleccionada: new Date(),
      attrs: [
        {
          key: "today",
          highlight: true,
          dates: new Date(),
        },
      ],
    };
  },
  methods: {
    seleccionarData(dia) {
      this.dataSeleccionada = dia.date;

      this.$nextTick(() => {
        if (this.$refs.listaTarefasRef?.scrollAtaData) {
          this.$refs.listaTarefasRef.scrollAtaData(dia.date);
        }
      });
    },
  },
};
</script>

<template>
  <div class="tarefas-wrapper">
    <h1 class="titulo">Tarefas</h1>

    <!-- Selector de pestañas -->
    <div class="tarxetas">
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'lista' }"
        @click="componenteActivo = 'lista'"
      >
        Lista
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadir' }"
        @click="componenteActivo = 'engadir'"
      >
        Engadir
      </div>
    </div>

    <!-- Layout calendario + sección lateral -->
    <div class="tarefas-layout">
      <div class="calendario">
        <vc-calendar :attributes="attrs" @dayclick="seleccionarData" />
      </div>

      <div class="lateral">
        <ListaTarefas
          v-if="componenteActivo === 'lista'"
          ref="listaTarefasRef"
          :dataSeleccionada="dataSeleccionada"
        />
        <EngadirTarefas
          v-if="componenteActivo === 'engadir'"
          :dataSeleccionada="dataSeleccionada"
        />
      </div>
    </div>
  </div>
</template>

<style>
.tarefas-wrapper {
  padding: 40px;
  background-color: #f5f6f8;
  min-height: 100vh;
}

.titulo {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 30px;
}

.tarxetas {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.tarxeta {
  background-color: #4880ff;
  color: white;
  padding: 12px 30px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  transition: 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.inactiva {
  background-color: #d8d8d8;
  color: #fff;
}

.tarefas-layout {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 0;
  margin: 0 auto;
  max-width: 1100px;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

/* Calendario */
.calendario {
  flex: 1;
  padding: 30px;
  background-color: white;
  border-right: 1px solid #eee;
  box-sizing: border-box;
}

/* Compoñente lateral */
.lateral {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  padding: 30px;
  box-sizing: border-box;
}

/* v-calendar estilos */
.vc-container {
  width: 100% !important;
  font-size: 18px !important;
}

.vc-pane {
  min-height: 420px;
}
.vc-week {
  padding-top: 25px;
}
.vc-weekdays {
  padding-top: 25px;
}
.vc-day-content {
  font-size: large !important;
  height: 48px;
  width: 48px;
  margin: 5 auto !important;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition: background-color 0.3s, transform 0.2s;
}

.vc-day-content.is-today {
  background-color: #4880ff;
  color: white;
  font-weight: bold;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.vc-day-content.is-selected {
  background-color: #00b4d8;
  color: white;
  font-weight: bold;
}
</style>
