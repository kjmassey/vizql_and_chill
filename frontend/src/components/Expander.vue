<template>


    <v-card elevation="0" class="d-flex w-100 flex-column">
        <v-overlay contained v-model="selfIsLoading" :z-index="1000" class="d-flex align-center justify-center">
            <v-progress-circular indeterminate color="error" size="48"></v-progress-circular>
        </v-overlay>
        <v-card-title class="my-2">
            {{ `${$props.title} (${contentStore.searchResultsCountsByType[$props.itemType].count})` }}
        </v-card-title>
        <v-card-text class="w-100">
            <v-row>
                <div class="d-flex justify-center align-center flex-grow-1 flex-wrap w-100">
                    <template v-for="result in $props.itemsList">
                        <ContentPreviewNew :img-height="350" :content-type="result.content.type"
                            :content-name="result.content.title" :owner-name="result.content.ownerName"
                            :modified-date="result.content.modifiedTime"
                            :content-description="getDescription(result.content)" :img-url="buildImgUrl(result.content)"
                            :luid="result.content.luid" class="mx-4 my-4"
                            @openContentPreviewModal="(e) => { $emit('openContentPreviewModal', e) }" />
                    </template>
                </div>
            </v-row>
        </v-card-text>
        <!-- </v-fab-transition> -->
        <v-card-actions class="my-0 py-0">
            <div class="d-flex justify-center align-center flex-grow-1 flex-wrap w-100">
                <v-tooltip :text="showUpChevron ? 'Collapse' : 'Load More'" location="top" color="black">
                    <template #activator="{ props }">
                        <v-btn flat variant="tonal" v-bind="props" density="compact" @click="loadMore"><v-icon size="28"
                                class="mx-8">{{ showUpChevron ?
                                    'mdi-chevron-up' :
                                    'mdi-chevron-down' }}</v-icon></v-btn>
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
    name: 'Expander',
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
    },
    computed: {
        computedItemList() {
            return this.showAll ? this.$props.itemsList.slice(0, 4) : this.$props.itemsList;
        },
        showUpChevron() {
            let currentCount = this.contentStore.searchResultsCountsByType[this.$props.itemType].itemsLoaded
            let totalCount = this.contentStore.searchResultsCountsByType[this.$props.itemType].count

            if (currentCount >= totalCount) {
                return true;
            }
            return false;
        }
    },
    components: {
        ContentPreviewNew
    },
    methods: {
        async loadMore() {
            this.selfIsLoading = true;

            let searchObj = {
                searchTerm: this.contentStore.searchTerm,
                searchLimit: 20,
                objectType: this.$props.itemType,
            }

            let pagesLoad = this.contentStore.searchResultsCountsByType[this.$props.itemType].pagesLoaded

            pagesLoad === 0 ? searchObj.pageIndex = 0 : searchObj.pageIndex = pagesLoad;

            await this.contentStore.loadMoreSearchResults(searchObj)

            this.showAll = true;
            this.selfIsLoading = false;

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
    transition: max-height 2s ease-in;
}

.expand-content.expand {
    transition: max-height 2s ease-out;
    max-height: 10000px;
}
</style>