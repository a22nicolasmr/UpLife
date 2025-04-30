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

      console.log("Campos do formulario:");
      console.log("Nome:", this.nome);
      console.log("Repeticións:", this.repeticions);
      console.log("Peso:", this.peso);
      console.log("Categoría seleccionada:", this.categoriaSeleccionada);
      console.log("ID categoría:", idCategoria);
      console.log("Data:", this.dataHoxeISO);
      console.log("ID usuario:", this.idUsuario);

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
    <h2>Engadir exercicio</h2>

    <div class="formulario">
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
p,
label {
  color: white;
}
</style>
