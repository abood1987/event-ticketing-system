<template>
  <v-app>
    <v-app-bar v-if="isLoggedIn" app color="primary" dark>
      <v-toolbar-title>Event Ticketing System</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="isAdmin" text @click="$router.push('/events')">Events</v-btn>
      <v-btn v-if="isAdmin" text @click="$router.push('/admin/users')">Users</v-btn>
      <v-btn v-if="isAdmin" text @click="$router.push('/admin/events')">Admin</v-btn>
      <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>
    <router-view />
  </v-app>
</template>

<script>
import { auth } from "./firebaseConfig"; // Import the correct auth object
import { onAuthStateChanged, signOut } from "firebase/auth";

export default {
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
    };
  },
  mounted() {
    onAuthStateChanged(auth, async (user) => {
      this.isLoggedIn = !!user; // Update isLoggedIn based on user presence
      if (user) {
        const tokenResult = await user.getIdTokenResult();
        this.isAdmin = tokenResult.claims.admin || false; // Check if user is admin
      } else {
        this.isAdmin = false;
      }
    });
  },
  methods: {
    logout() {
      signOut(auth)
        .then(() => {
          this.isLoggedIn = false;
          this.isAdmin = false;
          this.$router.push("/");
        })
        .catch((error) => {
          console.error("Error logging out:", error);
        });
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
