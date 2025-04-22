<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      medallas: [],
      primeirasMedallas: [],
      segundasMedallas: [],
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
          this.primeirasMedallas = medallas.slice(0, 5);
          this.segundasMedallas = medallas.slice(5, 10);
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
  <div>
    <h1>Medallas</h1>
    <div class="general">
      <div class="medallas-container">
        <div class="column left-column">
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

        <div class="column right-column">
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.general {
  height: 100%;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  background-color: white;
  border-radius: 5%;
  display: flex;
  justify-self: center;
  margin-right: 20px;
}

.medallas-container {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
}

.column {
  width: 48%;
}

.left-column {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.right-column {
  display: flex;
  flex-direction: column;
}

.medalla {
  margin-bottom: 10px;
}

.medalla-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.check-icon {
  font-size: 1.2em;
  color: green;
  margin-right: 5px;
}

.medalla-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

img {
  max-width: 50px;
  height: auto;
  border-radius: 10px;
}

h3 {
  font-size: 1.1em;
  margin-top: 3px;
  color: #333;
}

p {
  font-size: 0.7em;
  color: #666;
  margin-top: 2px;
}

h1 {
  color: #7f5af0;
}

#check {
  height: 4vh;
  margin-left: 20%;
}
</style>
