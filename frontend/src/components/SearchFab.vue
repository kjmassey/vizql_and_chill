<template>
    <div style="border: 1px solid red; margin-right: 100px">
        <v-fab :color="userStore.selectedUser.color" icon="mdi-menu" app position="static" location="top right"
            class="pl-4" @click="showMenuDial = true" style="z-index: 1000">


            <v-icon>mdi-magnify</v-icon>

        </v-fab>
    </div>

</template>

<script>
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()

        return { userStore }
    },

    name: "SearchFab",
    data: () => ({
        //
    })
}
</script>

<style scoped>
.speed-dial-item {
    background-color: rgb(22, 22, 29, .85);
    padding: 12px 24px;
    border-radius: 10px;
}
</style>