<template>

    <v-container class="fill-height" min-width="90vw">
        <div class="d-flex flex-column fill-height w-100 align-center justify-center" style="margin-top: -100px">
            <div class="text-overline pb-4">Welcome to...</div>
            <div class="w-100 d-flex justify-center mb-12">
                <v-img :src="'./logo.png'" class="d-block" max-width="1100px" />
            </div>

            <div class="w-100 d-flex align-center justify-space-evenly mt-6" style="max-width: 1100px">
                <v-avatar size="180" :color="user.color" v-for="user in users" :key="user.id" class="user-avatar"
                    @mouseover="hoveredUserId = user.id" @mouseleave="hoveredUserId = null" @click="selectUser(user)">
                    <v-avatar size="170">
                        <v-img :src="user.imgUrl" style="position: absolute;" fill />
                        <div class="text-h5 user-name" style="" v-if="user.id == hoveredUserId">{{
                            user.name }}
                        </div>
                    </v-avatar>
                </v-avatar>
                <v-avatar size="180" color="error" class="user-avatar" @mouseover="hoveredUserId = users.length + 1"
                    @mouseleave="hoveredUserId = null">
                    <v-avatar size="170">
                        <v-icon size="160" style="position: absolute;">mdi-account</v-icon>
                        <div class="text-h5 user-name" v-if="hoveredUserId == users.length + 1">Guest
                        </div>
                    </v-avatar>
                </v-avatar>
            </div>
        </div>
    </v-container>

</template>

<script>
import { useUserStore } from '@/stores/user'
import { useTableauStore } from '@/stores/tableau'
import { tableauSignInBody, patName, patSecret } from '@/stores/consts'
import axios from 'axios'

export default {
    setup() {
        const userStore = useUserStore()
        const tableauStore = useTableauStore()

        return { userStore, tableauStore }
    },

    name: 'SelectUser',
    data: () => ({
        users: [
            { id: 1, name: 'Will', color: 'warning', imgUrl: './will.png', userLuid: 'f2ba9553-a4d0-44c9-8dcb-a832b89b66f3' },
            { id: 2, name: 'Kyle', color: 'primary', imgUrl: './kyle.jpeg', userLuid: '41aeb79b-7e83-40d6-b0b4-19aa274d95e3' },

        ],
        selectedUser: null,
        hoveredUserId: null
    }),
    methods: {
        selectUser(user) {
            this.userStore.selectedUser = user
            this.$router.push('/gallery')
        },
    },
    async mounted() {

    }
}

</script>

<style>
.user-avatar {
    cursor: pointer;
}

.user-avatar:hover {
    opacity: 0.7;
    transform: scale(1.2);
    transition: all 0.3s;
}

.user-avatar:not(:hover) {
    transform: scale(1);
    transition: all 0.3s;
}

.user-name {
    position: relative;
    top: 0;
    opacity: 1 !important;
    text-shadow: 2px 2px 2px #000;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 2px 18px 2px 18px;
    border-radius: 12px;
}
</style>