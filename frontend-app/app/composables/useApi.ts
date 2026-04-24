import createClient from "openapi-fetch";
import type { paths } from "~/api/types";

export function useApi() {
    const client = createClient<paths>({
        baseUrl: "http://localhost:8000",
    });

    client.use({
        onRequest(options) {
            const token = localStorage.getItem("access_token");
            if (token) {
                options.request.headers.append("Authorization", `Bearer ${token}`);
            }
        },
    });

    return client;
}
