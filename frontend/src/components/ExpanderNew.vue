<template>



    <v-card elevation="0" class="d-flex w-100 flex-column">
        <v-overlay contained v-model="selfIsLoading" :z-index="1000" class="d-flex align-center justify-center">
            <v-progress-circular indeterminate color="error" size="48"></v-progress-circular>
        </v-overlay>
        <v-card-title v-if="!$props.isSearchResults" class="text-h5 mx-2 my-2">
            {{ `${$props.title} (${$props.itemsList.length})` }}
        </v-card-title>
        <v-card-title v-else class="text-h5 mx-2 my-2">
            {{ `${$props.title} (${totalItemCount})` }}
        </v-card-title>
        <v-card-text class="w-100">
            <v-row>
                <div class="d-flex  align-center flex-grow-0  w-100" :class="showAll ? 'flex-wrap' : 'flex-nowrap'">
                    <template v-if="!showAll" v-for="result in $props.itemsList">
                        <v-col xxl="2" xl="3" lg="4" md="6" sm="12">
                            <ContentPreviewNew :img-height="350" :item-obj="result"
                                @openContentPreviewModal="(e) => { $emit('openContentPreviewModal', e) }" />
                        </v-col>
                    </template>
                    <template v-else v-for="result in $props.itemsList">
                        <v-col xxl="2" xl="3" lg="4" md="6" sm="12">
                            <ContentPreviewNew :img-height="350" :item-obj="result"
                                @openContentPreviewModal="(e) => { $emit('openContentPreviewModal', e) }" />
                        </v-col>
                    </template>
                </div>
            </v-row>
        </v-card-text>
        <v-card-actions class="my-0 py-0">
            <div class="d-flex justify-center align-center flex-grow-1 flex-nowrap w-100"
                v-if="!$props.isSearchResults">
                <v-tooltip :text="showUpChevron ? 'Collapse' : 'Load More'" location="top" color="black">
                    <template #activator="{ props }">
                        <v-btn flat variant="tonal" v-bind="props" density="compact" @click="showAll = !showAll"><v-icon
                                size="28" class="mx-8">{{ showUpChevron ?
                                    'mdi-chevron-up' :
                                    'mdi-chevron-down' }}</v-icon></v-btn>
                    </template>
                </v-tooltip>
            </div>
            <div class="d-flex justify-center align-center flex-grow-1 flex-nowrap w-100" v-else>
                <v-tooltip text="Load More" location="top" color="black">
                    <template #activator="{ props }">

                        <v-btn flat variant="tonal" v-bind="props" density="compact" @click="loadMore()" class="mx-2"
                            :disabled="!enableExpandButton"><v-icon size="28"
                                class="mx-8">mdi-chevron-down</v-icon></v-btn>
                    </template>
                </v-tooltip>
                <v-tooltip text="Collapse" location="top" color="black" v-if="showAll">
                    <template #activator="{ props }">

                        <v-btn flat variant="tonal" v-bind="props" density="compact" @click="showAll = false"
                            class="mx-2"><v-icon size="28" class="mx-8">mdi-chevron-up</v-icon></v-btn>
                    </template>
                </v-tooltip>
            </div>
        </v-card-actions>
    </v-card>

</template>

<script>
import { useContentStore } from '@/stores/content';
import { useUserStore } from '@/stores/user';
import ContentPreviewNew from './ContentPreviewNew.vue';
import { tableauUrlRoot, tableauSite } from '@/stores/consts';

export default {
    name: 'ExpanderNew',
    setup() {
        const contentStore = useContentStore();
        const userStore = useUserStore();

        return { contentStore, userStore };
    },
    data: () => ({
        showAll: false,
        urlRoot: tableauUrlRoot,
        site: tableauSite,
        showOverlay: true,
        selfIsLoading: false
    }),
    props: {
        title: {
            type: String,
            default: 'Expander Title'
        },
        itemsList: {
            type: Array,
            default: [1]
        },
        itemType: {
            type: String,
            default: 'View'
        },
        isSearchResults: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        totalItemCount() {
            return this.contentStore.searchResultsCountsByType[this.$props.itemType].count;
        },
        enableExpandButton() {
            if (this.contentStore.searchResultsCountsByType[this.$props.itemType].count <= 5) {
                return true;
            }

            if (!this.showAll) { return true }

            return !this.contentStore.searchResultsCountsByType[this.$props.itemType].itemsLoaded === this.totalItemCount
        },
        computedItemList() {
            return this.showAll ? this.$props.itemsList.slice(0, 4) : this.$props.itemsList;
        },
        showUpChevron() {
            return this.showAll ? true : false
        },
        components: {
            ContentPreviewNew
        },
    },
    methods: {
        async loadMore() {
            if (this.contentStore.searchResultsCountsByType[this.$props.itemType].itemsLoaded !== this.totalItemCount) {

                this.selfIsLoading = true;

                let searchObj = {
                    searchTerm: this.contentStore.searchTerm,
                    searchLimit: 20,
                    objectType: this.$props.itemType,
                }

                let pagesLoad = this.contentStore.searchResultsCountsByType[this.$props.itemType].pagesLoaded

                pagesLoad === 0 ? searchObj.pageIndex = 0 : searchObj.pageIndex = pagesLoad;

                await this.contentStore.loadMoreSearchResults(searchObj)

                this.selfIsLoading = false;
            }
            this.showAll = true;

        },
        buildImgUrl(itemContent) {
            let urlBase = `${this.urlRoot}/t/${this.site}/views`;

            switch (itemContent.type) {
                case 'workbook':
                    return `${urlBase}/${itemContent.defaultViewUrl}.png`;

                case 'view':
                    return `${urlBase}/${itemContent.path}.png`;

                case 'datasource':
                    return './datasource.png';

                case 'table':
                    return './database_table.png'

                default:
                    return `${this.urlRoot}/t/${this.site}/views/${itemContent.defaultViewUrl}.png`;
            }
        },
        getDescription(content) {
            switch (content.type) {
                case 'workbook':
                    return content.shareDescription;
                case 'view':
                    return `Parent Workbook: ${content.containerNameadmin}`;
                case 'datasource':
                    return content.description;
                case 'project':
                    return content.description;
                default:
                    return content.description;
            }
        }
    },
    async mounted() {
        //
    }

};

</script>

<style scoped>
.hide-expand-content {

    display: none;
}

.expand-content {
    overflow: hidden;
    max-height: 0px;
    /* transition: max-height 2s ease-in; */
}

.expand-content.expand {
    /* transition: max-height 2s ease-out; */
    max-height: 10000px;
}

.dimmed-button {
    opacity: .7;
}
</style>