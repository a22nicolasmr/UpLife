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
      rTarefas: 0,
      rExercicios: 0,
      rComidas: 0,
      rAuga: 0,
      dataPasada: false,
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
    reenviarTarefasConHora(tarefas) {
      this.$emit("emitirDatasConTarefas", tarefas);
    },
    getFechasDeshabilitadas({ date }) {
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0);

      const comparar = new Date(date);
      comparar.setHours(0, 0, 0, 0);

      return comparar < hoy;
    },
    seleccionarData(dia) {
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0); // Elimina horas para comparar solo la fecha

      if (dia.date < hoy) return; // Evita selección si es día pasado

      this.dataSeleccionada = dia.date;

      this.$nextTick(() => {
        if (this.$refs.listaTarefasRef?.scrollAtaData) {
          this.$refs.listaTarefasRef.scrollAtaData(dia.date);
        }
      });
    },

    actualizarDatasConTarefas(datas) {
      const tarefasAttrs = datas.map((dataISO) => ({
        key: `tarefa-${dataISO}`,
        highlight: {
          color: "#add8e6", // azul claro
          fillMode: "outline",
        },
        dates: new Date(dataISO),
      }));

      this.attrs = [
        {
          key: "today",
          highlight: true,
          dates: new Date(),
        },
        ...tarefasAttrs,
      ];
    },
  },
  computed: {
    disabledDates() {
      return [
        {
          end: new Date(new Date().setDate(new Date().getDate() - 1)),
        },
      ];
    },
  },
};
</script>

<template>
  <div id="divXeral">
    <h1 class="titulo">Tarefas</h1>
    <div class="divsArriba">
      <div id="izquierda">
        <div>
          <p>Racha de tarefas</p>
          <p>{{ rTarefas }}</p>
        </div>
        <div>
          <img src="/imaxes/task.png" alt="Icona tarefas" />
        </div>
      </div>

      <div id="exercicio">
        <div>
          <p>Racha de exercicios</p>
          <p>{{ rExercicios }}</p>
        </div>
        <div>
          <img src="/imaxes/exercise.png" alt="Icona exercicios" />
        </div>
      </div>

      <div id="comidas">
        <div>
          <p>Racha de comidas</p>
          <p>{{ rComidas }}</p>
        </div>
        <div>
          <img src="/imaxes/diet.png" alt="Icona comidas" />
        </div>
      </div>

      <div id="auga">
        <div>
          <p>Racha de auga</p>
          <p>{{ rAuga }}</p>
        </div>
        <div>
          <img src="/imaxes/water-bottle.png" alt="Icona auga" />
        </div>
      </div>
    </div>

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

    <div class="tarefas-layout">
      <div class="calendario">
        <vc-calendar
          :attributes="attrs"
          @dayclick="seleccionarData"
          :min-date="new Date()"
          :disabled-dates="disabledDates"
        />
      </div>

      <div class="lateral">
        <ListaTarefas
          v-if="componenteActivo === 'lista'"
          ref="listaTarefasRef"
          :dataSeleccionada="dataSeleccionada"
          @datas-con-tarefas="reenviarTarefasConHora"
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
#izquierda,
#exercicio,
#auga,
#comidas {
  display: flex;
  padding: 1%;
  padding-right: 2%;
}
#izquierda p:nth-of-type(2),
#exercicio p:nth-of-type(2),
#auga p:nth-of-type(2),
#comidas p:nth-of-type(2) {
  font-size: x-large;
}
#divXeral {
  display: flex;
  flex-direction: column;
  height: 85%;
  overflow-y: auto;
  margin-left: 4%;
}

.divsArriba img {
  height: 8vh;
  width: 8vh;
  padding-top: 60%;
}
.divsArriba {
  display: flex;
  flex: 0.5;
  justify-content: space-between;
  margin-right: 4%;
  margin-bottom: 2%;
}
.divsArriba > div {
  background-color: white;
  border-radius: 5%;
}
.tarefas-wrapper {
  background-color: #f5f6f8;
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
  margin-left: 28.3%;
}

.tarxeta {
  background-color: #4880ff;
  color: white;
  padding: 12px 30px;
  border-radius: 1vh 1vh 0 0;
  cursor: pointer;
  font-weight: bold;
  font-size: medium;
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
  background-color: white;
  border-radius: 2%;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
}

/* Calendario */
.calendario {
  flex: 1;
  background-color: white;
  box-sizing: border-box;
}
h1 {
  display: flex;
  align-self: flex-start;
  font-size: 2vw;
  margin-bottom: 3vh;
  color: #7f5af0;
}
/* Compoñente lateral */
.lateral {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
}

/* v-calendar estilos */
.vc-container {
  width: 100% !important;
  font-size: 18px !important;
  padding: 2%;
  border: none !important;
}

.vc-week {
  padding-top: 3.5%;
}
.vc-weekdays {
  padding-top: 1%;
}
.vc-day-content {
  font-size: large !important;
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
