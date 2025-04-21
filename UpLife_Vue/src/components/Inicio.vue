<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      contrasinal: "",
      erro: "",
    };
  },
  methods: {
    async mandarFormulario() {
      this.erro = "";

      if (!this.email || !this.contrasinal) {
        this.erro = "Completa todos os campos";
        this.contrasinal = "";
        return;
      }

      try {
        const response = await axios.post("http://localhost:8000/login/", {
          identificador: this.email,
          contrasinal: this.contrasinal,
        });

        if (response.status === 200) {
          this.$router.push({
            name: "tarefas",
            query: { nombre: usuario.nombre },
          });
        }
      } catch (error) {
        console.error("Erro ao iniciar sesión:", error);
        if (error.response?.status === 401 || error.response?.status === 404) {
          this.erro = "Nome de usuario";
        } else {
          this.erro = "Erro ao iniciar sesión. Inténtao de novo.";
        }
        this.contrasinal = "";
      }
    },
  },
};
</script>

<template>
  <div class="formulario">
    <h1>Benvido de volta a UpLife</h1>
    <form action="" method="get">
      <label for="inputEmail">Nome de usuario ou Email</label>
      <input
        type="text"
        id="inputEmail"
        placeholder="Escribe o teu nome de usuario ou email"
        v-model="email"
      />

      <label for="inputContrasinal">Contrasinal</label>
      <input
        type="password"
        id="inputContrasinal"
        placeholder="Escribe o teu contrasinal"
        v-model="contrasinal"
      />

      <div v-if="erro" class="erro">
        {{ erro }}
      </div>

      <button type="submit" @click.prevent="mandarFormulario()">
        Iniciar sesión
      </button>

      <p>
        Non tes unha conta?
        <a href="#" @click.prevent="$router.push({ name: 'rexistro' })">
          Rexistro
        </a>
      </p>
    </form>
  </div>
</template>

<style scoped>
.erro {
  color: red;
  font-size: 0.9rem;
  margin-bottom: 8px;
}
</style>
