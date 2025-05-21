import { defineStore } from 'pinia'
import axios from 'axios'
import { API_ROOT } from '@/consts'

export const useUserStore = defineStore('user', {
    state: () => ({ error: null, selectedUser: {}, userJwt: null, userContentRatings: [] }),
    getters: {},
    actions: {
        resetSelectedUser: () => {
            this.selectedUser = {}
        },
        resetUserJwt: () => {
            this.userJwt = null
        },
        async fetchUserJwt() {
            console.log("+++++ FETCHING JWT")
            console.log(`${API_ROOT}/tableau/getUserJwt`)

            await axios.get(`${API_ROOT}/tableau/getUserJwt/`)
                .then(response => {
                    console.log("++++++ JWT RESPONSE, ", response.data)
                    this.userJwt = response.data.token
                })
                .catch(error => {
                    console.log("++++++ JWT ERROR, ", error)
                    this.error = error
                })
        },
        async fetchUserContentRatings() {
            await axios.post(`${API_ROOT}/tableau/getRatingsForUser/`, { "user": this.selectedUser.userLuid })
                .then(response => {
                    this.userContentRatings = response.data

                })
                .catch(error => {
                    this.error = error
                })
        },
        async rateContent(userLuid, contentLuid, rating, type) {
            await axios.post(`${API_ROOT}/tableau/addUserRating/`, { "user": userLuid, "item": contentLuid, "rating": rating, "item_type": type })
                .then(response => {
                    console.log("+++++ REFRESHING USER RATINGS")
                    this.fetchUserContentRatings()
                })
                .catch(error => {
                    this.error = error
                })
        }
    },
})