 import { defineStore } from "pinia"
import axios from "axios"

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    isAuthenticated: false,
    role: null
  }),

  actions: {
    async fetchMy() {
      try {
        const r = await axios.get("/api/userprofile/my/", {
          withCredentials: true
        })

        this.user = r.data
        this.isAuthenticated = true
        this.role = r.data.role
      } catch (e) {
        this.user = null
        this.isAuthenticated = false
        this.role = null
      }
    },

    async login(username, password) {
      const r = await axios.post(
        "/api/userprofile/login/",
        { username, password },
        { withCredentials: true }
      )

      if (r.data.success) {
        this.user = r.data.user
        this.isAuthenticated = true
        this.role = r.data.user.role
      }
    },

    async logout() {
      await axios.post(
        "/api/userprofile/logout/",
        {},
        { withCredentials: true }
      )

      this.user = null
      this.isAuthenticated = false
      this.role = null
    }
  }
})