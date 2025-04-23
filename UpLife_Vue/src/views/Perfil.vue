<script>
import Calculadora from "@/components/Calculadora.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    Calculadora,
  },
  data() {
    return {
      imagen: "", // <- acá se guarda la URL de la imagen
      nome: "",
      email: "",
      nomeUsuario: "",
    };
  },
  computed: {
    id() {
      const store = useUsuarioStore();
      return store.id;
    },
  },
  async mounted() {
    if (this.id) {
      try {
        const response = await fetch(
          `http://localhost:8001/api/usuarios/${this.id}/`
        );
        const data = await response.json();

        // Asegurate de que el campo correcto se llama 'imaxe_perfil' o algo similar
        this.imagen = data.imaxe_perfil || "/imaxes/usuario.png";
        this.nome = data.nome;
        this.email = data.email;
        this.nomeUsuario = data.nome_usuario;
      } catch (error) {
        console.error("Erro ao obter imaxe do usuario:", error);
        this.imagen = "/imaxes/usuario.png";
      }
    }
  },
};
</script>

<template>
  <div class="container">
    <div class="perfil-layout">
      <div class="datos">
        <h2>Detalles da conta</h2>
        <p><strong>Nome:</strong> {{ nome }}</p>
        <p><strong>Email:</strong> {{ email }}</p>
        <p><strong>Nome de usuario:</strong> {{ nomeUsuario }}</p>
        <p><strong>Imaxe de usuario:</strong></p>
        <img :src="imagen" alt="Imaxe de usuario" />

        <h2>Datos do usuario</h2>
        <p>Peso:</p>
        <p>Obxectivo:</p>
        <p>Actividade:</p>
        <p>Idade:</p>
        <p>Calorías diarias:</p>
        <p>Cantidade de auga diaria:</p>
      </div>
      <div class="calculadora">
        <Calculadora />
      </div>
    </div>
  </div>
</template>

<style scoped>
img {
  height: 10vh;
  width: 10vh;
  border-radius: 50%;
}
h2 {
  color: #7f5af0;
}

html,
body {
  height: 100vh;
}
.container {
  background-color: #f2f2f2;
}

.perfil-layout {
  max-height: 89vh;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: stretch;
  gap: 0; /* sin espacio explícito, el color los separa visualmente */
  margin-right: 14px;
}

/* Columna izquierda (datos) */
.datos {
  flex: 1;
  padding: 20px;
  background-color: white;
  border-radius: 10px 0 0 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-height: 83vh; /* <-- Ajustá este valor según lo que necesites */
}

.datos p {
  margin: 8px 0;
  line-height: 1.2;
}

/* Columna derecha (calculadora) */
.calculadora {
  width: 40%;
  background-color: black;
  padding: 20px;
  border-radius: 0 10px 10px 0;
  color: white;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: stretch;
}
.datos,
.calculadora {
  padding-top: 40px;
  padding-bottom: 40px;
}
</style>
