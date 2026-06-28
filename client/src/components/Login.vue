<template>
  <div class="login-page">
    <div class="login-card">

      <div class="logo">🚗</div>

      <h1>Car Dealership</h1>
      <p class="subtitle">Management System</p>

      <form @submit.prevent="login">

        <input
          v-model="username"
          type="text"
          placeholder="Username"
          required
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
        />

        <button
          type="submit"
          :disabled="loading"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>

      </form>

      <p
        v-if="error"
        class="error"
      >
        {{ error }}
      </p>

    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user";

export default {
  name: "LoginView",

  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: "",
    };
  },

  methods: {
    async login() {
      this.loading = true;
      this.error = "";

      try {
        const userStore = useUserStore();

        await userStore.login(
          this.username,
          this.password
        );

        if (userStore.isAuthenticated) {
          this.$router.push("/");
        } else {
          this.error = "Invalid username or password";
        }
      } catch (e) {
        console.error(e);
        this.error = "Login failed.";
      }

      this.loading = false;
    },
  },
};
</script>

<style scoped>

.login-page{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#020617,#0f172a,#1e3a8a);
}

.login-card{
    width:390px;
    background:#fff;
    border-radius:25px;
    padding:45px;
    text-align:center;
    box-shadow:0 20px 60px rgba(0,0,0,.3);
}

.logo{
    width:70px;
    height:70px;
    border-radius:50%;
    background:#eaf2ff;
    display:flex;
    justify-content:center;
    align-items:center;
    margin:auto;
    font-size:35px;
    margin-bottom:20px;
}

h1{
    margin:0;
    font-size:38px;
    font-weight:700;
    color:#111827;
}

.subtitle{
    color:#64748b;
    margin-bottom:30px;
}

input{
    width:100%;
    padding:15px;
    margin-bottom:18px;
    border-radius:12px;
    border:1px solid #d1d5db;
    font-size:15px;
    box-sizing:border-box;
    background:#f8fafc;
}

input:focus{
    outline:none;
    border-color:#2563eb;
    background:#fff;
}

button{
    width:100%;
    padding:15px;
    border:none;
    border-radius:12px;
    background:#2563eb;
    color:#fff;
    font-size:17px;
    font-weight:bold;
    cursor:pointer;
    transition:.3s;
}

button:hover{
    background:#1d4ed8;
}

button:disabled{
    background:#93c5fd;
    cursor:not-allowed;
}

.error{
    color:#dc2626;
    margin-top:18px;
    font-size:14px;
}

</style>