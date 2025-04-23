<script>
import Calculador from "./Calculador.vue";
export default {
  components: {
    Calculador,
  },
  data() {
    return {};
  },
};
</script>
<template>
  <div class="">
    <h3>Calculadora IMC</h3>
    <Calculador></Calculador>
    <hr />
    <h3>Calculadora de Auga e Calorias</h3>
    <form action="">
      <label for="inputXenero">Xénero</label>
      <select name="inputXenero" id="inputXenero">
        <option value="">Seleccionar</option>

        <option value="Home">Home</option>
        <option value="Muller">Muller</option>
      </select>
      <label for="inputObxectivo">Obxectivo</label>
      <select name="inputObxectivo" id="inputObxectivo">
        <option value="">Seleccionar</option>
        <option value="PerderGraxaA">Perder graxa agresivamente</option>
        <option value="PerderGraxaL">Perder graxa levemente</option>
        <option value="ManterPeso">Manter o peso</option>
        <option value="GanarMasaL">Gañar masa levemente</option>
        <option value="GanarMasaA">Gañar masa agresivamente</option>
      </select>
      <label for="inputActividade">Actividade</label>
      <select name="inputActividade" id="inputActividade">
        <option value="">Seleccionar</option>
        <option value="">Moi activo</option>
        <option value="">Activo</option>
        <option value="">Normal</option>
        <option value="">Pouco activo</option>
        <option value="">Sedentario</option>
      </select>
      <label for="inputIdade">Idade</label>
      <input type="text" id="inputIdade" placeholder="Ingresa a tua idade" />
      <button type="submit">Calcular</button>
    </form>
  </div>
</template>
<style scoped>
h1 {
  color: white;
}
.calculadora {
  max-width: 100%;
  width: 100%;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.calculadora h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: white;
  font-weight: bold;
  text-align: left;
}

.calculadora form {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  align-items: start;
}

.calculadora label {
  margin-bottom: 5px;
  color: white;
  font-weight: 500;
}

.calculadora select,
.calculadora input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #eff0f2;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  color: #043133;
  box-sizing: border-box;
}

.calculadora select::placeholder,
.calculadora input::placeholder {
  color: #838383;
}

.calculadora button {
  width: 100%;
  padding: 12px;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

.calculadora button:hover {
  background-color: #007074;
}

.calculadora p {
  margin-top: 15px;
  text-align: left; /* <-- aquí está el cambio */
  font-size: 14px;
  color: white;
}
</style>
