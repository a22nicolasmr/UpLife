<script>
import EngadirAuga from "@/components/EngadirAuga.vue";
import HistorialAuga from "@/components/HistorialAuga.vue";

export default {
  components: {
    HistorialAuga,
    EngadirAuga,
  },
  data() {
    return {
      componenteActivo: "historial",
      augaHoxe: [],
    };
  },
  mounted() {
    // this.cargarAugaHoxe();
  },
  methods: {
    async cargarAugaHoxe() {
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch("http://localhost:8001/api/exercicios/");
        if (!response.ok) throw new Error("Erro ao cargar exercicios");

        const exercicios = await response.json();
        this.augaHoxe = exercicios.filter((ex) => ex.data === hoxe);
      } catch (error) {
        console.error("Erro cargando exercicios:", error);
      }
    },
    async eliminarExercicio(id) {
      try {
        const response = await fetch(
          `http://localhost:8001/api/exercicios/${id}/`,
          {
            method: "DELETE",
          }
        );
        if (!response.ok) throw new Error("Erro ao eliminar exercicio");

        this.augaHoxe = this.augaHoxe.filter((ex) => ex.id_exercicio !== id);
        window.location.reload();
      } catch (error) {
        console.error("Erro eliminando exercicio:", error);
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
                <th>Hora</th>
                <th>Cantidade</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="exercicio in augaHoxe" :key="exercicio.id_exercicio">
                <td>{{ exercicio.nome }}</td>
                <td>{{ nomeCategoriaPorId(exercicio.categoria) }}</td>
                <td>{{ exercicio.repeticions }}</td>
                <td>{{ exercicio.peso }} kg</td>
                <td>
                  <img
                    src="/imaxes/trash.png"
                    alt="icona borrar"
                    @click="eliminarExercicio(exercicio.id_exercicio)"
                  />
                </td>
              </tr>
              <tr v-if="augaHoxe.length === 0">
                <td colspan="4">Non hai exercicios rexistrados para hoxe.</td>
              </tr>
            </tbody>
          </table>
          <button @click="componenteActivo = 'engadirA'" id="engadirA">
            +
          </button>
        </div>
      </div>

      <div class="dereita">
        <HistorialAuga v-if="componenteActivo === 'historial'" />
        <EngadirAuga v-if="componenteActivo === 'engadirA'" />
      </div>
    </div>
  </div>
</template>

<style scoped>
#engadirA {
  font-size: xx-large;
}
#engadirP {
  font-size: smaller;
  width: 25%;
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
  width: 9%;
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
#divXeral2 {
  display: flex;
  flex-direction: column;
  height: 85%;
  overflow-y: auto;
  margin: none;
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
  margin-bottom: 1%;
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
  border-bottom: 1% solid #acacac;
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
