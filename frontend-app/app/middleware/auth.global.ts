export default defineNuxtRouteMiddleware(async (to, from) => {
    const withoutAuthRoutes = ["login", "register", "index"];

    const authStore = useAuthStore();

    await authStore.initPromise;

    if (!authStore.isAuthenticated) {
        if (!withoutAuthRoutes.includes(to.name as string)) {
            return navigateTo("/login");
        }
    } else if (withoutAuthRoutes.includes(to.name as string)) {
        return navigateTo("/my");
    }
});
