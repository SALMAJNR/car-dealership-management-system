import { defineStore } from "pinia"
import axios from "axios"

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    isAuthenticated: true,
    role: null
  }),

  actions: {
    async fetchMy() {
      try {
        let r = await axios.get("/api/userprofile/my/")
        this.user = r.data
        this.isAuthenticated = true
        this.role = true
      } catch (e) {
        this.user = null
        this.isAuthenticated = false
      }
    },

    async login(username, password) {
      let r = await axios.post("/api/userprofile/login/", {
        username,
        password
      })

      if (r.status === 200) {
        await this.fetchMy()
      }
    },

    async logout() {
      await axios.post("/api/userprofile/logout/")
      this.user = null
      this.isAuthenticated = false
    }
  }
})