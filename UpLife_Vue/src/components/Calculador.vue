<script>
export default {
  emits: ["updateAltura", "updatePeso"],
  data() {
    return {
      altura: 170,
      peso: 72,
    };
  },
  watch: {
    altura(nuevaAltura) {
      this.$emit("updateAltura", nuevaAltura);
    },
    peso(nuevoPeso) {
      this.$emit("updatePeso", nuevoPeso);
    },
  },
  computed: {
    imc() {
      const alturaM = this.altura / 100;
      return this.peso / (alturaM * alturaM);
    },
    estadoIMC() {
      const v = this.imc;
      if (v < 18.5) return "Baixo peso";
      if (v < 25) return "Saudable";
      if (v < 30) return "Sobrepeso";
      return "Obesidade";
    },
  },
  methods: {
    calcularPosicion() {
      const min = 10;
      const max = 40;
      const imc = this.imc;
      const percent = ((imc - min) / (max - min)) * 100;
      return Math.min(100, Math.max(0, percent));
    },
  },
};
</script>

s
<template>
  <div class="imc-wrapper">
    <div class="inputs">
      <div class="input-box altura">
        <label>Altura</label>
        <input type="range" min="100" max="220" v-model="altura" />
        <div>{{ altura }} cm</div>
      </div>
      <div class="input-box peso">
        <label>Peso</label>
        <input type="range" min="30" max="150" v-model="peso" />
        <div>{{ peso }} kg</div>
      </div>
    </div>
    <div class="resultado">
      <p>Índice de Masa Corporal (IMC)</p>
      <div class="valor-imc">{{ imc.toFixed(1) }}</div>
      <div class="etiqueta">{{ estadoIMC }}</div>
      <div class="barra-imc">
        <div
          class="indicador"
          :style="{ left: calcularPosicion() + '%' }"
        ></div>
      </div>
      <div class="valores">
        <span>5</span><span>18.5</span><span>25</span><span>30</span
        ><span>40</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.imc-wrapper {
  display: flex;
  gap: 20px;
  align-items: stretch; /* <-- hace que ambos lados tengan misma altura */
  color: white;
  height: 31%;
}

.inputs {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
  height: 100%; /* <-- clave para que iguale a .resultado */
}

.input-box {
  flex: 1; /* <-- reparte el espacio entre los dos */
  background-color: #ffe5b4;
  padding: 16px;
  border-radius: 20px 0 0 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: black;
}

.peso {
  background-color: #caf0f8;
}
.resultado {
  background-color: #2d2d2d;
  border-radius: 0 20px 20px 0;
  padding: 20px;
  flex: none;
  width: 230px; /* <-- ajustá el ancho al deseado */
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.valor-imc {
  font-size: 32px;
  font-weight: bold;
  margin: 10px 0;
}

.etiqueta {
  background-color: #b2f2bb;
  padding: 5px 10px;
  border-radius: 12px;
  display: inline-block;
  font-weight: bold;
}

.barra-imc {
  height: 10px;
  background: linear-gradient(to right, #00b4d8, #90e0ef, #ffe066, #ff6b6b);
  border-radius: 10px;
  position: relative;
  margin: 10px 0;
  width: 100%;
}

.indicador {
  position: absolute;
  top: -5px;
  width: 10px;
  height: 20px;
  background-color: red;
  border-radius: 3px;
}
.valores {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #ccc;
}
</style>
