<template>
  <div class="login-page">
    <div class="login-card">
      <div class="logo">🚗</div>

      <h1>Car Dealership</h1>
      <p>Management System</p>

      <form @submit.prevent="login">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />

        <button type="submit" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginView",

  data() {
    return {
      username: "",
      password: "",
      error: "",
      loading: false,
    };
  },

  methods: {
    async login() {
      this.error = "";
      this.loading = true;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/userprofile/login/",
          {
            username: this.username,
            password: this.password,
          },
          {
            withCredentials: true,
          }
        );

        if (response.data.success) {
          localStorage.setItem("username", this.username);
          window.location.href = "/";
        } else {
          this.error = "Invalid username or password";
        }
      } catch (error) {
        this.error = "Invalid username or password";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #020617, #0f172a, #1e3a8a);
  font-family: Arial, sans-serif;
}

.login-card {
  width: 390px;
  padding: 42px;
  background: #ffffff;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.35);
}

.logo {
  width: 70px;
  height: 70px;
  margin: 0 auto 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eff6ff;
  border-radius: 50%;
  font-size: 34px;
}

h1 {
  margin: 0;
  color: #0f172a;
  font-size: 30px;
  font-weight: 800;
}

p {
  margin: 10px 0 28px;
  color: #64748b;
  font-size: 15px;
}

input {
  width: 100%;
  padding: 15px;
  margin-bottom: 16px;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  font-size: 15px;
  box-sizing: border-box;
  background: #f8fafc;
}

input:focus {
  outline: none;
  border-color: #2563eb;
  background: white;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

button {
  width: 100%;
  padding: 15px;
  border: none;
  border-radius: 12px;
  background: #2563eb;
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
}

button:hover {
  background: #1d4ed8;
}

button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.error {
  margin-top: 18px;
  color: #dc2626;
  font-size: 14px;
}
</style>