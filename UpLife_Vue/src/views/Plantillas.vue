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
      plantillas: [],
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
        const response = await fetch(`http://localhost:8001/api/plantillas/`);

        if (!response.ok) throw new Error("Erro ao cargar plantillas");
        const plantillas = await response.json();

        this.plantillas = plantillas.filter((p) => p.usuario === idUsuario);
      } catch (error) {
        console.error("Erro cargando datos:", error);
      }
    },
    async borrarPlantilla(id) {
      try {
        const response = await fetch(
          `http://localhost:8001/api/plantillas/${id}/`,
          {
            method: "DELETE",
          }
        );

        if (!response.ok) {
          throw new Error("Erro ao eliminar a plantilla");
        }

        this.plantillas = this.plantillas.filter((p) => p.id_plantilla !== id);
        window.location.reload();
      } catch (error) {
        console.error("❌ Erro eliminando plantilla:", error);
      }
    },
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
        Engadir
      </div>
    </div>

    <div class="plantilla-layout">
      <div class="esquerda">
        <h1>Lista de plantillas</h1>
        <div
          v-for="plantilla in this.plantillas"
          :key="plantilla.id"
          id="divPlantilla"
        >
          <div class="plantilla-header">
            <img :src="plantilla.icona" alt="icona plantilla" />
            <h3>{{ plantilla.nome }}</h3>
            <button class="button" @click="componenteActivo = 'engadirE'">
              +
            </button>
            <img
              src="/imaxes/trash.png"
              alt="icona borrar"
              @click="borrarPlantilla(plantilla.id_plantilla)"
            />
          </div>

          <div class="exercicios-plantilla">
            <template
              v-if="plantilla.exercicios && plantilla.exercicios.length"
            >
              <div
                v-for="ex in plantilla.exercicios"
                :key="ex.id_exercicio"
                class="exercicio"
              >
                {{ ex.nome }} - {{ ex.repeticions }} - {{ ex.peso }}kg
              </div>
            </template>
            <p v-else class="sen-exercicios">
              Esta plantilla non ten exercicios.
            </p>
          </div>
        </div>
        <button @click="componenteActivo = 'nova'" id="engadirE">+</button>
      </div>

      <div class="dereita">
        <NovaPlantilla v-if="componenteActivo === 'nova'" />
        <EngadirExercicioPlantilla v-if="componenteActivo === 'engadirE'" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.button {
  background-color: #d8d8d8;
  color: #7f5af0;
  font-size: xx-large;
  display: flex;
  justify-self: center;
}
#divPlantilla {
  background-color: #d8d8d8;
  border-radius: 2%;
  margin-bottom: 2%;
  padding: 1%;
  display: flex;
  flex-direction: column;
}

.plantilla-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#divPlantilla > .plantilla-header img:first-child {
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
  border-radius: 2%;
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

.info-plantilla p {
  margin: 2px 0;
  color: #666;
  font-size: large;
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
}

.exercicio {
  border-bottom: 1px solid #ccc;
  color: black;
}

.sen-exercicios {
  font-style: italic;
  color: #777;
}
</style>
