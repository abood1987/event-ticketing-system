<template>
  <v-container>
    <h1 class="text-center mb-5">Admin Events</h1>
    <v-btn fab color="primary" class="mb-5" @click="openCreateModal">
      <v-icon icon="mdi-plus" />
    </v-btn>
    <v-list dense>
      <v-list-item v-for="event in events" :key="event.id" class="mb-3">
        <v-card class="w-100 primary-border" outlined>
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <span class="font-weight-bold">{{ event.name }}</span>
              <span>{{ formatDatetime(event.datetime) }} | ${{ event.price }}</span>
              <v-btn color="red" @click="deleteEvent(event.id)">Delete</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-list-item>
    </v-list>

    <!-- Create Event Modal -->
    <v-dialog v-model="isCreateModalOpen" max-width="500">
      <v-card>
        <v-card-title class="text-h5">Create Event</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="newEvent.name" label="Event Name" required></v-text-field>
            <v-text-field v-model="newEvent.location" label="Location" required></v-text-field>
            <v-text-field v-model="newEvent.datetime" label="Datetime" type="datetime-local" required></v-text-field>
            <v-text-field
              v-model="newEvent.totalTickets"
              label="Total Tickets"
              type="number"
              required
            ></v-text-field>
            <v-text-field v-model="newEvent.price" label="Price" type="number" required></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeCreateModal">Cancel</v-btn>
          <v-btn color="primary" @click="createEvent">Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { auth } from "@/firebaseConfig";

export default {
  data() {
    return {
      events: [],
      isCreateModalOpen: false,
      newEvent: {
        name: "",
        location: "",
        datetime: "",
        totalTickets: 0,
        price: 0,
      },
    };
  },
  mounted() {
    this.fetchEvents();
  },
  methods: {
    async fetchEvents() {
      const token = await this.getAuthToken();
      try {
        const response = await this.$http.get("/events", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.events = response.data.map((event) => ({
          ...event,
          id: event.id || event.event_id,
        }));
      } catch (error) {
        console.error("Failed to fetch events:", error);
      }
    },
    async deleteEvent(eventId) {
      if (!confirm("Are you sure you want to delete this event?")) return;

      const token = await this.getAuthToken();
      try {
        await this.$http.delete(`/events/${eventId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Event deleted successfully!");
        this.fetchEvents();
      } catch (error) {
        console.error("Failed to delete event:", error);
        alert("Failed to delete event.");
      }
    },
    async createEvent() {
      const token = await this.getAuthToken();
      try {
        const event = {
          name: this.newEvent.name,
          location: this.newEvent.location,
          datetime: this.newEvent.datetime,
          total_tickets: this.newEvent.totalTickets,
          price: this.newEvent.price,
        };
        await this.$http.post("/events", event, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Event created successfully!");
        this.closeCreateModal();
        this.fetchEvents();
      } catch (error) {
        console.error("Failed to create event:", error);
        alert("Failed to create event.");
      }
    },
    openCreateModal() {
      this.isCreateModalOpen = true;
    },
    closeCreateModal() {
      this.isCreateModalOpen = false;
    },
    async getAuthToken() {
      const user = auth.currentUser;
      if (!user) throw new Error("User not authenticated");
      return user.getIdToken();
    },
    formatDatetime(datetime) {
      return new Date(datetime).toLocaleString();
    },
  },
};
</script>

<style scoped>
.primary-border {
  border: 2px solid #1976d2; /* Vuetify primary color */
  border-radius: 5px;
}
</style>
