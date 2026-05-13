<template>
    <div class="page my-page">
        <Profile class="profile" />
        <Balance class="balance" />
        <OperationsHistory class="operations-history" />
    </div>
</template>
<script lang="ts" setup></script>
<style lang="scss" scoped>
.my-page {
    display: grid;
    grid-template-areas:
        "profile operations-history"
        "balance operations-history";
    gap: 24px;

    .profile {
        grid-area: profile;
    }

    .balance {
        grid-area: balance;
    }

    .operations-history {
        grid-area: operations-history;
    }
}
</style>
