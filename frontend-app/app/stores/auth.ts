import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useApi } from "~/composables/useApi";

export const useAuthStore = defineStore("auth", () => {
    const api = useApi();

    const token = ref<string | null>(localStorage.getItem("access_token"));
    const currentUser = ref<any | null>(null);

    const isAuthenticated = computed(() => !!token.value);

    function setToken(t: string | null) {
        token.value = t;
        if (t) {
            localStorage.setItem("access_token", t);
        } else {
            localStorage.removeItem("access_token");
        }
    }

    async function loadCurrentUser() {
        try {
            const data = await api.GET("/api/v1/users/me");
            currentUser.value = data;
            return { ok: true, data };
        } catch (error) {
            currentUser.value = null;
            return { ok: false, error };
        }
    }

    async function login(payload: { username: string; password: string }) {
        const fd = new FormData();
        fd.append("username", payload.username);
        fd.append("password", payload.password);

        const res = await api.POST("/api/v1/auth/login", {
            // TODO поправить formdata на json
            // @ts-ignore
            body: fd,
        });

        if (!res.error && res.data && (res.data as any).access_token) {
            setToken((res.data as any).access_token);
            await loadCurrentUser();
            return { ok: true, data: res.data };
        }

        return { ok: false, error: res.error || res.data };
    }

    async function register(payload: { email: string; username: string; password: string }) {
        const res = await api.POST("/api/v1/auth/register", {
            body: {
                email: payload.email,
                username: payload.username,
                password: payload.password,
                user_role: "customer",
            },
        });

        if (!res.error && res.data) {
            return { ok: true, data: res.data };
        }

        return { ok: false, error: res.error };
    }

    async function logout() {
        setToken(null);
        currentUser.value = null;
    }

    if (token.value) {
        loadCurrentUser();
    }

    return {
        token,
        currentUser,
        isAuthenticated,
        login,
        register,
        logout,
        loadCurrentUser,
        setToken,
    };
});
