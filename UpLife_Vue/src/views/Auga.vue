<script>
import EngadirAuga from "@/components/Auga/EngadirAuga.vue";
import HistorialAuga from "@/components/Auga/HistorialAuga.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    HistorialAuga,
    EngadirAuga,
  },
  data() {
    return {
      componenteActivo: "historial",
      augaHoxe: [],
      editando: { id: null, campo: null, valor: "" },
    };
  },

  computed: {
    // cargar o id a data de hoxe e a auga necesaria polo usuario
    idUsuario() {
      return useUsuarioStore().id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
    augaTotalNecesaria() {
      return useUsuarioStore().auga;
    },

    //calcular o total de auga inxerida o día de hoxe
    augaInxeridaHoxe() {
      return this.augaHoxe.reduce((total, a) => total + a.cantidade, 0);
    },

    //calcular porcentaxe de auga en función a auga necesitada e a auga inxerida
    porcentaxeAuga() {
      const total = this.augaTotalNecesaria;
      const inxerida = this.augaInxeridaHoxe;

      if (!total || total <= 0) return 0;

      return Math.min(Math.round((inxerida / total) * 100), 100);
    },
  },
  mounted() {
    this.cargarAugaHoxe();
  },
  methods: {
    activarEdicion(id, campo) {
      const entrada = this.augaHoxe.find((a) => a.id_auga === id);
      if (!entrada) return;

      this.editando = { id, campo, valor: entrada[campo] };

      this.$nextTick(() => {
        const ref = this.$refs[`editInput-${id}-${campo}`];
        if (ref && ref.focus) ref.focus();
      });
    },
    async guardarCampoEditado(id, campo) {
      const novoValor = this.editando.valor;
      this.editando = { id: null, campo: null, valor: "" };
      try {
        await fetch(`https://uplife-4c0p.onrender.com/api/auga/${id}/`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ [campo]: novoValor }),
        });
        this.cargarAugaHoxe();
        this.$refs.filloAuga.cargarAuga();
      } catch (error) {
        console.error("Erro ao actualizar rexistro de auga:", error);
      }
    },
    //cargar a auga inxerida na fecha actual
    async cargarAugaHoxe() {
      try {
        const response = await fetch(
          "https://uplife-4c0p.onrender.com/api/auga/"
        );
        if (!response.ok) throw new Error("Erro ao cargar auga");

        const auga = await response.json();
        this.augaHoxe = auga.filter(
          (ex) => ex.usuario === this.idUsuario && ex.data === this.dataHoxeISO
        );

        // const seteDiasAtras = new Date();
        // seteDiasAtras.setDate(seteDiasAtras.getDate() - 7);

        // const augaBorrar = auga.filter((e) => {
        //   if (!e.data) return false;
        //   const dataAuga = new Date(e.data);
        //   return dataAuga < seteDiasAtras;
        // });

        // augaBorrar.forEach((e) => {
        //   this.eliminarAuga(e.id_auga);
        // });
        this.$refs.filloAuga.cargarAuga();
      } catch (error) {
        console.error("Erro cargando auga:", error);
      }
    },
    //eliminar rexistros de auga
    async eliminarAuga(id) {
      try {
        const response = await fetch(
          `https://uplife-4c0p.onrender.com/api/auga/${id}/`,
          {
            method: "DELETE",
          }
        );
        if (!response.ok) throw new Error("Erro ao eliminar auga");

        this.augaHoxe = this.augaHoxe.filter((ex) => ex.id_auga !== id);
        this.cargarAugaHoxe();
        this.$refs.filloAuga.cargarAuga();
      } catch (error) {
        console.error("Erro eliminando auga:", error);
      }
    },
  },
};
</script>

