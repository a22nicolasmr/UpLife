<script>
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
    async mandarFormulario() {
      let isValid = true;
      // Resetea los errores
      this.errors = {
        nomeCompleto: "",
        email: "",
        nomeUsuario: "",
        contrasinal: "",
        repiteContrasinal: "",
      };

      // Validación de Nome Completo
      if (!this.nomeCompleto) {
        this.errors.nomeCompleto = "Nome Completo obrigatorio";
        isValid = false;
      }

      // Validación de Email
      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!this.email) {
        this.errors.email = "Email obrigatorio";
        isValid = false;
      } else if (!emailPattern.test(this.email)) {
        this.errors.email = "Email non válido";
        isValid = false;
      }

      // Validación de Nome de Usuario
      if (!this.nomeUsuario) {
        this.errors.nomeUsuario = "Nome de Usuario obrigatorio";
        isValid = false;
      }

      // Validación de Contraseña
      if (!this.contrasinal) {
        this.errors.contrasinal = "Contrasinal obrigatorio";
        isValid = false;
      }

      // Validación de Repetir Contraseña
      if (!this.repiteContrasinal) {
        this.errors.repiteContrasinal = "Repite o contrasinal obrigatorio";
        isValid = false;
      } else if (this.contrasinal !== this.repiteContrasinal) {
        this.errors.repiteContrasinal = "Os contrasinais non coinciden";
        isValid = false;
      }

      // Si todo está bien, realiza el POST
      if (isValid) {
        try {
          // Hacemos el POST al servidor con los datos del formulario
          const response = await fetch("http://localhost:8000/api/usuarios/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              nome: this.nomeCompleto,
              email: this.email,
              nome_usuario: this.nomeUsuario,
              contrasinal: this.contrasinal,
              modo_aplicacion: "C",
            }),
          });

          // Si el POST es exitoso, muestra un mensaje
          if (response.status === 201) {
            this.$router.push({ name: "inicio" });
          } else {
            const data = await response.json();
            console.error("Error al crear la cuenta:", data);
            alert("Erro ao crear a conta. Inténtao de novo.");
          }
        } catch (error) {
          console.error("Hubo un error al crear la cuenta:", error);
          alert("Erro ao crear a conta. Inténtao de novo.");
        }
      } else {
        alert("Hai erros no formulario");
      }
    },
  },
};
</script>

<template>
  <div>
    <h1>Benvido a UpLife</h1>
    <form @submit.prevent="mandarFormulario">
      <label for="idNomeCompleto">Nome Completo</label>
      <input
        type="text"
        id="idNomeCompleto"
        v-model="nomeCompleto"
        placeholder="Escribe o teu nome completo"
      />
      <div v-if="errors.nomeCompleto" style="color: red">
        {{ errors.nomeCompleto }}
      </div>

      <br />

      <label for="idEmail">Email</label><br />
      <input
        type="text"
        id="idEmail"
        v-model="email"
        placeholder="Escribe o teu email"
      />
      <div v-if="errors.email" style="color: red">
        {{ errors.email }}
      </div>

      <br />

      <label for="idNomeUsuario">Nome de Usuario</label>
      <input
        type="text"
        id="idNomeUsuario"
        v-model="nomeUsuario"
        placeholder="Escribe o teu nome de usuario"
      />
      <div v-if="errors.nomeUsuario" style="color: red">
        {{ errors.nomeUsuario }}
      </div>

      <br />

      <label for="idContrasinal">Contrasinal</label>
      <input
        type="password"
        id="idContrasinal"
        v-model="contrasinal"
        placeholder="Escribe o teu contrasinal"
      />
      <div v-if="errors.contrasinal" style="color: red">
        {{ errors.contrasinal }}
      </div>

      <br />

      <label for="idRepiteContrasinal">Repite Contrasinal</label>
      <input
        type="password"
        id="idRepiteContrasinal"
        v-model="repiteContrasinal"
        placeholder="Repite o teu contrasinal"
      />
      <div v-if="errors.repiteContrasinal" style="color: red">
        {{ errors.repiteContrasinal }}
      </div>

      <br />

      <button type="submit">Crear conta</button>
      <p>
        Xa tes unha conta?
        <a href="#" @click="this.$router.push({ name: 'inicio' })"
          >Iniciar sesión</a
        >
      </p>
    </form>
  </div>
</template>

<style scoped>
/* Estilos opcionales */
</style>
