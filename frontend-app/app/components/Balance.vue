<template>
    <div class="balance box">
        <h3>Баланс</h3>
        {{ voucherBalance }}
    </div>
</template>
<script lang="ts" setup>
const api = useApi();

const voucherBalance = ref();

try {
    const data = await api.GET("/api/v1/vouchers/balance");
    if (data.response && data.data) {
        voucherBalance.value = data.data;
    } else {
        console.error("Failed to fetch balance data", data.error);
    }
} catch (error) {}
</script>
<style lang="scss" scoped>
@use "@/assets/scss/profile.scss";
</style>
