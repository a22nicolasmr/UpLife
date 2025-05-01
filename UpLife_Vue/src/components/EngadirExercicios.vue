<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      nome: "",
      repeticions: "",
      peso: null,
      categoriaSeleccionada: "",
      categorias: ["Peito", "Espalda", "Core", "Brazo", "Pierna"],
    };
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
    obterIdCategoria(nome) {
      const mapa = {
        Perna: 1,
        Brazo: 2,
        Core: 3,
        Espalda: 4,
        Peito: 5,
      };
      return mapa[nome];
    },
    async engadirExercicio() {
      const idCategoria = this.obterIdCategoria(this.categoriaSeleccionada);
      if (!this.nome || !this.repeticions || !this.peso || !idCategoria) {
        alert("Por favor, cobre todos os campos.");
        return;
      }

      const payload = {
        nome: this.nome,
        repeticions: this.repeticions,
        peso: this.peso,
        data: this.dataHoxeISO,
        usuario: this.idUsuario,
        categoria: this.obterIdCategoria(this.categoriaSeleccionada),
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

        // Limpiar formulario
        this.nome = "";
        this.repeticions = "";
        this.peso = null;
        this.categoriaSeleccionada = "";

        window.location.reload();
      } catch (error) {
        console.error("❗Erro no try-catch:", error);
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Engadir exercicio</h2>

      <label for="categoria">Categoría</label>
      <select v-model="categoriaSeleccionada" id="categoria">
        <option disabled value="">Selecciona unha categoría</option>
        <option v-for="cat in categorias" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>

      <label for="nome">Nome do exercicio</label>
      <input
        type="text"
        id="nome"
        v-model="nome"
        placeholder="Nome do exercicio"
      />

      <label for="repeticions">Repeticións</label>
      <input
        type="text"
        id="repeticions"
        v-model="repeticions"
        placeholder="Exemplo: 3x10"
      />

      <label for="peso">Peso (kg)</label>
      <input type="number" id="peso" v-model="peso" min="0" step="0.1" />

      <button @click="engadirExercicio">Engadir</button>
    </div>
  </div>
</template>

<style scoped>
.formulario button {
  margin-bottom: 4%;
  width: 100%;
}
.formulario label {
  width: 100%;
}
.formulario {
  display: flex;
  flex-direction: column;
  width: 100%;
}
.engadir-container {
  height: 100%;
  width: 100%;
  overflow-y: auto;

  display: flex;
  justify-content: center;
  align-items: center;
}
h2 {
  color: #7f5af0;
}
p,
label {
  color: white;
}
input,
select {
  padding: 2%;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: medium;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 5%;
}
</style>
