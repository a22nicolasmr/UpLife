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
      attrs: [],
      valorMedallas: [
        {
          id_medalla: 4,
          completado: true,
        },
      ],
      advertencias: {
        tarefas: false,
        exercicios: false,
        comidas: false,
        auga: false,
      },
    };
  },

  //cando se carga a vista, cargar as datas con tarefas
  mounted() {
    this.cargarDatasConTarefas();
    this.comprobarRachas();
    this.comprobarMedallas();
  },

  methods: {
    async comprobarMedallas() {
      await this.comprobarRachas();
      const valorMedallas = [];

      // Medalla 4
      valorMedallas.push({
        id_medalla: 4,
        completado: true,
      });
      // Medalla 5 - Racha saudable: comidas 7 días seguidos
      valorMedallas.push({
        id_medalla: 5,
        completado: this.rComidas >= 7,
      });

      // Medalla 6 - No camiño: exercicios 5 días na mesma semana
      valorMedallas.push({
        id_medalla: 6,
        completado: this.rExercicios >= 5,
      });

      // Medalla 7 - Máster da hidratación: auga 7 días seguidos
      valorMedallas.push({
        id_medalla: 7,
        completado: this.rAuga >= 7,
      });

      // Medalla 8 - Asasino de tarefas: tarefas 5 días seguidos
      valorMedallas.push({
        id_medalla: 8,
        completado: this.rTarefas >= 5,
      });

      // Medalla 9 - Semana perfecta: comidas, exercicios e auga 7 días seguidos
      valorMedallas.push({
        id_medalla: 9,
        completado:
          this.rComidas >= 7 && this.rExercicios >= 7 && this.rAuga >= 7,
      });

      // Medalla 10 - Rastreador consciente: idem anterior pero antes das 22:00
      // Esta necesitaría comprobación de hora exacta en rexistros -> non implementada aquí
      valorMedallas.push({
        id_medalla: 10,
        completado: false, // Placeholder, implementa se levas control de hora rexistro
      });

      // Medalla 11 - Plantillas: 3 plantillas creadas e usadas polo menos 2 veces cada unha
      try {
        const plantillaRes = await fetch(
          "https://uplife-4c0p.onrender.com/api/plantillas/"
        );
        const plantillas = await plantillaRes.json();

        // Filtra só as do usuario actual
        const usuarioStore = useUsuarioStore();
        const idUsuario = usuarioStore.id;

        const plantillasUsuario = plantillas.filter(
          (p) => p.usuario === idUsuario
        );

        // Contar cantas plantillas teñen polo menos 2 usos (2 datas diferentes)
        const usadasSuficiente = plantillasUsuario.filter((p) => {
          if (!p.usos || !Array.isArray(p.usos)) return false;
          const datasUsadas = p.usos.filter((u) => !!u.data);
          return datasUsadas.length >= 2;
        });

        const completado = usadasSuficiente.length >= 3;

        valorMedallas.push({
          id_medalla: 11,
          completado,
        });
      } catch (error) {
        console.error("Erro ao comprobar medalla de plantillas:", error);
        valorMedallas.push({
          id_medalla: 11,
          completado: false, // fallback se falla a consulta
        });
      }

      // Medalla 12 - Racha perfecta 90 días
      valorMedallas.push({
        id_medalla: 12,
        completado:
          this.rComidas >= 90 &&
          this.rExercicios >= 90 &&
          this.rAuga >= 90 &&
          this.rTarefas >= 90,
      });

      // Medalla 13 - Racha perfecta 365 días
      valorMedallas.push({
        id_medalla: 13,
        completado:
          this.rComidas >= 365 &&
          this.rExercicios >= 365 &&
          this.rAuga >= 365 &&
          this.rTarefas >= 365,
      });

      this.valorMedallas = valorMedallas;
      this.$emit("mandarRachas", this.valorMedallas);

      return valorMedallas;
    },
    //comprobar as rachas do usuario en función das datas anteriores a data actual
    // en tarefas tamén comproba se están completadas
    async comprobarRachas() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      const urls = [
        {
          key: "auga",
          var: "rAuga",
          url: "https://uplife-4c0p.onrender.com/api/auga/",
        },
        {
          key: "comidas",
          var: "rComidas",
          url: "https://uplife-4c0p.onrender.com/api/comidas/",
        },
        {
          key: "tarefas",
          var: "rTarefas",
          url: "https://uplife-4c0p.onrender.com/api/tarefas/",
        },
      ];

      // Reiniciar rachas
      this.rAuga = 0;
      this.rComidas = 0;
      this.rExercicios = 0;
      this.rTarefas = 0;

      // Procesar augas, comidas, tarefas
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
            item.key !== "tarefas" || entry.completado === true;

          return esUsuario && tieneFechaValida && estaCompletado;
        });

        const fechas = [...new Set(userData.map((entry) => entry.data))]
          .sort()
          .reverse();

        let racha = 0;
        let hoy = new Date().toISOString().split("T")[0];

        // Dentro del bucle for de urls (para auga, comidas, tarefas)
        const hayHoy = userData.some(
          (entry) => entry.data === new Date().toISOString().split("T")[0]
        );
        this.advertencias[item.key] = !hayHoy;

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

      // ✅ Calcular rExercicios usando ejercicios + plantillas
      try {
        const [resEx, resPl] = await Promise.all([
          fetch("https://uplife-4c0p.onrender.com/api/exercicios/"),
          fetch("https://uplife-4c0p.onrender.com/api/plantillas/"),
        ]);

        const [exercicios, plantillas] = await Promise.all([
          resEx.json(),
          resPl.json(),
        ]);

        const ejerciciosValidos = exercicios
          .filter(
            (e) =>
              e.usuario === idUsuario &&
              e.data &&
              e.data <= new Date().toISOString().split("T")[0]
          )
          .map((e) => e.data);

        const plantillasValidas = plantillas
          .filter(
            (p) =>
              p.usuario === idUsuario &&
              p.data &&
              p.data <= new Date().toISOString().split("T")[0]
          )
          .map((p) => p.data);

        const todasFechas = new Set([
          ...ejerciciosValidos,
          ...plantillasValidas,
        ]);
        const fechasUnicasOrdenadas = [...todasFechas].sort().reverse(); // más reciente a más antigua

        // Calcular racha consecutiva
        let rachaEx = 0;
        let hoy = new Date().toISOString().split("T")[0];

        const hayHoy = [...ejerciciosValidos, ...plantillasValidas].includes(
          new Date().toISOString().split("T")[0]
        );
        this.advertencias.exercicios = !hayHoy;

        for (const fecha of fechasUnicasOrdenadas) {
          if (fecha === hoy) {
            rachaEx++;
            hoy = new Date(new Date(hoy).getTime() - 86400000)
              .toISOString()
              .split("T")[0];
          } else {
            break;
          }
        }

        this.rExercicios = rachaEx;
      } catch (error) {
        console.error("Erro ao comprobar exercicios e plantillas:", error);
      }
    },
    //comprobar se hai tarefas para unha data
    async comprobarTarefasNaData(date) {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      try {
        const response = await fetch(
          `https://uplife-4c0p.onrender.com/api/tarefas/`
        );
        const tarefas = await response.json();

        const tarefasNaData = tarefas.filter(
          (t) =>
            t.usuario === idUsuario &&
            new Date(t.data).toDateString() === date.toDateString()
        );

        const todasCompletadas =
          tarefasNaData.length > 0 &&
          tarefasNaData.every((t) => t.completado === true);

        if (tarefasNaData.length === 0 || todasCompletadas) {
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
      const today = new Date();
      const todayISO = today.toISOString().split("T")[0];

      const todayAttr = {
        key: "today",
        highlight: {
          color: "#003366",
          fillMode: "solid",
        },
        dates: today,
        order: 100,
        customData: { esHoy: true },
      };

      const taskAttrs = datas
        .filter((date) => date !== todayISO)
        .map((date) => ({
          key: `task-${date}`,
          highlight: {
            color: "#add8e6",
            fillMode: "light",
          },
          dates: new Date(date),
          order: 1,
        }));

      this.attrs = [todayAttr, ...taskAttrs];
    },
    // obter as tarefas filtradas por usuario e data
    async cargarDatasConTarefas() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      try {
        const response = await fetch(
          `https://uplife-4c0p.onrender.com/api/tarefas/`
        );
        const tarefas = await response.json();

        const datasUnicas = [
          ...new Set(
            tarefas.filter((t) => t.usuario === idUsuario).map((t) => t.data)
          ),
        ];

        this.actualizarDatasConTarefas(datasUnicas);
        this.componenteActivo = "lista";
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
          <p v-if="advertencias.tarefas" class="advertencia">
            ✔ Fai unha tarefa!
          </p>
        </div>
        <div>
          <img src="/imaxes/task.png" alt="Icona tarefas" />
        </div>
      </div>

      <div id="exercicio">
        <div>
          <p>Racha de exercicios</p>
          <p>{{ rExercicios }}</p>
          <p v-if="advertencias.exercicios" class="advertencia">
            💪 Fai un exercicio hoxe!
          </p>
        </div>
        <div>
          <img src="/imaxes/exercise.png" alt="Icona exercicios" />
        </div>
      </div>

      <div id="comidas">
        <div>
          <p>Racha de comidas</p>
          <p>{{ rComidas }}</p>
          <p v-if="advertencias.comidas" class="advertencia">
            🍽️ Rexistra a túa comida!
          </p>
        </div>
        <div>
          <img src="/imaxes/diet.png" alt="Icona comidas" />
        </div>
      </div>

      <div id="auga">
        <div>
          <p>Racha de auga</p>
          <p>{{ rAuga }}</p>
          <p v-if="advertencias.auga" class="advertencia">
            💧 Rexistra a túa auga!
          </p>
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
          :key="attrs.length"
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
          @comprobarRachas="comprobarRachas"
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
  height: 60vh;
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
  margin-bottom: 0;
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
.vc-weeks {
  margin-top: 5%;
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
</style>
