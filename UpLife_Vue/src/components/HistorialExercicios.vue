<script>
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
      seteDiasAtras.setDate(seteDiasAtras.getDate() - 6); // últimos 7 días incluyendo hoxe

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
  methods: {
    nomeCategoria(id) {
      const mapa = {
        1: "Perna",
        2: "Brazo",
        3: "Core",
        4: "Espalda",
        5: "Peito",
      };
      return mapa[id] || "Descoñecida";
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
              <button class="boton-dereita">+</button>
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
  margin-bottom: 20px;
}

.historial-scroll {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 10px;
}

.grupo-dia {
  margin-bottom: 20px;
  border-bottom: 1px solid #aaa;
  padding-bottom: 10px;
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
  padding: 6px 0;
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
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.3s ease;
}

.boton-dereita:hover {
  background-color: #6e4bd9;
}
</style>
