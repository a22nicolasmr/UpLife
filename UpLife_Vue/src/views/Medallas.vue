<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      medallas: [],
      primeirasMedallas: [],
      segundasMedallas: [],
      terceirasMedallas: [],
    };
  },
  computed: {
    usuarioId() {
      const store = useUsuarioStore();
      return store.id;
    },
  },
  mounted() {
    this.obterMedallas();
  },
  methods: {
    async obterMedallas() {
      try {
        const response = await fetch("http://localhost:8001/api/medallas/");
        const medallas = await response.json();

        if (medallas) {
          this.medallas = medallas;
          const total = medallas.length;
          const tercio = Math.ceil(total / 3);
          this.primeirasMedallas = medallas.slice(0, tercio);
          this.segundasMedallas = medallas.slice(tercio, tercio * 2);
          this.terceirasMedallas = medallas.slice(tercio * 2, total);
        }
      } catch (error) {
        console.error("Error cargando datos de medallas:", error);
      }
    },
    medallaCompletadaPorUsuario(medalla) {
      return medalla.usuarios.includes(this.usuarioId) && medalla.completado;
    },
  },
};
</script>

<template>
  <div id="todo">
    <h1>Medallas</h1>
    <div class="general">
      <div class="medallas-container">
        <div class="column">
          <div
            v-for="medalla in primeirasMedallas"
            :key="medalla.id_medalla"
            class="medalla"
          >
            <div class="medalla-content">
              <div
                v-if="medallaCompletadaPorUsuario(medalla)"
                class="check-icon"
              >
                <img src="/imaxes/check.png" alt="Check" id="check" />
              </div>
              <div v-else>
                <img
                  src="/imaxes/invisible.PNG"
                  alt="Invisible"
                  id="invisible"
                />
              </div>
              <div class="medalla-info">
                <img :src="medalla.icona" alt="Icona medalla" />
                <div>
                  <h3>{{ medalla.nome }}</h3>
                  <p>{{ medalla.descripcion }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div
            v-for="medalla in segundasMedallas"
            :key="medalla.id_medalla"
            class="medalla"
          >
            <div class="medalla-content">
              <div
                v-if="medallaCompletadaPorUsuario(medalla)"
                class="check-icon"
              >
                <img src="/imaxes/check.png" alt="Check" id="check" />
              </div>
              <div v-else>
                <img
                  src="/imaxes/invisible.PNG"
                  alt="Invisible"
                  id="invisible"
                />
              </div>
              <div class="medalla-info">
                <img :src="medalla.icona" alt="Icona medalla" />
                <div>
                  <h3>{{ medalla.nome }}</h3>
                  <p>{{ medalla.descripcion }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div
            v-for="medalla in terceirasMedallas"
            :key="medalla.id_medalla"
            class="medalla"
          >
            <div class="medalla-content">
              <div
                v-if="medallaCompletadaPorUsuario(medalla)"
                class="check-icon"
              >
                <img src="/imaxes/check.png" alt="Check" id="check" />
              </div>
              <div v-else>
                <img
                  src="/imaxes/invisible.PNG"
                  alt="Invisible"
                  id="invisible"
                />
              </div>
              <div class="medalla-info">
                <img :src="medalla.icona" alt="Icona medalla" />
                <div>
                  <h3>{{ medalla.nome }}</h3>
                  <p>{{ medalla.descripcion }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.general {
  width: 95%;
  height: 70%;
  padding: 2vw;
  box-sizing: border-box;
  background-color: white;
  border-radius: 1vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.medallas-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2vw;
  width: 100%;
  justify-content: center;
  height: 100%;
}

.column {
  flex: 1 1 30%;
  display: flex;
  flex-direction: column;
  gap: 1.5vh;
}

.medalla {
  display: flex;
  align-items: stretch; /* Asegura que todos los elementos se estiren */
  flex-direction: column;
  height: 100%; /* Hace que las medallas tengan el mismo alto */
}

.medalla-content {
  display: flex;
  align-items: center;
  gap: 1vw;
  height: 100%;
}

.check-icon,
#invisible {
  margin-right: 0.5vw;
  flex-shrink: 0; /* Evita que las imágenes se deformen */
}

.medalla-info {
  display: flex;
  align-items: center;
  gap: 1vw;
  flex-grow: 1; /* Hace que el texto ocupe el espacio restante */
}

.medalla-info img {
  width: 4vw;
  height: 4vw;
  object-fit: cover;
  border-radius: 8%;
  flex-shrink: 0; /* Para que la imagen no se deforme */
}

.medalla-info div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%; /* Asegura que los textos se alineen con la imagen */
}

img {
  max-width: 5vw;
  min-width: 1vw;
  border-radius: 8%;
}

h1 {
  font-size: x-large;
  margin-bottom: 3vh;
  color: #7f5af0;
}

h3 {
  font-size: 1.5vw;
  margin: 0;
  color: #333;
}

p {
  font-size: 1vw;
  margin: 0;
  color: #666;
}

#check,
#invisible {
  height: 3vh;
  margin-left: 2vw;
}

#todo {
  display: flex;
  flex-direction: column;
  margin-left: 2%;
  height: 100%;
}
</style>
