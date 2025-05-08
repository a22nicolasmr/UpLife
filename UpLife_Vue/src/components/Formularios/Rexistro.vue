<script>
import axios from "axios";

export default {
  data() {
    return {
      nomeCompleto: "",
      email: "",
      nomeUsuario: "",
      contrasinal: "",
      repiteContrasinal: "",
      errors: {
        nomeCompleto: "",
        email: "",
        nomeUsuario: "",
        contrasinal: "",
        repiteContrasinal: "",
      },
    };
  },
  methods: {
    // mandar formulario de rexistro facendo un post se o formulario está correcto
    async mandarFormulario() {
      let isValid = true;
      this.errors = {
        nomeCompleto: "",
        email: "",
        nomeUsuario: "",
        contrasinal: "",
        repiteContrasinal: "",
      };

      if (!this.nomeCompleto) {
        this.errors.nomeCompleto = "Nome Completo obrigatorio";
        isValid = false;
      }

      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!this.email) {
        this.errors.email = "Email obrigatorio";
        isValid = false;
      } else if (!emailPattern.test(this.email)) {
        this.errors.email = "Email non válido";
        isValid = false;
      }

      if (!this.nomeUsuario) {
        this.errors.nomeUsuario = "Nome de Usuario obrigatorio";
        isValid = false;
      }

      if (!this.contrasinal) {
        this.errors.contrasinal = "Contrasinal obrigatorio";
        isValid = false;
      }

      if (!this.repiteContrasinal) {
        this.errors.repiteContrasinal = "Repite o contrasinal obrigatorio";
        isValid = false;
      } else if (this.contrasinal !== this.repiteContrasinal) {
        this.errors.repiteContrasinal = "Os contrasinais non coinciden";
        isValid = false;
      }

      if (isValid) {
        try {
          const response = await axios.post(
            "http://localhost:8001/api/usuarios/",
            {
              nome: this.nomeCompleto,
              email: this.email,
              nome_usuario: this.nomeUsuario,
              contrasinal: this.contrasinal,
              modo_aplicacion: "C",
            }
          );

          if (response.status === 201) {
            this.$router.push({ name: "inicio" });
          } else {
            this.contrasinal = "";
            this.repiteContrasinal = "";
            console.error("Erro:", response.data);
          }
        } catch (error) {
          this.contrasinal = "";
          this.repiteContrasinal = "";

          if (error.response?.status === 400) {
            const data = error.response.data;
            if (data.email) {
              this.errors.email = "Xa existe unha conta con ese email";
            }
            if (data.nome_usuario) {
              this.errors.nomeUsuario = "Este nome de usuario xa está en uso";
            }
          } else {
            console.log("Erro ao crear a conta. Inténtao de novo.");
          }

          console.error(
            "Erro ao crear a conta:",
            error.response?.data || error
          );
        }
      } else {
        this.contrasinal = "";
        this.repiteContrasinal = "";
        console.log("Hai erros no formulario");
      }
    },
  },
};
</script>

<template>
  <div class="formulario">
    <h1>Benvido a UpLife</h1>

    <form @submit.prevent="mandarFormulario">
      <label for="idNomeCompleto">Nome Completo</label>
      <input
        type="text"
        id="idNomeCompleto"
        v-model="nomeCompleto"
        placeholder="Escribe o teu nome completo"
      />
      <div v-if="errors.nomeCompleto" class="erro">
        {{ errors.nomeCompleto }}
      </div>

      <label for="idEmail">Email</label>
      <input
        type="text"
        id="idEmail"
        v-model="email"
        placeholder="Escribe o teu email"
      />
      <div v-if="errors.email" class="erro">{{ errors.email }}</div>

      <label for="idNomeUsuario">Nome de Usuario</label>
      <input
        type="text"
        id="idNomeUsuario"
        v-model="nomeUsuario"
        placeholder="Escribe o teu nome de usuario"
      />
      <div v-if="errors.nomeUsuario" class="erro">{{ errors.nomeUsuario }}</div>

      <label for="idContrasinal">Contrasinal</label>
      <input
        type="password"
        id="idContrasinal"
        v-model="contrasinal"
        placeholder="Escribe o teu contrasinal"
      />
      <div v-if="errors.contrasinal" class="erro">{{ errors.contrasinal }}</div>

      <label for="idRepiteContrasinal">Repite Contrasinal</label>
      <input
        type="password"
        id="idRepiteContrasinal"
        v-model="repiteContrasinal"
        placeholder="Repite o teu contrasinal"
      />
      <div v-if="errors.repiteContrasinal" class="erro">
        {{ errors.repiteContrasinal }}
      </div>

      <button type="submit">Crear conta</button>

      <p>
        Xa tes unha conta?
        <a href="#" @click.prevent="$router.push({ name: 'inicio' })"
          >Iniciar sesión</a
        >
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
