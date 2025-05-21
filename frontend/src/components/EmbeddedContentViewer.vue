<template>
    <v-dialog :model-value="true">
        <div class="card-container">

            <div class="card">
                <v-card class="w-100">
                    <v-card-title>

                        <div class="d-flex justify-space-between align-center pa-4">
                            <div class="d-flex">
                                <div class="d-flex flex-column text-h3">
                                    <div>
                                        {{ $props.propsObj[$props.propsObj.type].name }}
                                    </div>
                                    <div class="pl-2 text-body-1">
                                        by {{ itemInContentStore && itemInContentStore.owner_name }}
                                    </div>
                                </div>
                                <v-icon size="26" class="mx-2" style="cursor: pointer;"
                                    @click="openContentInTableau">mdi-open-in-new</v-icon>
                            </div>
                            <div style="align-self: flex-start;" class="close-dialog-icon"
                                @click="$emit('closeEmbeddedContentViewer')">
                                <v-icon>mdi-window-close</v-icon>
                            </div>

                        </div>
                        <div class="d-flex px-6 justify-start align-center">
                            <v-btn size="36" flat class="mr-4"
                                @click="userStore.rateContent(userStore.selectedUser.userLuid, $props.propsObj[$props.propsObj.type].id, 0)">
                                <v-tooltip text="Not For Me" activator="parent" location="bottom"></v-tooltip>
                                <v-icon size="34" :color="isLikedDisliked === 0 ? 'error' : null">
                                    {{ isLikedDisliked === 0 ? 'mdi-thumb-down' :
                                        'mdi-thumb-down-outline'
                                    }}

                                </v-icon>
                            </v-btn>
                            <v-btn size="36" flat
                                @click="userStore.rateContent(userStore.selectedUser.userLuid, $props.propsObj[$props.propsObj.type].id, 1)">
                                <v-tooltip text="I Like It!" activator="parent" location="bottom"></v-tooltip>
                                <v-icon size="34" :color="isLikedDisliked === 1 ? 'primary' : null">
                                    {{ isLikedDisliked === 1 ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'
                                    }}
                                </v-icon>
                            </v-btn>
                            <div class="d-flex align-center pl-4 text-body-1">
                                ({{ itemInContentStore && `${Math.round(itemInContentStore.rating * 100)}%` }})
                            </div>
                        </div>
                        <div class="my-2">
                            <div class="d-flex px-2 justify-start align-start w-100">
                                <template v-if="!isFavorited">
                                    <v-btn variant="plain" color="primary" class=" text-none" @click="addRemoveFavorite"
                                        :loading="localFaveLoading">
                                        <v-tooltip text="Click to Add" activator="parent" location="bottom"></v-tooltip>
                                        <v-icon class="pr-4">mdi-plus</v-icon>Add to
                                        Favorites</v-btn>
                                </template>
                                <template v-else>

                                    <v-btn variant="plain" color="success" class=" text-none" @click="addRemoveFavorite"
                                        :loading="localFaveLoading">
                                        <v-tooltip text="Click to Remove" activator="parent"
                                            location="bottom"></v-tooltip>
                                        <v-icon class="pr-4" @click="contents">mdi-check</v-icon>Added to
                                        Favorites</v-btn>
                                </template>
                            </div>

                        </div>
                        <div class="pa-4 d-flex justify-start align-center">
                            <div class="px-2 d-flex align-center">
                                <v-icon>mdi-file-document-outline</v-icon>
                                <div class="text-body-1 pl-2">
                                    {{ $props.propsObj.type.charAt(0).toUpperCase() + $props.propsObj.type.slice(1) }}
                                </div>
                                <div class="d-flex align-center pl-8">
                                    <div>
                                        <v-icon>mdi-tag-outline</v-icon>
                                    </div>
                                    <div class="pl-4 text-body-1">
                                        <v-progress-circular :size="20" :width="2" indeterminate
                                            v-if="localTagsLoading"></v-progress-circular>
                                        {{ itemInContentStore && itemInContentStore.tags }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </v-card-title>
                    <v-card-text class="h-100">
                        <div class="embedded-content">
                            <div class="flex-shrink-1 flex-grow-1 d-flex justify-center align-center">
                                <tableau-viz :src="$props.contentUrl" device="desktop" hide-tabs toolbar="hidden">
                                </tableau-viz>
                            </div>
                        </div>
                    </v-card-text>
                </v-card>
            </div>
        </div>
    </v-dialog>
</template>

<script>
import { useContentStore } from "@/stores/content";
import { useUserStore } from "@/stores/user";

export default {
    setup() {
        const contentStore = useContentStore();
        const userStore = useUserStore();

        return { contentStore, userStore };
    },
    data: () => ({
        localFaveLoading: false,
        localTagsLoading: false,
    }),
    props: {
        contentUrl: {
            type: String,
            default: ""
        },
        contentTitle: {
            type: String,
            default: "Content Title..."
        },
        propsObj: {
            type: Object,
            default: () => ({})
        }
    },
    computed: {
        itemInContentStore() {
            try {
                return this.contentStore.contentDetails.find(e => e.luid === this.$props.propsObj[this.$props.propsObj.type].id)
            }
            catch (e) {
                return {}
            }
        },
        isLikedDisliked() {
            let itemRatings = this.userStore.userContentRatings.filter(e => e.item === this.$props.propsObj[this.$props.propsObj.type].id)

            if (itemRatings.length > 0) {
                return itemRatings[0].rating
            } else {
                return -1
            }

        },
        isFavorited() {
            let itemFavorites = this.contentStore.formattedUserFavorites.filter(e => e.luid === this.$props.propsObj[this.$props.propsObj.type].id)

            if (itemFavorites.length > 0) {
                return true
            } else {
                return false
            }
        },
        computedItemName() {
            try {
                if (this.$props.propsObj.contentName) {
                    return this.$props.propsObj.contentName
                } else {
                    return this.$props.itemObj[this.$props.itemObj.type].name
                }
            } catch (e) {
                return ''
            }
        },

    },
    methods: {
        async initViz() {
            // This is required when the page loads and any time the embedded viz changes in order for it to be interactive!

            // Set the <tableau-viz> component to be our embedded viz for interactivity -- this all works because of the import added to index.html
            const viz = document.querySelector("tableau-viz");

            this.embeddedViz = viz;

            // Add an event listener to verify the viz becomes interactive
            await new Promise((resolve) => {
                this.embeddedViz.addEventListener("firstinteractive", () => {
                    resolve();
                });
            });
        },
        openContentInTableau() {
            // Open the content in Tableau
            window.open(this.$props.contentUrl, "_blank");
        },
        async addRemoveFavorite() {
            this.localFaveLoading = true

            let reqObj = {
                userLuid: this.userStore.selectedUser.userLuid,
                itemLuid: this.$props.propsObj[this.$props.propsObj.type].id,
                itemType: this.$props.propsObj.type,
                label: this.$props.propsObj[this.$props.propsObj.type].name
            }

            if (this.isFavorited) {
                await this.contentStore.removeFromUserFavorites(reqObj)
            } else {
                await this.contentStore.addToUserFavorites(reqObj)
            }

            this.localFaveLoading = false
        },
    },
    async mounted() {
        await this.initViz();
    }
}
</script>

<style scoped>
.card-container {
    min-height: 95vh;
    min-width: 90vw;
    position: relative
}

.card {
    display: flex;
    height: 100%;
    width: 100%;
    position: absolute
}

.close-dialog-icon {
    cursor: pointer;
    z-index: 99
}

.embedded-content {
    height: 80%;
    display: flex;
    flex-grow: 0;
    justify-content: center;
    align-items: top;
    overflow: auto;
}
</style>