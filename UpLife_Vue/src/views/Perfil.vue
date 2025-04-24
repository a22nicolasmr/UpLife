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
        <p>
          Xénero: <strong>{{ xenero }}</strong>
        </p>
        <p>
          Altura: <strong>{{ altura }} cm</strong>
        </p>
        <p>
          Peso: <strong>{{ peso }} kg</strong>
        </p>
        <p>
          Obxectivo: <strong>{{ obxectivo }}</strong>
        </p>
        <p>
          Actividade: <strong>{{ actividade }}</strong>
        </p>
        <p>
          Idade: <strong>{{ idade }} anos</strong>
        </p>
        <p>
          Calorías diarias: <strong>{{ calorias }} kcal</strong>
        </p>
        <p>
          Cantidade de auga diaria: <strong>{{ auga }} ml</strong>
        </p>
      </div>
      <div class="calculadora">
        <Calculadora @actualizarDatos="actualizarDatos" />
      </div>
    </div>
  </div>
</template>

<style scoped>
img {
  height: 8vh;
  width: 8vh;
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
