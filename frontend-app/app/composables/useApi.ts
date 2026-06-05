import createClient from "openapi-fetch";
import type { paths } from "~/api/types";

const BASE_URL = "http://localhost:8000";

let refreshPromise: Promise<boolean> | null = null;

async function tryRefresh(): Promise<boolean> {
    if (refreshPromise) return refreshPromise;
    refreshPromise = fetch(`${BASE_URL}/api/v1/auth/refresh`, {
        method: "POST",
        credentials: "include",
    })
        .then((r) => r.ok)
        .catch(() => false)
        .finally(() => { refreshPromise = null; });
    return refreshPromise;
}

export function useApi() {
    const client = createClient<paths>({
        baseUrl: BASE_URL,
        credentials: "include",
    });

    client.use({
        async onResponse({ response, request }) {
            if (response.status !== 401) return response;
            if (request.url.includes("/auth/refresh")) return response;

            // На сервере редирект обрабатывает auth.global.ts
            if (import.meta.server) return response;

            const ok = await tryRefresh();
            if (!ok) {
                useAuthStore().clearUser();
                await navigateTo("/login");
                return response;
            }

            return fetch(request.clone());
        },
    });

    return client;
}
