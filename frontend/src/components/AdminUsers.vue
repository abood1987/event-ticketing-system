<template>
    <v-container>
      <h1 class="text-center mb-5">User Management</h1>
      <v-list dense>
        <v-list-item
          v-for="user in users"
          :key="user.uid"
          class="mb-3"
        >
          <v-card class="w-100">
            <v-card-text>
              <div class="d-flex justify-space-between align-center">
                <span class="font-weight-bold">{{ user.email }}</span>
                <div>
                  <v-btn
                    v-if="!user.admin"
                    color="primary"
                    @click="setAdmin(user.uid)"
                  >
                    Set Admin
                  </v-btn>
                  <v-btn
                    v-if="user.admin"
                    color="red"
                    @click="removeAdmin(user.uid)"
                  >
                    Remove Admin
                  </v-btn>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-list-item>
      </v-list>
    </v-container>
  </template>
  
  <script>
  import { auth } from "@/firebaseConfig";
  
  export default {
    data() {
      return {
        users: [],
      };
    },
    async mounted() {
      await this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const token = await this.getAuthToken();
          const response = await this.$http.get("/admin/users", {
            headers: { Authorization: `Bearer ${token}` },
          });
          const currentUser = await auth.currentUser.uid;
          this.users = response.data.filter(user => user.uid !== currentUser);
        } catch (error) {
          console.error("Failed to fetch users:", error);
        }
      },
      async setAdmin(uid) {
        try {
          const token = await this.getAuthToken();
          await this.$http.post(
            "https://REGION-PROJECT.cloudfunctions.net/setAdmin",
            { uid },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          alert("Admin role granted!");
          this.fetchUsers();
        } catch (error) {
          console.error("Failed to set admin role:", error);
          alert("Failed to set admin role.");
        }
      },
      async removeAdmin(uid) {
        try {
          const token = await this.getAuthToken();
          await this.$http.post(
            "https://REGION-PROJECT.cloudfunctions.net/removeAdmin",
            { uid },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          alert("Admin role revoked!");
          this.fetchUsers();
        } catch (error) {
          console.error("Failed to remove admin role:", error);
          alert("Failed to remove admin role.");
        }
      },
      async getAuthToken() {
        const user = auth.currentUser;
      if (!user) throw new Error("User not authenticated");
      return user.getIdToken();
      },
    },
  };
  </script>
  
  <style scoped>
  .font-weight-bold {
    font-weight: bold;
  }
  </style>
  