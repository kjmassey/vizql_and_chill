import { defineStore } from "pinia";

export const useTableauStore = defineStore("tableau", {
    state: () => ({ apiToken: "", siteLuid: "", userLuid: "", error: "", siteContentUrl: "" }),
    getters: {
        //
    },
    actions: {
        updateAuthDetails(response) {
            console.log("RESP IN STATE: ", response.data)

            this.apiToken = response.data.credentials.token
            this.siteLuid = response.data.credentials.site.id
            this.siteContentUrl = response.data.credentials.site.contentUrl
            this.userLuid = response.data.credentials.user.id
        },
        updateError(error) {
            this.error = error
        },
    },
});