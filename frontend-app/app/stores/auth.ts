import { defineStore } from "pinia";
import { useApi } from "~/composables/useApi";

export const useAuthStore = defineStore("auth", () => {
    const api = useApi();

    const currentUser = ref<any | null>(null);
    const isAuthenticated = ref(false);

    let _initResolve: () => void;
    const initPromise = new Promise<void>((resolve) => {
        _initResolve = resolve;
    });

    function clearUser() {
        currentUser.value = null;
        isAuthenticated.value = false;
    }

    async function loadCurrentUser() {
        const { data, error } = await api.GET("/api/v1/users/me");
        if (data && !error) {
            currentUser.value = data;
            isAuthenticated.value = true;
            return { ok: true };
        }
        clearUser();
        return { ok: false };
    }

    async function login(payload: { email: string; password: string }) {
        const { data, error } = await api.POST("/api/v1/auth/login", {
            body: payload,
        });

        if (data && !error) {
            currentUser.value = data;
            isAuthenticated.value = true;
            return { ok: true };
        }

        return { ok: false, error };
    }

    async function register(payload: { email: string; username: string; password: string }) {
        const { data, error } = await api.POST("/api/v1/auth/register", {
            body: { ...payload, user_role: "customer" },
        });

        if (data && !error) {
            return { ok: true, data };
        }

        return { ok: false, error };
    }

    async function logout() {
        await api.POST("/api/v1/auth/logout", {});
        clearUser();
    }

    async function init() {
        await loadCurrentUser();
        _initResolve();
    }

    init();

    return {
        currentUser,
        isAuthenticated,
        initPromise,
        login,
        register,
        logout,
        clearUser,
        loadCurrentUser,
    };
});
