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
    const result = await auth.register({
        username: models.username.value,
        email: models.email.value,
        password: models.password.value,
    });
    if (result.ok) {
        alert("Аккаунт успешно создан. Теперь вы можете войти");
        useRouter().push("/login");
    } else {
        console.error(result.error);
    }
}
</script>
<style lang="scss">
@use "../assets/scss/auth";
</style>
