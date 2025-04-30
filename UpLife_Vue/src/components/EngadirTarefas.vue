<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  props: {
    dataSeleccionada: {
      type: Date,
      required: true,
    },
  },
  data() {
    return {
      tarefa: "",
      hora: "",
    };
  },
  computed: {
    id() {
      const store = useUsuarioStore();
      return store.id;
    },
    dataFormateada() {
      return this.dataSeleccionada
        .toLocaleDateString("gl-ES", {
          weekday: "long",
          year: "numeric",
          month: "long",
          day: "numeric",
        })
        .toUpperCase();
    },
    minHora() {
      const now = new Date();
      const hojeISO = now.toISOString().split("T")[0];
      const seleccionadaISO = this.dataSeleccionada.toISOString().split("T")[0];

      if (seleccionadaISO === hojeISO) {
        const horas = now.getHours().toString().padStart(2, "0");
        const minutos = now.getMinutes().toString().padStart(2, "0");
        return `${horas}:${minutos}`;
      }

      return "00:00";
    },
  },
  methods: {
    async engadirTarefa() {
      if (
        this.dataSeleccionada.toDateString() === new Date().toDateString() &&
        this.hora <= this.minHora
      ) {
      } else if (hora == "") {
      } else {
        alert("Non podes engadir unha tarefa para unha hora pasada de hoxe.");
        return;
      }

      const payload = {
        hora: this.hora === "" ? null : this.hora,
        titulo: this.tarefa,
        data: this.dataSeleccionada.toLocaleDateString("en-CA"),
        completado: false,
        usuario: this.id,
      };

      try {
        const response = await fetch("http://localhost:8001/api/tarefas/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Erro ao engadir tarefa");

        const resultado = await response.json();
        console.log("Tarefa engadida:", resultado);

        this.tarefa = "";
        this.hora = "";
        window.location.reload();
      } catch (error) {
        console.error("Erro:", error);
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <h2>Engadir tarefa</h2>
    <p class="data">
      <strong>{{ dataFormateada }}</strong>
    </p>

    <div class="formulario">
      <label for="hora">Hora</label>
      <input type="time" id="hora" v-model="hora" :min="minHora" />

      <label for="tarefa">Descrición da tarefa</label>
      <input
        type="text"
        id="tarefa"
        v-model="tarefa"
        placeholder="Escribe a túa tarefa"
      />

      <button @click="engadirTarefa">Engadir</button>
    </div>
  </div>
</template>

<style scoped>
.formulario {
  padding-top: 0;
}
.engadir-container {
  background-color: black;
  padding: 7%;
  border-radius: 12px;
  margin: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  text-align: left;
  display: flex;
  flex-direction: column;
}

h2 {
  color: #7f5af0;
  font-size: 24px;
}

.data {
  color: white;
  font-weight: 500;
}

label {
  margin: 3% 0 1%;
  font-weight: 500;
  color: white;
}

input,
select {
  padding: 3%;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: medium;
  width: 100%;
  box-sizing: border-box; /* 🔹 asegura que el padding no sume al width */
}

button {
  padding: 3%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  box-sizing: border-box; /* 🔹 asegura que el padding no sume al width */
}

button:hover {
  background-color: #3461cc;
}
</style>
