<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      comidasPorDia: {},
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
      const response = await fetch("http://localhost:8001/api/comidas/");
      if (!response.ok) throw new Error("Erro ao cargar comidas");

      const comidas = await response.json();
      const comidasPorUsuario = comidas.filter(
        (c) => c.usuario === this.idUsuario
      );

      const agrupados = {};
      comidasPorUsuario.forEach((c) => {
        if (!agrupados[c.data]) agrupados[c.data] = [];
        agrupados[c.data].push(c);
      });

      const comidasOrdenadas = Object.fromEntries(
        Object.entries(agrupados).sort(
          (a, b) => new Date(b[0]) - new Date(a[0])
        )
      );

      this.comidasPorDia = comidasOrdenadas;
    } catch (error) {
      console.error("Erro ao obter historial de comidas:", error);
    }
  },
  methods: {
    async engadirComida(comida) {
      const payload = {
        nome: comida.nome,
        peso: comida.peso,
        graxas: comida.graxas,
        carbohidratos: comida.carbohidratos,
        proteinas: comida.proteinas,
        calorias: comida.calorias,
        data: this.dataHoxeISO,
        usuario: this.idUsuario,
      };

      try {
        const response = await fetch("http://localhost:8001/api/comidas/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Erro ao engadir comida");

        await response.json();
        window.location.reload();
      } catch (error) {
        console.error("❗Erro no try-catch:", error);
      }
    },
  },
};
</script>

<template>
  <div id="divXeral">
    <h2>Historial</h2>
    <div class="historial-scroll">
      <div
        v-for="(comidas, data) in comidasPorDia"
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
          <li v-for="comida in comidas" :key="comida.id_comida">
            <div class="fila-exercicio">
              <span>
                {{ comida.nome }} - {{ comida.peso }}g -
                {{ Math.ceil((comida.calorias / 100) * comida.peso) }} kcal
              </span>
              <button class="boton-dereita" @click="engadirComida(comida)">
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
