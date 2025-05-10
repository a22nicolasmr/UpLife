<script>
import EngadirExercicios from "@/components/Exercicios/EngadirExercicios.vue";
import EngadirPlantillasExercicios from "@/components/Exercicios/EngadirPlantillasExercicios.vue";
import HistorialExercicios from "@/components/Exercicios/HistorialExercicios.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

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
      plantillasHoxe: [],
    };
  },
  mounted() {
    //cargar exercicios e plantillas da data actual ao montar o compoñente
    this.cargarExerciciosHoxe();
    this.cargarPlantillasHoxe();
  },
  methods: {
    //mapear nome da categoría según o seu id
    nomeCategoriaPorId(id) {
      const mapa = {
        1: "Perna",
        2: "Brazo",
        3: "Core",
        4: "Espalda",
        5: "Peito",
        6: "Todo corpo",
      };
      return mapa[id] || "Descoñecida";
    },

    //cargar exercicios filtrando por data do día actual e id de usuario
    async cargarExerciciosHoxe() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch("http://localhost:8001/api/exercicios/");
        if (!response.ok) throw new Error("Erro ao cargar exercicios");

        const exercicios = await response.json();

        const seteDiasAtras = new Date();
        seteDiasAtras.setDate(seteDiasAtras.getDate() - 7);

        const exerciciosAnteriores = exercicios.filter((e) => {
          if (!e.data) return false;
          const dataExercicio = new Date(e.data);
          return dataExercicio < seteDiasAtras;
        });

        exerciciosAnteriores.forEach((e) => {
          this.eliminarExercicio(e.id_exercicio);
        });

        this.exerciciosHoxe = exercicios.filter(
          (ex) => ex.usuario === idUsuario && ex.data === hoxe
        );
      } catch (error) {
        console.error("Erro cargando exercicios:", error);
      }
    },
    //eliminar exercicio por id
    async eliminarExercicio(id) {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      try {
        const response = await fetch(
          `http://localhost:8001/api/exercicios/${id}/`,
          {
            method: "DELETE",
          }
        );
        if (!response.ok) throw new Error("Erro ao eliminar exercicio");

        this.exerciciosHoxe = this.exerciciosHoxe.filter(
          (ex) => ex.usuario === idUsuario && ex.id_exercicio !== id
        );
        this.cargarExerciciosHoxe();
      } catch (error) {
        console.error("Erro eliminando exercicio:", error);
      }
    },

    //cargar plantillas filtrando por data actual e id de usuario
    async cargarPlantillasHoxe() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch("http://localhost:8001/api/plantillas/");
        if (!response.ok) throw new Error("Erro ao cargar plantillas");

        const plantillas = await response.json();
        this.plantillasHoxe = plantillas.filter(
          (p) => p.usuario === idUsuario && p.data === hoxe
        );
      } catch (error) {
        console.error("Erro cargando plantillas hoxe:", error);
      }
    },
    //engadir plantilla ao usuario
    async engadirPlantilla(plantillaSeleccionada) {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      try {
        console.log(
          "plantilla seleccionada desde Exercicios ",
          plantillaSeleccionada
        );
        const response = await fetch(`http://localhost:8001/api/plantillas/`, {
          method: "GET",
        });
        const plantillas = await response.json();
        const plantillaFiltrada = plantillas.find(
          (p) => p.usuario === idUsuario && p.nome === plantillaSeleccionada
        );

        const hoxe = new Date().toISOString().split("T")[0]; // YYYY-MM-DD

        const response2 = await fetch(
          `http://localhost:8001/api/plantillas/${plantillaFiltrada.id_plantilla}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              data: hoxe,
            }),
          }
        );

        if (!response2.ok) {
          throw new Error("Erro ao actualizar a plantilla");
        }
        this.cargarPlantillasHoxe();
      } catch (error) {
        console.error(error);
      }
    },
    //eliminar plantilla por id
    async eliminarPlantilla(id_plantilla) {
      const response2 = await fetch(
        `http://localhost:8001/api/plantillas/${id_plantilla}/`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            data: null,
          }),
        }
      );

      if (!response2.ok) {
        throw new Error("Erro ao actualizar a plantilla");
      }
      this.cargarPlantillasHoxe();
    },
  },
};
</script>

<template>
  <div id="divXeral2">
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
        </div>
        <div class="esquerdaAbaixo">
          <table>
            <thead>
              <tr>
                <th>Título</th>
                <th>Categoría</th>
                <th>Repeticións</th>
                <th>Peso</th>
                <th>Eliminar</th>
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
                <td>
                  <img
                    src="/imaxes/trash.png"
                    alt="icona borrar"
                    @click="eliminarExercicio(exercicio.id_exercicio)"
                  />
                </td>
              </tr>
              <tr v-if="exerciciosHoxe.length === 0">
                <td colspan="4">Non hai exercicios rexistrados para hoxe.</td>
              </tr>
            </tbody>
          </table>
          <button @click="componenteActivo = 'engadirE'">+</button>
        </div>

        <!-- NOVA TÁBOA DE PLANTILLAS -->
        <div class="esquerdaAbaixo">
          <h2>Plantillas de hoxe</h2>
          <table>
            <thead>
              <tr>
                <th>Icona</th>
                <th>Nome</th>
                <th>Eliminar</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="plantilla in plantillasHoxe"
                :key="plantilla.id_plantilla"
              >
                <td>
                  <img
                    :src="plantilla.icona"
                    alt="icona plantilla"
                    class="icona"
                  />
                </td>
                <td>{{ plantilla.nome }}</td>
                <td>
                  <img
                    src="/imaxes/trash.png"
                    alt="icona borrar"
                    @click="eliminarPlantilla(plantilla.id_plantilla)"
                    class="icon"
                  />
                </td>
              </tr>
              <tr v-if="plantillasHoxe.length === 0">
                <td colspan="3">Non hai plantillas rexistradas para hoxe.</td>
              </tr>
            </tbody>
          </table>
          <button @click="componenteActivo = 'engadirP'">+</button>
        </div>
      </div>

      <div class="dereita">
        <HistorialExercicios
          v-if="componenteActivo === 'historial'"
          @cargarExerciciosHoxe="cargarExerciciosHoxe"
          @cargarPlantillasHoxe="cargarPlantillasHoxe"
        />
        <EngadirExercicios
          v-if="componenteActivo === 'engadirE'"
          @cargarExerciciosHoxe="cargarExerciciosHoxe"
        />
        <EngadirPlantillasExercicios
          v-if="componenteActivo === 'engadirP'"
          @engadirPlantilla="engadirPlantilla"
          @cargarPlantillasHoxe="cargarPlantillasHoxe"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.icon {
  height: 10%;
  width: 10%;
}
.icona {
  height: 20%;
  width: 20%;
  background: white;
  border-radius: 4px;
}
#engadirE {
  font-size: xx-large;
}
#engadirPbutton {
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
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  margin-bottom: 1%;
  height: 65vh;
  overflow: hidden;
}

.esquerda {
  width: 60%;
  height: 100%;
  overflow-y: auto;
  padding: 1%;
  box-sizing: border-box;
  overflow-x: hidden;
}

.esquerdaAbaixo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  padding: 2%;
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
  overflow-y: auto;
}

table {
  width: 96%;
  border-collapse: collapse;
  background-color: #d8d8d8;
  color: black;
  border-radius: 8px;
  overflow: hidden;
  margin: 0;
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

td[colspan="4"],
td[colspan="3"] {
  text-align: center;
  color: #aaa;
  font-style: italic;
}
</style>
