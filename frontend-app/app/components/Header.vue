<template>
    <header>
        <NuxtLink
            class="logo"
            to="/"
            >IWS</NuxtLink
        >
        <div
            v-if="authStore.currentUser"
            class="account">
            <div
                class="username"
                @click="authStore.logout">
                {{ authStore.currentUser.username }}
            </div>
        </div>
    </header>
</template>
<script lang="ts" setup>
const authStore = useAuthStore();
</script>
<style lang="scss" scoped>
header {
    height: 3rem;
    display: flex;
    align-items: center;
    height: 50px;

    .logo {
        color: var(--color-primary);
        font-weight: bold;
        font-size: 2rem;
        text-decoration: none;
    }

    .account {
        margin-left: auto;
    }
}
</style>
