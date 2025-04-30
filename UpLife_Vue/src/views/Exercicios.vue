<script>
import EngadirExercicios from "@/components/EngadirExercicios.vue";
import EngadirPlantillasExercicios from "@/components/EngadirPlantillasExercicios.vue";
import HistorialExercicios from "@/components/HistorialExercicios.vue";

export default {
  components: {
    HistorialExercicios,
    EngadirExercicios,
    EngadirPlantillasExercicios,
  },
  data() {
    return {
      componenteActivo: "historial",
      exerciciosHoxe: [],
    };
  },
  mounted() {
    this.cargarExerciciosHoxe();
  },
  methods: {
    nomeCategoriaPorId(id) {
      const mapa = {
        1: "Perna",
        2: "Brazo",
        3: "Core",
        4: "Espalda",
        5: "Peito",
      };
      return mapa[id] || "Descoñecida";
    },
    async cargarExerciciosHoxe() {
      const hoxe = new Date().toISOString().split("T")[0];

      try {
        const response = await fetch("http://localhost:8001/api/exercicios/");
        if (!response.ok) throw new Error("Erro ao cargar exercicios");

        const exercicios = await response.json();
        this.exerciciosHoxe = exercicios.filter((ex) => ex.data === hoxe);
      } catch (error) {
        console.error("Erro cargando exercicios:", error);
      }
    },
  },
};
</script>

<template>
  <div id="divXeral">
    <h1 class="titulo">Exercicios</h1>
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
        :class="{ inactiva: componenteActivo !== 'engadirE' }"
        @click="componenteActivo = 'engadirE'"
      >
        Engadir exercicios
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadirP' }"
        @click="componenteActivo = 'engadirP'"
      >
        Engadir plantillas
      </div>
    </div>

    <div class="exercicios-layout">
      <div class="esquerda">
        <div class="esquerdaArriba">
          <h2>Exercicios de hoxe</h2>
          <button id="engadirP">Engadir plantilla</button>
        </div>
        <div class="esquerdaAbaixo">
          <table>
            <thead>
              <tr>
                <th>Título</th>
                <th>Categoría</th>
                <th>Repeticións</th>
                <th>Peso</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="exercicio in exerciciosHoxe"
                :key="exercicio.id_exercicio"
              >
                <td>{{ exercicio.nome }}</td>
                <td>{{ nomeCategoriaPorId(exercicio.categoria) }}</td>
                <td>{{ exercicio.repeticions }}</td>
                <td>{{ exercicio.peso }} kg</td>
              </tr>
              <tr v-if="exerciciosHoxe.length === 0">
                <td colspan="4">Non hai exercicios rexistrados para hoxe.</td>
              </tr>
            </tbody>
          </table>
          <button @click="componenteActivo = 'engadirE'" id="engadirE">
            +
          </button>
        </div>
      </div>

      <div class="dereita">
        <HistorialExercicios v-if="componenteActivo === 'historial'" />
        <EngadirExercicios v-if="componenteActivo === 'engadirE'" />
        <EngadirPlantillasExercicios v-if="componenteActivo === 'engadirP'" />
      </div>
    </div>
  </div>
</template>

<style scoped>
#engadirE {
  font-size: xx-large;
}
#engadirP {
  font-size: smaller;
}
.esquerdaAbaixo {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 100%;
}
table {
  width: 100%;
}
tr {
  display: flex;
  justify-content: space-around;
}
.esquerdaArriba {
  display: flex;
  justify-content: space-between;
  margin-left: 2%;
  margin-right: 2%;
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
  width: 10%;
  height: 5%;
}
html,
body {
  height: 100%;
  width: 100%;
}
.esquerda {
  width: 60%;
}
#divXeral {
  display: flex;
  flex-direction: column;
  height: 85%;
  overflow-y: auto;
  margin-left: 4%;
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
  margin-left: 46.4%;
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

.exercicios-layout {
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
h2 {
  color: #7f5af0;
}
h1 {
  display: flex;
  align-self: flex-start;
  font-size: 2vw;
  margin-bottom: 3vh;
  color: #7f5af0;
}
/* Compoñente dereita */
.dereita {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
}
.esquerdaAbaixo {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  padding: 2%;
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
  padding: 12px;
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

td[colspan="4"] {
  text-align: center;
  color: #aaa;
  font-style: italic;
}
</style>
