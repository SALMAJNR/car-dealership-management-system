<template>
  <div>
    <form @submit.prevent.stop="login">
      <input type="text" v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />
      <button type="submit">LOGIN</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"
import { useUserStore } from "../stores/user"

const username = ref("")
const password = ref("")

const router = useRouter()
const userStore = useUserStore()

async function login() {
 
    let r = await axios.post("/api/userprofile/login/", {
      username: username.value,
      password: password.value
    })

    if (r.status === 200) {
      await userStore.fetchMy()
      router.push("/")
    }
 
}
</script>