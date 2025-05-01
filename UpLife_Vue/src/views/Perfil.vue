<script>
import Calculadora from "@/components/Calculadora.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    Calculadora,
  },
  data() {
    return {
      imagen: "",
      nome: "",
      email: "",
      nomeUsuario: "",
      xenero: "",
      altura: 0,
      peso: 0,
      obxectivo: "",
      actividade: "",
      idade: 0,
      calorias: 0,
      auga: 0,
    };
  },
  computed: {
    id() {
      const store = useUsuarioStore();
      return store.id;
    },
  },
  methods: {
    // actualizar datos do usuario cando click en Calcular de Calculadora
    async actualizarDatos() {
      if (this.id) {
        try {
          const response = await fetch(
            `http://localhost:8001/api/usuarios/${this.id}/`
          );
          const data = await response.json();

          this.imagen = data.imaxe_perfil || "/imaxes/usuario.png";
          this.nome = data.nome;
          this.email = data.email;
          this.nomeUsuario = data.nome_usuario;
          this.xenero = data.xenero;
          this.altura = data.altura;
          this.peso = data.peso;
          this.obxectivo = data.obxectivo;
          this.actividade = data.actividade;
          this.idade = data.idade;
          this.calorias = data.calorias_diarias;
          this.auga = data.auga_diaria;
        } catch (error) {
          console.error("Erro ao actualizar datos:", error);
        }
      }
    },

    // cambiar imaxe de usuario cando click enriba da imaxe de usuario
    cambiarImagen() {
      this.$refs.fileInput.click();
    },
    async subirImagen(event) {
      const archivo = event.target.files[0];
      if (!archivo) return;

      const formData = new FormData();
      formData.append("imaxe_perfil", archivo);

      try {
        const response = await fetch(
          `http://localhost:8001/api/usuarios/${this.id}/`,
          {
            method: "PATCH",
            body: formData,
          }
        );
        const resultado = await response.json();
        console.log("Imagen actualizada:", resultado);
        this.actualizarDatos();
        const store = useUsuarioStore();
        store.imagen = resultado.imaxe_perfil || "/imaxes/usuario.png";
      } catch (error) {
        console.error("Erro ao subir imaxe:", error);
      }
    },
  },
  mounted() {
    this.actualizarDatos();
  },
};
</script>

<template>
  <div class="container">
    <h1>Perfil</h1>
    <div class="perfil-layout">
      <div class="datos">
        <h2>Detalles da conta</h2>
        <p><strong>Nome:</strong> {{ nome }}</p>
        <p><strong>Email:</strong> {{ email }}</p>
        <p><strong>Nome de usuario:</strong> {{ nomeUsuario }}</p>
        <p><strong>Imaxe de usuario:</strong></p>
        <img :src="imagen" alt="Imaxe de usuario" @click="cambiarImagen()" />
        <input
          type="file"
          ref="fileInput"
          style="display: none"
          @change="subirImagen"
        />
        <h2>Datos do usuario</h2>
        <p><strong>Xénero:</strong> {{ xenero }}</p>
        <p><strong>Altura:</strong> {{ altura }} cm</p>
        <p><strong>Peso:</strong> {{ peso }} kg</p>
        <p><strong>Obxectivo:</strong> {{ obxectivo }}</p>
        <p><strong>Actividade:</strong> {{ actividade }}</p>
        <p><strong>Idade:</strong> {{ idade }} anos</p>
        <p><strong>Calorías diarias:</strong> {{ calorias }} kcal</p>
        <p id="ultimoP">
          <strong>Cantidad de auga diaria:</strong> {{ auga }} ml
        </p>
      </div>
      <div class="calculadora">
        <Calculadora @actualizarDatos="actualizarDatos" />
      </div>
    </div>
  </div>
</template>

<style scoped>
p {
  font-size: large;
}
img {
  height: 10%;
  width: 10%;
  border-radius: 50%;
}
h1 {
  font-size: xx-large;
}
h2 {
  color: #7f5af0;
  font-size: x-large;
}

html,
body {
  height: 100vh;
}

.container {
  background-color: #f2f2f2;
  display: flex;
  max-height: 70%;
  flex-direction: column;
  margin-left: 1%;
  margin-right: 1%;
  margin-bottom: 2%;
}

.perfil-layout {
  display: flex;
  flex-direction: row;
  max-height: 80%;
  justify-content: center;
  align-items: stretch;
  gap: 0; /* sin espacio explícito, el color los separa visualmente */
  margin-right: 1%;
}

/* Columna izquierda (datos) */
.datos {
  flex: 1;
  padding: 6%;
  background-color: white;
  border-radius: 2% 0 0 2%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 2%;
}

#ultimoP {
  margin-bottom: 2%; /* Añadido margen para separación adicional */
}

.datos p {
  margin: 0.8% 0;
  line-height: 20%;
}

/* Columna derecha (calculadora) */
.calculadora {
  width: 40%;
  background-color: black;
  padding: 2%;
  border-radius: 0 2% 2% 0;
  color: white;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: stretch;
}
.datos,
.calculadora {
  padding-top: 2%;
  padding-bottom: 2%;
}
</style>
