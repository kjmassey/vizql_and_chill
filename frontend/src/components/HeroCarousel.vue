<template>
    <v-carousel height="55vh" cycle cover style="margin-top: -64px;" show-arrows="hover"
        @mouseover="showHeroCarouselArrows = true" @mouseleave="showHeroCarouselArrows = false"
        hide-delimiter-background>

        <v-carousel-item v-for="item in contentStore.carouselItems" :key="item['Item ID']">
            <div class="d-flex h-100">
                <div class="fill-height w-100" style="position: relative;">
                    <v-img :src="`${item['Item Hyperlink'].replace('/#/site/', '/t/')}.png`" cover
                        lazy-src="../../public/chart-lazy-load.png"></v-img>
                </div>
                <div style=" position: absolute; top: 0; flex-wrap: nowrap;" class="d-flex w-100 mx-2 my-2">
                    <div class="d-flex flex-column"
                        style="background-color: rgb(0,0,0,.6); border-radius: 10px; max-width: 75%;">
                        <div class="text-h2 px-4 py-2"
                            style="flex-wrap: nowrap; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; ">
                            {{ item['Item Name'] }}
                        </div>
                        <div class="text-body-1 px-4 py-2">{{ item["Item Type"] }} by {{ itemInContentStore(item) &&
                            itemInContentStore(item)[itemInContentStore(item).type]['owner_name'] }}
                            <v-btn icon="mdi-open-in-app" color="transparent" density="compact" variant="flat"
                                @click="$emit('showEmbeddedView', itemInContentStore(item))"></v-btn>
                        </div>
                    </div>
                </div>
            </div>
        </v-carousel-item>


    </v-carousel>
</template>

<script>
import { useContentStore } from '@/stores/content';

export default {
    name: 'HeroCarousel',
    setup() {
        const contentStore = useContentStore();

        return { contentStore };
    },

    data: () => ({
        //
    }),
    props: {
        //
    },
    computed: {
        //
    },
    methods: {
        itemInContentStore(currentItem) {
            let item = this.contentStore.contentDetails.find((e) => (
                e.luid === currentItem['Item LUID']
            ));

            if (item) {

                let objType = item['type'];

                let itemObj = {
                    type: objType
                }

                let url = currentItem['Item Hyperlink'].replace('/#/site/', '/t/')

                itemObj[objType] = {
                    contentUrl: url,
                    id: item['luid'],
                    name: item['name'],
                    owner_name: item['owner_name'],
                }

                return itemObj;
            } else {
                return null;
            }
        }
    },
    mounted() {
        for (const item of this.contentStore.carouselItems) {
            this.contentStore.getContentDetails(item['Item LUID']);
        }
    }
}
</script>

<style scoped>
/* */
</style>