import { createRouter, createWebHistory } from 'vue-router';
import Login from "@/components/UserLogin.vue";
import Events from "@/components/EventsList.vue";
import AdminEvents from "@/components/AdminEvents.vue";
import { auth } from "@/firebaseConfig";
import AdminUsers from '@/components/AdminUsers.vue';
//import Tickets from "@/components/TicketsList.vue";

const routes = [
  { path: "/", name: "Login", component: Login },
  { path: "/events", name: "Events", component: Events },
  { path: "/admin/events", name: "AdminEvents", component: AdminEvents },
  { path: "/admin/users", name: "AdminUsers", component: AdminUsers },
  //{ path: "/tickets", name: "Tickets", component: Tickets },
];

 const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, from, next) => {
  const adminRoutes = ["/admin", "/admin/events", "/admin/users"];
  if (adminRoutes.includes(to.path)) {
    const user = await auth.currentUser;
    const tokenResult = await user.getIdTokenResult();
    const isAdmin = tokenResult.claims.admin || false;

    if (!isAdmin) {
      alert("Unauthorized access!");
      return next("/");
    }
  }
  next();
});

export default router;
