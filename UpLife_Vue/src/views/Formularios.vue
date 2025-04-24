<template>
  <div class="contenedor">
    <div class="izquierda">
      <img src="/imaxes/imagen4.png" alt="" />
    </div>

    <div class="derecha">
      <!-- cargar formularios -->
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "Formularios",
};
</script>

<style>
.contenedor {
  display: flex;
  height: 100%;
  width: 100%;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}
.izquierda img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.izquierda,
.derecha {
  width: 50%;
  padding: 40px;
  box-sizing: border-box;
}

.izquierda {
  background-color: #e6f0ff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.derecha {
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 0;
  height: 100%;
}

.formulario {
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
  padding-top: 40px;
}

.formulario h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #043133;
  font-weight: bold;
  text-align: center;
}

.formulario label {
  display: block;
  margin-bottom: 5px;
  color: #043133;
  font-weight: 500;
}

.formulario input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #eff0f2;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  color: #043133;
}

.formulario input::placeholder {
  color: #838383;
}

.formulario button {
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
}

.formulario button:hover {
  background-color: #007074;
}

.formulario p {
  margin-top: 15px;
  text-align: center;
  font-size: 14px;
  color: #4d5959;
}

.formulario a {
  color: #007074;
  text-decoration: none;
  font-weight: bold;
}

.formulario a:hover {
  text-decoration: underline;
}
body {
  height: 100vh;
  width: 100vw;
  margin: 0;
}

html,
body,
#app {
  height: 100%;
  margin: 0;
}
</style>
