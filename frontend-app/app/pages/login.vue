<template>
    <div class="page">
        <h2>Вход</h2>
        <form
            class="auth-form"
            @submit.prevent="onSubmit">
            <UiInput
                v-model="models.username"
                :schema="schemas.username"
                placeholder="Логин" />
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

const api = useApi();

const models = {
    username: {
        value: "",
        error: "",
    },
    password: {
        value: "",
        error: "",
    },
};

const schemas = {
    username: z.string(),
    password: z.string(),
};

async function onSubmit() {
    try {
        const fd = new FormData();
        fd.append("username", models.username.value);
        fd.append("password", models.password.value);

        const response = await api.POST("/api/v1/auth/login", {
            // TODO заменить formdata на json
            // @ts-ignore
            body: fd,
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
