<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      exerciciosPorDia: {},
      plantillasPorDia: [],
    };
  },
  computed: {
    idUsuario() {
      const store = useUsuarioStore();
      return store.id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
  },
  async mounted() {
    try {
      const response = await fetch("http://localhost:8001/api/exercicios/");
      if (!response.ok) throw new Error("Erro ao cargar exercicios");

      const exercicios = await response.json();
      const exerciciosPorUsuario = exercicios.filter(
        (e) => e.usuario === this.idUsuario
      );
      const seteDiasAtras = new Date();
      seteDiasAtras.setDate(seteDiasAtras.getDate() - 7);

      const exerciciosFiltrados = exerciciosPorUsuario.filter((ex) => {
        const dataEx = new Date(ex.data);
        return dataEx >= seteDiasAtras;
      });

      const agrupados = {};
      exerciciosFiltrados.forEach((ex) => {
        if (!agrupados[ex.data]) agrupados[ex.data] = [];
        agrupados[ex.data].push(ex);
      });

      this.exerciciosPorDia = Object.fromEntries(
        Object.entries(agrupados).sort(
          (a, b) => new Date(b[0]) - new Date(a[0])
        )
      );

      const response2 = await fetch("http://localhost:8001/api/plantillas/");
      const plantillas = await response2.json();

      const seteDiasAtras2 = new Date();
      seteDiasAtras2.setDate(seteDiasAtras2.getDate() - 7);
      const seteDiasAtrasISO = seteDiasAtras2.toISOString().split("T")[0];

      const plantillasFiltradas = plantillas.filter(
        (p) => p.usuario === this.idUsuario && p.data >= seteDiasAtrasISO
      );
      this.plantillasPorDia = plantillasFiltradas;
    } catch (error) {
      console.error("Erro ao obter historial:", error);
    }
  },
  methods: {
    async engadirExercicio(exercicio) {
      const payload = {
        nome: exercicio.nome,
        repeticions: exercicio.repeticions,
        peso: exercicio.peso,
        data: this.dataHoxeISO,
        usuario: this.idUsuario,
        categoria: exercicio.categoria,
      };

      try {
        const response = await fetch("http://localhost:8001/api/exercicios/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Erro ao engadir exercicio");

        await response.json();
        this.$emit("cargarExerciciosHoxe");
      } catch (error) {
        console.error("❗Erro no try-catch:", error);
      }
    },
    async engadirPlantilla(plantilla) {
      const response = await fetch(
        `http://localhost:8001/api/plantillas/${plantilla.id_plantilla}/`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ data: this.dataHoxeISO }),
        }
      );

      if (!response.ok) {
        console.error("Erro ao actualizar plantilla");
      } else {
        this.$emit("cargarPlantillasHoxe");
      }
    },
    nomeCategoria(idCategoria) {
      const mapa = {
        1: "Perna",
        2: "Brazo",
        3: "Core",
        4: "Espalda",
        5: "Peito",
        6: "Todo corpo",
      };
      return mapa[idCategoria] || "Desco\u00f1ecida";
    },
  },
};
</script>

<template>
  <div id="divXeral">
    <h2>Historial</h2>
    <div class="historial-scroll">
      <div
        v-for="(exs, data) in exerciciosPorDia"
        :key="data"
        class="grupo-dia"
      >
        <h3>
          {{
            new Date(data).toLocaleDateString("gl-ES", {
              weekday: "long",
              day: "numeric",
              month: "long",
            })
          }}
        </h3>
        <ul>
          <li v-for="ex in exs" :key="ex.id_exercicio">
            <div class="fila-exercicio">
              <span>
                [E] {{ ex.nome }} - {{ ex.repeticions }} - {{ ex.peso }}kg ({{
                  nomeCategoria(ex.categoria)
                }})
              </span>
              <button class="boton-dereita" @click="engadirExercicio(ex)">
                +
              </button>
            </div>
          </li>
        </ul>
        <ul>
          <li
            v-for="p in plantillasPorDia.filter((x) => x.data === data)"
            :key="p.id_plantilla"
          >
            <div class="fila-exercicio">
              <span id="spanPlantilla"> [P] {{ p.nome }} </span>
              <button class="boton-dereita" @click="engadirPlantilla(p)">
                +
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.icona {
  height: 10%;
  width: 10%;
  background: white;
  border-radius: 4px;
}
#divXeral {
  padding: 5%;
}

h2 {
  color: #7f5af0;
  margin-bottom: 2%;
}

.historial-scroll {
  overflow-y: auto;
  padding-right: 2%;
}

.grupo-dia {
  border-bottom: 1px solid #aaa;
  padding-bottom: 2%;
}

h3 {
  color: white;
  margin-bottom: 5px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  color: white;
  padding: 1% 0;
}

.fila-exercicio {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.boton-dereita {
  background-color: #7f5af0;
  color: white;
  border: none;
  padding: 1% 2%;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.3s ease;
}

.boton-dereita:hover {
  background-color: #6e4bd9;
}
</style>
