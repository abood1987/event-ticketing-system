<template>
  <v-container class="d-flex justify-center align-center fill-height">
    <v-card class="pa-4" elevation="16" max-width="512" width="100%">
      <v-toolbar dark color="primary">
        <v-toolbar-title>Login Form</v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <form ref="form" @submit.prevent="login">
          <v-text-field
            v-model="email"
            name="email"
            label="Email"
            type="text"
            placeholder="Enter your email"
            required
          ></v-text-field>
          <v-text-field
            v-model="password"
            name="password"
            label="Password"
            type="password"
            placeholder="Enter your password"
            required
          ></v-text-field>
          <v-btn type="submit" class="mt-4" color="primary" block>Login</v-btn>
        </form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebaseConfig";

export default {
  data() {
    return {
      email: "",
      password: "",
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const userCredential = await signInWithEmailAndPassword(auth, this.email, this.password);
        alert(`Welcome, ${userCredential.user.email}!`);
        this.$router.push("/events");
      } catch (error) {
        this.error = error.message;
        console.error("Login error:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Full height for the container */
.fill-height {
  height: 100vh;
}

/* Ensure the card takes up a wider width */
.v-card {
  width: 100%;
  max-width: 512px;
}
</style>
