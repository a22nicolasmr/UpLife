<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      exerciciosPorDia: {},
    };
  },
  async mounted() {
    try {
      const response = await fetch("http://localhost:8001/api/exercicios/");
      if (!response.ok) throw new Error("Erro ao cargar exercicios");

      const exercicios = await response.json();

      const seteDiasAtras = new Date();
      seteDiasAtras.setDate(seteDiasAtras.getDate() - 6); // últimos 7 días incluindo hoxe

      const exerciciosFiltrados = exercicios.filter((ex) => {
        const dataEx = new Date(ex.data);
        return dataEx >= seteDiasAtras;
      });

      // Agrupar por data (YYYY-MM-DD)
      const agrupados = {};
      exerciciosFiltrados.forEach((ex) => {
        if (!agrupados[ex.data]) agrupados[ex.data] = [];
        agrupados[ex.data].push(ex);
      });

      // Ordenar por data descendente
      this.exerciciosPorDia = Object.fromEntries(
        Object.entries(agrupados).sort(
          (a, b) => new Date(b[0]) - new Date(a[0])
        )
      );
    } catch (error) {
      console.error("Erro ao obter historial:", error);
    }
  },
  computed: {
    idUsuario() {
      const store = useUsuarioStore();
      return store.id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0]; // formato YYYY-MM-DD
    },
  },
  methods: {
    async engadirExercicio(exercicio) {
      const payload = {
        nome: exercicio.nome,
        repeticions: exercicio.repeticions,
        peso: exercicio.peso,
        data: this.dataHoxeISO, // 👈 siempre hoy
        usuario: this.idUsuario,
        categoria: exercicio.categoria, // 👈 mantenemos categoría
      };

      try {
        const response = await fetch("http://localhost:8001/api/exercicios/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error("Erro ao engadir exercicio");
        }

        const resultado = await response.json();

        window.location.reload();
      } catch (error) {
        console.error("❗Erro no try-catch:", error);
      }
    },
    nomeCategoria(idCategoria) {
      const mapa = {
        1: "Perna",
        2: "Brazo",
        3: "Core",
        4: "Espalda",
        5: "Peito",
      };
      return mapa[idCategoria] || "Descoñecida";
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
                {{ ex.nome }} - {{ ex.repeticions }} - {{ ex.peso }}kg ({{
                  nomeCategoria(ex.categoria)
                }})
              </span>
              <button class="boton-dereita" @click="engadirExercicio(ex)">
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
