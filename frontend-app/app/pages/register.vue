<template>
    <div class="page">
        <h2>Создание аккаунта</h2>
        <form
            class="auth-form"
            @submit.prevent="onSubmit">
            <UiInput
                v-model="models.username"
                :schema="schemas.username"
                placeholder="Имя" />
            <UiInput
                v-model="models.email"
                :schema="schemas.email"
                placeholder="Почта"
                type="email" />
            <UiInput
                v-model="models.password"
                :schema="schemas.password"
                placeholder="Пароль"
                type="password" />
            <UiButton type="submit">Создать</UiButton>
        </form>
    </div>
</template>
<script lang="ts" setup>
import z from "zod";

const api = useApi();

const models = {
    email: {
        value: "",
        error: "",
    },
    password: {
        value: "",
        error: "",
    },
    username: {
        value: "",
        error: "",
    },
};

const schemas = {
    email: z.email(),
    password: z.string(),
    username: z.string(),
};

async function onSubmit() {
    try {
        const response = await api.POST("/api/v1/auth/register", {
            body: {
                email: models.email.value,
                password: models.password.value,
                username: models.username.value,
                user_role: "customer",
            },
        });
        if (!response.error && response.data) {
            console.log(response.data);
        }
    } catch (error) {
        console.error(error);
    }
}
</script>
<style lang="scss">
@use "../assets/scss/auth";
</style>
