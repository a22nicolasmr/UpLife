import { defineStore } from "pinia";

export const useUsuarioStore = defineStore("usuario", {
  state: () => ({
    id: null,
    nome: "",
    imagen: "/imaxes/usuario.png",
    medallas: 0,
  }),
  actions: {
    async cargarUsuario(nome) {
      try {
        const response = await fetch("http://localhost:8001/api/usuarios/");
        const usuarios = await response.json();
        const usuario = usuarios.find((u) => u.nome_usuario === nome);
        if (!usuario) return;

        this.id = usuario.id_usuario;
        this.nome = usuario.nome;
        this.imagen = usuario.imaxe_perfil || "/imaxes/usuario.png";

        // Guarda solo lo necesario en localStorage
        localStorage.setItem(
          "usuario",
          JSON.stringify({
            id: this.id,
            nome: this.nome,
          })
        );

        // Carga medallas
        await this.cargarMedallas();
      } catch (error) {
        console.error("Error cargando datos del usuario:", error);
      }
    },

    async cargarMedallas() {
      try {
        const medallasRes = await fetch("http://localhost:8001/api/medallas/");
        const medallas = await medallasRes.json();
        this.medallas = medallas.filter(
          (m) => m.usuarios.includes(this.id) && m.completado
        ).length;
      } catch (error) {
        console.error("Error cargando medallas:", error);
      }
    },

    cargarDesdeStorage() {
      const datos = localStorage.getItem("usuario");
      if (datos) {
        const { id, nome } = JSON.parse(datos);
        this.id = id;
        this.nome = nome;
        this.cargarMedallas(); // Cargar medallas al restaurar
      }
    },

    cerrarSesion() {
      localStorage.removeItem("usuario");
      this.id = null;
      this.nome = "";
      this.imagen = "/imaxes/usuario.png";
      this.medallas = 0;
    },
  },
  // Al crear el store, cargamos los datos desde localStorage si existen
  persist: true,
});
