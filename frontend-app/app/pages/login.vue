<template>
    <div class="page">
        <h2>Вход</h2>
        <form
            class="auth-form"
            @submit.prevent="onSubmit">
            <UiInput
                v-model="models.email"
                :schema="schemas.email"
                placeholder="Email"
                type="email" />
            <UiInput
                v-model="models.password"
                :schema="schemas.password"
                placeholder="Пароль"
                type="password" />
            <UiButton type="submit">Войти</UiButton>
        </form>
    </div>
</template>
<script lang="ts" setup>
import z from "zod";

definePageMeta({
    layout: "auth",
});

const auth = useAuthStore();

const models = {
    email: {
        value: "",
        error: "",
    },
    password: {
        value: "",
        error: "",
    },
};

const schemas = {
    email: z.string().email(),
    password: z.string(),
};

async function onSubmit() {
    const result = await auth.login({
        email: models.email.value,
        password: models.password.value,
    });

    if (result.ok) {
        navigateTo("/my");
    } else {
        console.error(result.error);
    }
}
</script>
<style lang="scss">
@use "../assets/scss/auth";
</style>
