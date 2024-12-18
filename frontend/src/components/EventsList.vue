<template>
  <v-container class="mt-5">
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <h1 class="text-center mb-5">Events</h1>
        <v-list dense>
          <v-list-item v-for="event in events" :key="event.id" class="mb-3">
            <v-card class="w-100 primary-border" outlined>
              <v-card-text>
                <!-- Event Details -->
                <div class="d-flex justify-space-between align-center">
                  <span class="font-weight-bold">
                    {{ event.name }} (Price: ${{ event.price }})
                  </span>
                  <v-btn icon @click.stop="openPaymentModal(event)">
                    <v-icon color="primary" icon="mdi-cash" />
                  </v-btn>
                </div>
                <div class="d-flex justify-space-between align-center mt-2">
                  <span class="text-muted">
                    {{ event.location }} (Remaining {{ event.ticketsRemaining }} tickets)
                  </span>
                  <span class="text-muted">{{ formatDateTime(event.datetime) }}</span>
                </div>
              </v-card-text>
            </v-card>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>

    <!-- Payment Modal -->
    <v-dialog v-model="isPaymentModalOpen" max-width="400">
      <v-card>
        <v-card-title class="text-h5">Buy Tickets</v-card-title>
        <v-card-text>
          <div>
            <p><strong>Event:</strong> {{ selectedEvent.name }}</p>
            <p><strong>Available Tickets:</strong> {{ selectedEvent.ticketsRemaining }}</p>
            <p><strong>Price Per Ticket:</strong> ${{ selectedEvent.price }}</p>
          </div>
          <v-text-field
            v-model="numberOfTickets"
            label="Number of Tickets"
            type="number"
            min="1"
            :max="selectedEvent.ticketsRemaining"
            required
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closePaymentModal">Cancel</v-btn>
          <v-btn :loading="isLoading" color="primary" @click="payTickets">Pay</v-btn>
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
      isPaymentModalOpen: false,
      selectedEvent: {},
      numberOfTickets: 1,
      isLoading: false, // Loading state for API calls
    };
  },
  mounted() {
    this.fetchEvents();
  },
  methods: {
    async fetchEvents() {
      try {
        const response = await this.$http.get("/events");
        this.events = response.data.map((event) => ({
          ...event,
          id: event.id || event.event_id, // Map backend ID if necessary
        }));
        console.log("Fetched events:", this.events);
      } catch (error) {
        console.error("Failed to fetch events:", error);
      }
    },
    formatDateTime(date) {
      const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    openPaymentModal(event) {
      this.selectedEvent = event;
      this.numberOfTickets = 1;
      this.isPaymentModalOpen = true;
    },
    closePaymentModal() {
      this.isPaymentModalOpen = false;
    },
    async payTickets() {
      if (this.numberOfTickets > this.selectedEvent.ticketsRemaining) {
        alert("Not enough tickets available!");
        return;
      }

      console.log(this.selectedEvent.id);
      const ticketsToBuy = this.numberOfTickets;
      this.isLoading = true;

      try {
        const token = await this.getAuthToken();
        await this.$http.post(
          "/purchase",
          { event_id: this.selectedEvent.id, tickets: ticketsToBuy },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        alert(`Successfully purchased ${ticketsToBuy} tickets!`);
        this.selectedEvent.ticketsRemaining -= ticketsToBuy; // Update tickets locally
        this.closePaymentModal();
      } catch (error) {
        console.error("Payment failed:", error);
        alert(error.response?.data?.message || "Failed to purchase tickets. Please try again.");
      } finally {
        this.isLoading = false;
      }
    },
    async getAuthToken() {
      const user = auth.currentUser;
      if (!user) {
        throw new Error("User not authenticated");
      }
      return await user.getIdToken(); // Retrieve the user's ID token
    },
  },
};
</script>

<style scoped>
.text-muted {
  font-size: 0.9rem;
  color: gray;
}

.text-primary {
  font-size: 1rem;
  color: #1976d2; /* Vuetify primary color */
}

.font-weight-bold {
  font-weight: bold;
}

.primary-border {
  border: 2px solid #1976d2; /* Vuetify primary color */
  border-radius: 5px;
}
</style>
