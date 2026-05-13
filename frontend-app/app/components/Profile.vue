<template>
    <div class="box">
        <h3>Данные</h3>
        <div class="field">
            <div class="label">Почта:</div>
            <div class="value">{{ user?.email }}</div>
        </div>
        <div class="field">
            <div class="label">Роль:</div>
            <div class="value">{{ user?.user_role }}</div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import type { paths } from "~/api/types";

const api = useApi();

const user = ref<paths["/api/v1/users/me"]["get"]["responses"]["200"]["content"]["application/json"] | null>(null);

try {
    const data = await api.GET("/api/v1/users/me");
    if (data.response && data.data) {
        user.value = data.data;
    } else {
        console.error("Failed to fetch user data", data.error);
    }
} catch (error) {
    console.error("An error occurred while fetching user data", error);
}
</script>
<style lang="scss" scoped>
@use "@/assets/scss/profile.scss";
</style>