<template>
  <div id="divXeral2">
    <h1 class="titulo">Auga</h1>

    <div class="tarxetas">
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'historial' }"
        @click="componenteActivo = 'historial'"
      >
        Historial
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadirA' }"
        @click="componenteActivo = 'engadirA'"
      >
        Engadir auga
      </div>
    </div>

    <div class="auga-layout">
      <div class="esquerda">
        <!-- GRÁFICO DE PROGRESO -->
        <div class="grafico-auga">
          <svg viewBox="0 0 36 36" class="circular-chart">
            <path
              class="circle-bg"
              d="M18 2.0845
                 a 15.9155 15.9155 0 0 1 0 31.831
                 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              class="circle"
              :stroke-dasharray="porcentaxeAuga + ', 100'"
              d="M18 2.0845
                 a 15.9155 15.9155 0 0 1 0 31.831
                 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <text x="18" y="20.35" class="percentage">
              {{ porcentaxeAuga }}%
            </text>
          </svg>
          <div class="info-auga">
            <p>
              <strong>Auga restante:</strong>
              {{ augaTotalNecesaria - augaInxeridaHoxe }} ml
            </p>
            <p><strong>Auga inxerida:</strong> {{ augaInxeridaHoxe }} ml</p>
          </div>
        </div>

        <div class="esquerdaAbaixo">
          <table>
            <thead>
              <tr>
                <th>Cantidade(ml)</th>
                <th>Hora</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="auga in augaHoxe" :key="auga.id_auga">
                <td @click="activarEdicion(auga.id_auga, 'cantidade')">
                  <input
                    :ref="`editInput-${auga.id_auga}-cantidade`"
                    v-if="
                      editando.id === auga.id_auga &&
                      editando.campo === 'cantidade'
                    "
                    type="number"
                    v-model.number="editando.valor"
                    @blur="guardarCampoEditado(auga.id_auga, 'cantidade')"
                    @keyup.enter="
                      guardarCampoEditado(auga.id_auga, 'cantidade')
                    "
                    @click.stop
                  />
                  <span v-else>{{ auga.cantidade }}</span>
                </td>
                <td @click="activarEdicion(auga.id_auga, 'hora')">
                  <input
                    :ref="`editInput-${auga.id_auga}-hora`"
                    v-if="
                      editando.id === auga.id_auga && editando.campo === 'hora'
                    "
                    type="time"
                    v-model="editando.valor"
                    @blur="guardarCampoEditado(auga.id_auga, 'hora')"
                    @keyup.enter="guardarCampoEditado(auga.id_auga, 'hora')"
                    @click.stop
                  />
                  <span v-else>{{ auga.hora }}</span>
                </td>

                <td>
                  <img
                    src="/imaxes/trash.png"
                    alt="icona borrar"
                    @click="eliminarAuga(auga.id_auga)"
                  />
                </td>
              </tr>
              <tr v-if="augaHoxe.length === 0">
                <td colspan="3">Non hai rexistros de auga para hoxe.</td>
              </tr>
            </tbody>
          </table>
          <button @click="componenteActivo = 'engadirA'" id="engadirA">
            +
          </button>
        </div>
      </div>

      <div class="dereita">
        <HistorialAuga
          v-if="componenteActivo === 'historial'"
          @cargarAugaHoxe="cargarAugaHoxe"
          ref="filloAuga"
        />
        <EngadirAuga
          v-if="componenteActivo === 'engadirA'"
          @cargarAugaHoxe="cargarAugaHoxe"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
#divXeral2 {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
}

.titulo {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
  margin-bottom: 2%;
  color: #7f5af0;
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

.auga-layout {
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

.esquerda {
  width: 60%;
  padding: 2%;
  overflow-y: auto;
}

.dereita {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
  overflow-y: auto;
}

.grafico-auga {
  display: flex;
  align-items: center;
  gap: 5%;
  justify-content: left;
  margin-bottom: 3%;
}

.circular-chart {
  max-width: 15%;
  max-height: 15%;
}

.circle-bg {
  fill: none;
  stroke: #eee;
  stroke-width: 3.8;
}

.circle {
  fill: none;
  stroke: #4880ff;
  stroke-width: 3.8;
  stroke-linecap: round;
  transform: rotate(-90deg);
  transform-origin: center;
  transition: stroke-dasharray 0.5s;
}

.percentage {
  fill: #4880ff;
  font-size: x-small;
  text-anchor: middle;
}

.info-auga p {
  margin: 2px 0;
  color: #666;
  font-size: large;
}

table {
  width: 96%;
  border-collapse: collapse;
  background-color: #d8d8d8;
  color: black;
  border-radius: 8px;

  overflow: hidden;
}

th,
td {
  padding: 2%;
  text-align: center;
  flex: 1;
}

thead {
  background-color: #7f5af0;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}

tbody tr {
  border-bottom: 1px solid #acacac;
}

tr {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

td[colspan="3"] {
  text-align: center;
  color: #aaa;
  font-style: italic;
}

button {
  margin-top: 3%;
  padding: 1%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 9%;
  height: 5%;
}

#engadirA {
  font-size: xx-large;
}
</style>
