<script>
import ListaTarefas from "@/components/Tarefas/ListaTarefas.vue";
import EngadirTarefas from "@/components/Tarefas/EngadirTarefas.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

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
  //cando se carga a vista, cargar as datas con tarefas
  mounted() {
    this.cargarDatasConTarefas();
    this.comprobarRachas();
  },

  methods: {
    //comprobar as rachas do usuario en función das datas anteriores a data actual
    // en tarefas tamén comproba se están completadas
    async comprobarRachas() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      const urls = [
        { key: "auga", var: "rAuga", url: "http://localhost:8001/api/auga/" },
        {
          key: "comidas",
          var: "rComidas",
          url: "http://localhost:8001/api/comidas/",
        },
        {
          key: "exercicios",
          var: "rExercicios",
          url: "http://localhost:8001/api/exercicios/",
        },
        {
          key: "tarefas",
          var: "rTarefas",
          url: "http://localhost:8001/api/tarefas/",
        },
      ];

      this.rAuga = 0;
      this.rComidas = 0;
      this.rExercicios = 0;
      this.rTarefas = 0;

      for (const item of urls) {
        const res = await fetch(item.url);
        const data = await res.json();

        const userData = data.filter((entry) => {
          const esUsuario = entry.usuario === idUsuario;
          const tieneFechaValida =
            entry.data &&
            entry.data.trim() !== "" &&
            entry.data <= new Date().toISOString().split("T")[0];
          const estaCompletado =
            item.key !== "tarefas" || entry.completado === true; // solo pedir completado si es tarefas

          return esUsuario && tieneFechaValida && estaCompletado;
        });

        const fechas = [...new Set(userData.map((entry) => entry.data))]
          .sort()
          .reverse();

        let racha = 0;
        let hoy = new Date().toISOString().split("T")[0];

        for (const fecha of fechas) {
          if (fecha === hoy) {
            racha++;
            hoy = new Date(new Date(hoy).getTime() - 86400000)
              .toISOString()
              .split("T")[0];
          } else {
            break;
          }
        }

        this[item.var] = racha;
      }
    },

    //comprobar se hai tarefas para unha data
    async comprobarTarefasNaData(date) {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      try {
        const response = await fetch(`http://localhost:8001/api/tarefas/`);
        const tarefas = await response.json();

        const tarefasNaData = tarefas.filter(
          (t) =>
            t.usuario === idUsuario &&
            new Date(t.data).toDateString() === date.toDateString()
        );

        if (tarefasNaData.length === 0) {
          this.componenteActivo = "engadir";
        } else {
          this.componenteActivo = "lista";
        }
      } catch (error) {
        console.error("Erro ao comprobar tarefas na data", error);
      }
    },

    //enviar as tarefas que teñen hora
    reenviarTarefasConHora(tarefas) {
      this.$emit("emitirDatasConTarefas", tarefas);
    },

    // obter fechas deshabilitadas
    getFechasDeshabilitadas({ date }) {
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0);

      const comparar = new Date(date);
      comparar.setHours(0, 0, 0, 0);

      return comparar < hoy;
    },

    //seleccionar data no calendario
    seleccionarData(dia) {
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0); // eliminar horas para comparar só a data

      if (dia.date < hoy) return;

      this.dataSeleccionada = dia.date;
      this.comprobarTarefasNaData(this.dataSeleccionada);

      // scrollear ata as tarefas da data seleccionada
      this.$nextTick(() => {
        if (this.$refs.listaTarefasRef?.scrollAtaData) {
          this.$refs.listaTarefasRef.scrollAtaData(dia.date);
        }
      });
    },

    // os días que teñan tarefas serán marcados cunha cor azul claro usando attrs de vc-calendar
    actualizarDatasConTarefas(datas) {
      const tarefasAttrs = datas.map((dataISO) => {
        const date = new Date(dataISO);
        const isToday = date.toDateString() === new Date().toDateString();

        return {
          key: `tarefa-${dataISO}`,
          highlight: {
            color: isToday ? "#003366" : "#add8e6", // azul escuro se é hoxe
            fillMode: "light",
          },
          dates: date,
        };
      });

      // Eliminar posibles duplicados para hoxe
      const xaExisteToday = tarefasAttrs.some(
        (attr) =>
          new Date(attr.dates).toDateString() === new Date().toDateString()
      );

      if (!xaExisteToday) {
        tarefasAttrs.push({
          key: "today",
          highlight: {
            color: "#003366", // azul máis escuro
            fillMode: "light",
          },
          dates: new Date(),
        });
      }

      this.attrs = tarefasAttrs;
    },

    // obter as tarefas filtradas por usuario e data
    async cargarDatasConTarefas() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      try {
        const response = await fetch(`http://localhost:8001/api/tarefas/`);
        const tarefas = await response.json();

        const datasUnicas = [
          ...new Set(
            tarefas.filter((t) => t.usuario === idUsuario).map((t) => t.data)
          ),
        ];

        this.actualizarDatasConTarefas(datasUnicas);
      } catch (error) {
        console.error("Erro ao cargar datas con tarefas", error);
      }
    },
  },
  computed: {
    // deshabilitar todas aquelas datas por debaixo da data de hoxe
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
          @cargarDatasConTarefas="cargarDatasConTarefas"
        />

        <EngadirTarefas
          v-if="componenteActivo === 'engadir'"
          :dataSeleccionada="dataSeleccionada"
          @cargarDatasConTarefas="cargarDatasConTarefas"
          @comprobarRachas="comprobarRachas"
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
  min-height: 100%; /* Esto cubre la ventana completa */
  box-sizing: border-box; /* <-- Muy útil si usas paddings/margins */
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
  border-radius: 8px;
}
.tarefas-wrapper {
  background-color: #f5f6f8;
}

.titulo {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
  margin-bottom: 2%;
}

.tarxetas {
  display: flex;
  justify-content: center;
}

.tarxeta {
  background-color: #4880ff;
  color: white;
  padding: 1% 2%;
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
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.tarefas-layout {
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: white;
  border-radius: 8px;

  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  height: 100%;
  margin-bottom: 2%;
}

/* Calendario */
.calendario {
  display: flex;
  flex: 1;
  background-color: white;
  box-sizing: border-box;
}
h1 {
  display: flex;
  align-self: flex-start;
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
  font-size: medium !important;
  padding: 2%;
  border: none !important;
  height: 100%;
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
  border-radius: 8px;

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
