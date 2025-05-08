<script>
import EngadirExercicioPlantilla from "@/components/Plantillas/EngadirExercicioPlantilla.vue";
import NovaPlantilla from "@/components/Plantillas/NovaPlantilla.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    NovaPlantilla,
    EngadirExercicioPlantilla,
  },
  data() {
    return {
      componenteActivo: "nova",
      plantillas: [],
      expandedPlantillas: [],
      plantillaSeleccionada: null, // Nueva propiedad para gestionar la plantilla seleccionada
      plantillaSeleccionadaMandar: null, // Nueva propiedad para gestionar la plantilla seleccionada
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
    this.cargarDatos();
  },
  methods: {
    async cargarDatos() {
      try {
        const usuarioStore = useUsuarioStore();
        const idUsuario = usuarioStore.id;
        const response = await fetch("http://localhost:8001/api/plantillas/");

        if (!response.ok) throw new Error("Erro ao cargar plantillas");
        const plantillas = await response.json();

        // Inicializamos 'exercicios' en caso de que no exista
        this.plantillas = plantillas
          .filter((p) => p.usuario === idUsuario)
          .map((p) => ({ ...p, exercicios: p.exercicios || [] }));
      } catch (error) {
        console.error("Erro cargando datos:", error);
      }
    },
    async borrarPlantilla(id) {
      try {
        const response = await fetch(
          `http://localhost:8001/api/plantillas/${id}/`,
          { method: "DELETE" }
        );

        if (!response.ok) {
          throw new Error("Erro ao eliminar a plantilla");
        }

        // Actualizamos el estado sin necesidad de recargar la página
        this.plantillas = this.plantillas.filter((p) => p.id_plantilla !== id);
      } catch (error) {
        console.error("❌ Erro eliminando plantilla:", error);
      }
    },
    toggleExpand(id) {
      if (this.expandedPlantillas.includes(id)) {
        this.expandedPlantillas = this.expandedPlantillas.filter(
          (pid) => pid !== id
        );
      } else {
        this.expandedPlantillas.push(id);
      }
    },
    async borrarExercicio(idExercicio) {
      try {
        const response = await fetch(
          `http://localhost:8001/api/exercicios/${idExercicio}/`,
          { method: "DELETE" }
        );

        if (!response.ok) {
          throw new Error("Erro ao eliminar exercicio");
        }

        this.plantillas.forEach((p) => {
          p.exercicios = p.exercicios.filter(
            (e) => e.id_exercicio !== idExercicio
          );
        });
      } catch (error) {
        console.error("❌ Erro eliminando exercicio:", error);
      }
    },
  },
};
</script>

<
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
        Engadir
      </div>
    </div>

    <div class="plantilla-layout">
      <div class="esquerda">
        <h1>Lista de plantillas</h1>
        <div
          v-for="plantilla in plantillas"
          :key="plantilla.id_plantilla"
          class="divPlantilla"
        >
          <div class="plantilla-header">
            <img :src="plantilla.icona" alt="icona plantilla" />
            <h3>{{ plantilla.nome }}</h3>
            <div class="botons-container">
              <button
                class="expand-button"
                @click.stop="toggleExpand(plantilla.id_plantilla)"
                :class="{
                  rotated: expandedPlantillas.includes(plantilla.id_plantilla),
                }"
              >
                ▼
              </button>
              <button
                class="button-add"
                @click="
                  componenteActivo = 'engadirE';
                  this.plantillaSeleccionadaMandar = plantilla.id_plantilla;
                "
              >
                +
              </button>
              <img
                src="/imaxes/trash.png"
                alt="icona borrar"
                class="icono-trash"
                @click="borrarPlantilla(plantilla.id_plantilla)"
              />
            </div>
          </div>

          <transition name="fade-slide">
            <div
              v-if="expandedPlantillas.includes(plantilla.id_plantilla)"
              class="exercicios-plantilla"
            >
              <template
                v-if="plantilla.exercicios && plantilla.exercicios.length"
              >
                <div
                  v-for="ex in plantilla.exercicios"
                  :key="ex.id_exercicio"
                  class="exercicio"
                >
                  <span
                    >{{ ex.nome }} - {{ ex.repeticions }} -
                    {{ ex.peso }}kg</span
                  >
                  <img
                    src="/imaxes/trash.png"
                    alt="borrar exercicio"
                    class="icono-borrar-ex"
                    @click="borrarExercicio(ex.id_exercicio)"
                  />
                </div>
              </template>
              <p v-else class="sen-exercicios">
                Esta plantilla non ten exercicios.
              </p>
            </div>
          </transition>
        </div>
        <button @click="componenteActivo = 'nova'" id="engadirE">+</button>
      </div>

      <div class="dereita">
        <NovaPlantilla v-if="componenteActivo === 'nova'" />
        <EngadirExercicioPlantilla
          v-if="componenteActivo === 'engadirE'"
          :plantillaSeleccionadaMandar="plantillaSeleccionadaMandar"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.plantilla-header img:first-child {
  background-color: white;
  border-radius: 8px;
}
.button {
  background-color: #d8d8d8;
  color: #7f5af0;
  font-size: xx-large;
  display: flex;
  justify-self: center;
}

.expand-button {
  font-size: medium;
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  transition: transform 0.3s ease;
  display: flex;
  justify-content: right;
  transform-origin: center;
  width: 3%;
}

.expand-button.rotated {
  transform: rotate(180deg);
}

.divPlantilla {
  background-color: #d8d8d8;
  border-radius: 8px;

  margin-bottom: 2%;
  padding: 1%;
  display: flex;
  flex-direction: column;
  position: relative;
  box-sizing: border-box;
}

.plantilla-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  box-sizing: border-box;
  width: 100%;
}

.plantilla-header img:first-child {
  height: 8%;
  width: 8%;
}

#divXeral2 {
  display: flex;
  flex-direction: column;
  height: 85%;
  overflow: hidden;
}

.titulo {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
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
  border-radius: 8px;

  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  flex-grow: 1;
  height: calc(100vh - 30vh);
  overflow: hidden;
}

.esquerda {
  width: 60%;
  padding: 2%;
  box-sizing: border-box;
  height: 100%;
  overflow-y: auto;
}

.dereita {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
}

button {
  margin-top: 3%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 9%;
}

#engadirE {
  font-size: xx-large;
}

.exercicios-plantilla {
  width: 100%;
  margin-top: 1%;
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 8px;
  box-sizing: border-box;
  overflow: hidden;
}

.exercicio {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
  color: black;
  padding: 4px 0;
  box-sizing: border-box;
}

.sen-exercicios {
  font-style: italic;
  color: #777;
}

.icono-borrar-ex {
  width: 2%;
  height: 2%;
  cursor: pointer;
  margin-left: 8px;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-enter-to,
.fade-slide-leave-from {
  max-height: 500px;
  opacity: 1;
  transform: translateY(0);
}

.botons-container {
  display: flex;
  justify-content: space-between;
}

.button-add {
  background-color: #d8d8d8;
  color: #7f5af0;
  font-size: xx-large;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.icono-trash {
  width: 18%;
  height: 18%;
  cursor: pointer;
  margin-top: 22%;
}

.expand-button {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
