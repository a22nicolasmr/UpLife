<script>
import EngadirExercicioPlantilla from "@/components/EngadirExercicioPlantilla.vue";
import NovaPlantilla from "@/components/NovaPlantilla.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    NovaPlantilla,
    EngadirExercicioPlantilla,
  },
  data() {
    return {
      componenteActivo: "nova",
      plantillaHoxe: [],
    };
  },

  computed: {
    idUsuario() {
      return useUsuarioStore().id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
    plantillaTotalNecesaria() {
      return useUsuarioStore().plantilla;
    },
    plantillaInxeridaHoxe() {
      return this.plantillaHoxe.reduce((total, a) => total + a.cantidade, 0);
    },
    porcentaxeplantilla() {
      const total = this.plantillaTotalNecesaria;
      const inxerida = this.plantillaInxeridaHoxe;

      if (!total || total <= 0) return 0;

      return Math.min(Math.round((inxerida / total) * 100), 100);
    },
  },
  mounted() {
    // this.cargarplantillaHoxe();
  },
  methods: {
    // async cargarplantillaHoxe() {
    //   try {
    //     const response = await fetch("http://localhost:8001/api/plantilla/");
    //     if (!response.ok) throw new Error("Erro ao cargar plantilla");
    //     const plantilla = await response.json();
    //     this.plantillaHoxe = plantilla.filter(
    //       (ex) => ex.usuario === this.idUsuario && ex.data === this.dataHoxeISO
    //     );
    //   } catch (error) {
    //     console.error("Erro cargando plantilla:", error);
    //   }
    // },
    // async eliminarplantilla(id) {
    //   try {
    //     const response = await fetch(`http://localhost:8001/api/plantilla/${id}/`, {
    //       method: "DELETE",
    //     });
    //     if (!response.ok) throw new Error("Erro ao eliminar plantilla");
    //     this.plantillaHoxe = this.plantillaHoxe.filter((ex) => ex.id_plantilla !== id);
    //     window.location.reload();
    //   } catch (error) {
    //     console.error("Erro eliminando plantilla:", error);
    //   }
    // },
  },
};
</script>

<template>
  <div id="divXeral2">
    <h1 class="titulo">Plantillas</h1>

    <div class="tarxetas">
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'nova' }"
        @click="componenteActivo = 'nova'"
      >
        Nova
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadirE' }"
        @click="componenteActivo = 'engadirE'"
      >
        Engadir plantilla
      </div>
    </div>

    <div class="plantilla-layout">
      <div class="esquerda">
        <!-- GRÁFICO DE PROGRESO -->

        <div class="esquerdaAbaixo">
          <button @click="componenteActivo = 'engadirE'" id="engadirE">
            +
          </button>
        </div>
      </div>

      <div class="dereita">
        <NovaPlantilla v-if="componenteActivo === 'nova'" />
        <EngadirExercicioPlantilla v-if="componenteActivo === 'engadirE'" />
      </div>
    </div>
  </div>
</template>

<style scoped>
#divXeral2 {
  display: flex;
  flex-direction: column;
  height: 85%;
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

.plantilla-layout {
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: white;
  border-radius: 2%;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  height: 100%;
}

.esquerda {
  width: 60%;
  padding: 2%;
}

.dereita {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
}

.grafico-plantilla {
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

.info-plantilla p {
  margin: 2px 0;
  color: #666;
  font-size: large;
}

table {
  width: 96%;
  border-collapse: collapse;
  background-color: #d8d8d8;
  color: black;
  border-radius: 2%;
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

#engadirE {
  font-size: xx-large;
}
</style>
