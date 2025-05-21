import { defineStore } from 'pinia'
import axios from 'axios'
import { API_ROOT, SITE_CONTENT_DS_LUID } from '@/consts'
import { luidIsInList } from './helpers'
import { toRaw } from 'vue'
import { useUserStore } from './user'

const userStore = useUserStore()

export const useContentStore = defineStore('content', {

    state: () => ({
        isLoading: false,
        tagsLoading: false,
        favesLoading: false,
        error: null,
        allSiteContent: [],
        workbookPreviewImages: [],
        searchResults: [],
        searchResultsCountsByType: {},
        filteredSearchResults: [],
        searchTerm: '',
        carouselItems: [],
        itemTags: [],
        userFavorites: [],
        contentDetails: [],
        contentByTagResults: [],
        featuredContent1: [],
        showFeaturedContent1: false,
        featuredContent2: [],
        showFeaturedContent2: false,
        featuredContent3: [],
        showFeaturedContent3: false,
        featuredContent4: [],
        showFeaturedContent4: false,
        featuredContent5: [],
        showFeaturedContent5: false,
        agedContent: [],
        showAgedContent: false,
        newContent: [],
        showNewContent: false,
        featuredAuthorContent: [],
        showFeaturedAuthorContent: false,
        itemUrl: ''
    }),
    getters: {
        formattedSearchResultsByType: (state) => (type) => {
            let results = state.searchResults.filter(content => content.content.type === type)
            let formattedResults = []


            for (const res of results) {
                let newObj = {}

                newObj.type = type
                newObj[type] = {}
                newObj[type].id = res.content.luid
                newObj[type].contentUrl = res.content.repositoryUrl
                newObj[type].name = res.content.title
                newObj.name = res.content.title
                newObj[type].updatedAt = res.content.modifiedTime

                formattedResults.push(newObj)

            }

            return formattedResults
        },
        getUserExcludedContent: (state) => (userLuid) => {
            console.log()

            let userExcludedContent = state.contentDetails.filter(e => e.hide_from_users && e.hide_from_users.includes(userLuid))

            return userExcludedContent
        },
        getUserExcludedContentLuids: (state) => (userLuid) => {
            return [...new Set(state.getUserExcludedContent(userLuid).map(e => e.luid))]
        },
        uniqueContentTypes: (state) => {
            // let contentTypes = state.allSiteContent.map(content => content["Item Type"])
            // return [...new Set(contentTypes)]
            return ['View', 'Workbook', 'Datasource', 'Project']
        },
        filteredContent: (state) => (filterKey, filterVal) => {
            try {
                return state.allSiteContent.filter(content => content[filterKey] === filterVal)
            } catch (error) {
                console.error("Error filtering content:", error)
                return []
            }
        },
        // filteredSearchResults: (state) => (filterObj) => {
        //     filterObj.types = filterObj.types.map(e => e.toLowerCase())

        //     let results = state.searchResults

        //     if (filterObj.types.length > 0) {
        //         results = results.filter(content => filterObj.types.includes(content.content.type))
        //     }



        //     if (filterObj.likedByMe) {
        //         let userLuid = toRaw(userStore.selectedUser).userLuid

        //         let ratings = toRaw(userStore.userContentRatings)
        //         let positiveUserRatings = ratings.filter(e => e.user === userLuid && e.is_active && e.rating === 1)

        //         let likedLuids = positiveUserRatings.map(e => e.item)
        //         results = results.filter(content => likedLuids.includes(content.content.luid))
        //     }

        //     console.log("++++ RESULTS, ", results)
        //     return results
        // },
        getItemContentUrl: (state) => (itemType, luid) => {
            console.log("++++ LUID, ", luid)
            console.log("++++ ITEM TYPE, ", itemType)

            let content = state.allSiteContent.filter(e => (
                e["Item Type"].toLowerCase() === itemType.toLowerCase() && e["Item LUID"] === luid
            ))

            console.log("++++ CONTENT, ", content)

            try {
                return content[0]["Item Hyperlink"]
            } catch (error) {
                // console.error("Error getting item content URL:", error)
                return ''
            }
        },

        getItemTags: (state) => (luid) => {
            let items = state.itemTags.filter(e => e.itemLuid === luid)

            if (items.length > 0) {
                return { tags: items[0].tags }
            }
            else {
                return { tags: [] }
            }
        },
        formattedUserFavorites: (state) => {
            try {
                if (state.userFavorites.favorites.favorite.length > 0) {
                    return state.userFavorites.favorites.favorite.map(e => {
                        return { type: e.type, luid: e[e.type].id }
                    })
                }
                else {
                    return []
                }
            } catch {
                return []
            }
        },
        formattedUserRatings: (state) => (userRating) => {

            let ratings = userStore.userContentRatings.filter(e => e.is_active)
            let formattedRatings = []

            for (const rating of ratings) {
                let newObj = {}
                let objInDetails = state.contentDetails.find(e => e.luid === rating.item)

                if (objInDetails) {
                    newObj.type = objInDetails.type
                    newObj.rating = rating.rating
                    newObj[objInDetails.type] = {}
                    newObj[objInDetails.type].id = objInDetails.luid
                    newObj[objInDetails.type].name = objInDetails.name
                    newObj[objInDetails.type].contentUrl = ''

                    formattedRatings.push(newObj)
                }
            }

            return formattedRatings
        }
    },
    actions: {
        resetError() {
            this.error = null
        },
        resetSiteContent() {
            this.allSiteContent = []
        },
        resetSearchResults() {
            this.searchResults = []
        },
        resetSearchResultsCountsByType() {
            this.searchResultsCountsByType = {}
        },
        resetUserFavorites() {
            this.userFavorites = []
        },
        async getWorkbookPreviewImage(workbookLuid) {
            this.loading = true

            let reqBody = {
                "wb_luid": workbookLuid
            }

            await axios.post(`${API_ROOT}/tableau/getWorkbookPreviewImage/`, reqBody)
                .then(response => {
                    this.loading = false
                    this.workbookPreviewImages.push({ wbLuid: workbookLuid, image: response.data })
                })
                .catch(error => {
                    console.log("++++++ ", error)
                    this.error = error
                    this.loading = false
                })
        },
        getCarouselItems(arrLength) {
            let contentNoWorkbooks = this.allSiteContent.filter(e => e["Item Type"] === 'View')

            // Math.floor(Math.random() * (max - min + 1) + min)
            let randArr = Array.from({ length: arrLength }, () => Math.floor(Math.random() * (0, contentNoWorkbooks.length - 1 + 1) + 0))

            console.log("++++ RAND ARR, ", randArr)


            this.carouselItems = randArr.map(e => contentNoWorkbooks[e])
        },
        async vdsGetAllSiteContent(initialLoad = false) {
            let reqBody = {
                "ds_luid": SITE_CONTENT_DS_LUID,
                "initial": initialLoad,
            }

            console.log("++++ REQ BODY, ", reqBody)

            this.isLoading = true

            if (initialLoad) {
                console.log("+++++ INITIAL LOAD")

                this.resetSiteContent()
                await axios.post(`${API_ROOT}/tableau/getSiteContent/`, reqBody)
                    .then(response => {
                        console.log("++++ RESPONSE DATA, ", response.data)

                        this.allSiteContent = response.data.data
                        this.getCarouselItems(10)
                        this.isLoading = false
                    })
                    .catch(error => {
                        console.log(error)
                        this.isLoading = false
                    })
            } else {
                console.log("+++++ NOT INITIAL LOAD")
                await userStore.fetchUserJwt()
                axios.post(`${API_ROOT}/tableau/getSiteContent/`, reqBody)
                    .then(response => {
                        console.log("++++ RESPONSE DATA, ", response.data)

                        response.data.data.map(e => { this.allSiteContent.push(e) })
                        this.isLoading = false
                    })
                    .catch(error => {
                        console.log(error)
                        this.isLoading = false
                    })
            }
        },

        setSearchLoading(val) {
            this.isLoading = val
        },

        async searchForContent(searchObj) {
            let reqBody = {
                term: searchObj.searchTerm,
                limit: searchObj.searchLimit,
                objectType: searchObj.objectType,
                getAll: false,
                pageIndex: 0
            }

            // this.isLoading = true
            // this.resetSearchResults()
            await axios.post(`${API_ROOT}/tableau/contentSearch/`, reqBody)
                .then(response => {
                    console.log(response.data.length, " SEARCH RESULTS")

                    this.searchResults.push(...response.data.results)
                    this.searchResultsCountsByType[reqBody.objectType] = {}
                    this.searchResultsCountsByType[reqBody.objectType].count = response.data.pagination.totalAvailable
                    this.searchResultsCountsByType[reqBody.objectType].pagesLoaded = 0
                    this.searchResultsCountsByType[reqBody.objectType].itemsLoaded = 0
                })
                .catch(error => {
                    this.error = error
                    // this.isLoading = false
                })
        },
        async loadMoreSearchResults(searchObj) {
            let reqBody = {
                term: searchObj.searchTerm,
                limit: searchObj.searchLimit,
                objectType: searchObj.objectType,
                getAll: false,
                pageIndex: searchObj.pageIndex
            }

            this.isLoading = true
            await axios.post(`${API_ROOT}/tableau/contentSearch/`, reqBody)
                .then(response => {
                    console.log(response.data.length, " LOAD MORE SEARCH RESULTS")

                    if (searchObj.pageIndex === 0) {
                        this.searchResults.push(...response.data.results.slice(4))
                    } else {

                        this.searchResults.push(...response.data.results)
                    }

                    this.searchResultsCountsByType[reqBody.objectType].pagesLoaded += 1
                    this.searchResultsCountsByType[reqBody.objectType].itemsLoaded += response.data.results.length
                    this.isLoading = false
                })
                .catch(error => {
                    this.error = error
                    this.isLoading = false
                })
        },
        async getContentTags(contentLuid, contentType) {
            let reqBody = {
                "item_luid": contentLuid,
                "item_type": contentType
            }

            if (!luidIsInList(contentLuid, toRaw(this.itemTags))) {


                this.tagsLoading = true
                await axios.post(`${API_ROOT}/tableau/getItemTags/`, reqBody)
                    .then(response => {
                        const tagArr = response.data.view.tags.tag.map(e => e.label)
                        this.itemTags.push({ itemLuid: contentLuid, tags: tagArr })
                        this.tagsLoading = false
                    })
                    .catch(error => {
                        this.error = error
                        this.tagsLoading = false
                    })


            }
        },
        async getUserFavorites(userLuid) {
            this.favesLoading = true
            await axios.post(`${API_ROOT}/tableau/getUserFavorites/`, { "user_luid": userLuid })
                .then(response => {
                    this.userFavorites = response.data
                    this.favesLoading = false
                })
                .catch(error => {
                    this.error = error
                    this.favesLoading = false
                })
        },
        async addToUserFavorites(reqObj) {
            let reqBody = {
                "user_luid": reqObj.userLuid,
                "item_luid": reqObj.itemLuid,
                "item_type": reqObj.itemType,
                "label": reqObj.label
            }

            this.favesLoading = true
            await axios.post(`${API_ROOT}/tableau/addToUserFavorites/`, reqBody)
                .then(response => {
                    this.getUserFavorites(reqObj.userLuid)
                    this.favesLoading = false
                })
                .catch(error => {
                    this.error = error
                    this.favesLoading = false
                })
        },
        async removeFromUserFavorites(reqObj) {
            let reqBody = {
                "user_luid": reqObj.userLuid,
                "item_luid": reqObj.itemLuid,
                "item_type": reqObj.itemType,
                "label": reqObj.label
            }

            this.favesLoading = true
            await axios.post(`${API_ROOT}/tableau/removeFromUserFavorites/`, reqBody)
                .then(response => {
                    this.getUserFavorites(reqObj.userLuid)
                    this.favesLoading = false
                })
                .catch(error => {
                    this.error = error
                    this.favesLoading = false
                })
        },
        getFilteredSearchResults(filterObj) {
            filterObj.types = filterObj.types.map(e => e.toLowerCase())

            let results = this.searchResults

            if (filterObj.types.length > 0) {
                results = results.filter(content => filterObj.types.includes(content.content.type))
            }

            if (filterObj.likedByMe) {
                let userLuid = toRaw(userStore.selectedUser).userLuid

                let ratings = toRaw(userStore.userContentRatings)
                let positiveUserRatings = ratings.filter(e => e.user === userLuid && e.is_active && e.rating === 1)

                let likedLuids = positiveUserRatings.map(e => e.item)
                results = results.filter(content => likedLuids.includes(content.content.luid))
            }

            this.filteredSearchResults = results
        },
        getContentDetails(itemLuid) {
            //  console.log("+++++ ITEM LUID: ", itemLuid)
            let isInList = this.contentDetails.find(e => e.luid === itemLuid)

            if (!isInList) {
                //console.log("+++++ GET CONTENT DETAILS CALLED")

                let reqBody = {
                    luid: itemLuid
                }

                axios.post(`${API_ROOT}/tableau/retrieveContentDetails/`, reqBody).then(response => {

                    if (response.data) {
                        this.contentDetails.push(response.data)
                    }

                }).catch(error => {
                    console.log("+++++ ERROR GETTING CONTENT DETAILS, ", error)
                })
            }
            else {
                //
            }


        },
        async getContentByTag(tag) {
            let reqBody = {
                tag: tag
            }

            await axios.post(`${API_ROOT}/tableau/getItemsByTag/`, reqBody).then(response => {
                console.log("+++++ CONTENT BY TAG, ", response.data)
                this.contentByTagResults = response.data
            }).catch(error => {
                console.log("+++++ ERROR GETTING CONTENT BY TAG, ", error)
            })
        },
        updateFeatured1() {
            this.contentByTagResults.map(e => {
                this.getContentDetails(e[e.type].id)
                this.featuredContent1.push(e)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null

                this.showFeaturedContent1 = true
                this.isLoading = false
            })
        },
        updateFeatured2() {
            this.contentByTagResults.map(e => {
                this.getContentDetails(e[e.type].id)
                this.featuredContent2.push(e)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null

                this.showFeaturedContent2 = true
                this.isLoading = false
            })
        },
        updateFeatured3() {
            this.contentByTagResults.map(e => {
                this.getContentDetails(e[e.type].id)
                this.featuredContent3.push(e)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null

                this.showFeaturedContent3 = true
                this.isLoading = false
            })
        },
        updateFeatured4() {
            this.contentByTagResults.map(e => {
                this.getContentDetails(e[e.type].id)
                this.featuredContent4.push(e)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null

                this.showFeaturedContent4 = true
                this.isLoading = false
            })
        },
        updateFeatured5() {
            this.contentByTagResults.map(e => {
                this.getContentDetails(e[e.type].id)
                this.featuredContent5.push(e)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null

                this.showFeaturedContent5 = true
                this.isLoading = false
            })
        },
        async updateFeaturedContentByTag(featureObj) {
            this.isLoading = true

            console.log("+++++ FEATURED TAG, ", featureObj.tag)
            await this.getContentByTag(featureObj.tag)

            switch (featureObj.slot) {

                case 1:
                    this.updateFeatured1(this.contentByTagResults)
                    this.showFeaturedContent1 = true

                    break
                case 2:
                    this.updateFeatured2(this.contentByTagResults)
                    this.showFeaturedContent2 = true

                    break
                case 3:
                    this.updateFeatured3(this.contentByTagResults)
                    this.showFeaturedContent3 = true

                    break
                default:
                    console.log("+++++ ERROR: INVALID SLOT NUMBER")
            }

            this.isLoading = false

        },
        async vdsGetItemAndOpenInNewWindow(itemLuid) {
            let reqBody = {
                "ds_luid": SITE_CONTENT_DS_LUID,
                "item_luid": itemLuid
            }

            this.isLoading = true

            await axios.post(`${API_ROOT}/tableau/vdsQuerySingleItem/`, reqBody)
                .then(response => {
                    console.log("+++++ SINGLE ITEM VDS, ", response.data)
                    window.open(response.data.data[0].url, '_blank')
                    // this.itemUrl = response.data.url
                    this.isLoading = false
                })
                .catch(error => {
                    console.log("+++++ ERROR GETTING SINGLE ITEM VDS, ", error)
                    this.itemUrl = ''
                    this.isLoading = false
                })
        },
        async getOldContent() {
            this.isLoading = true

            await axios.get(`${API_ROOT}/tableau/getAgedContent/`).then(response => {
                this.agedContent = response.data
                this.showAgedContent = true
                this.isLoading = false
            })
        },
        updateOldContent() {
            this.agedContent.map(e => {
                this.getContentDetails(e[e.type].id)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null
            })
        },
        async getNewContent() {
            this.isLoading = true

            await axios.get(`${API_ROOT}/tableau/getNewContent/`).then(response => {
                this.newContent = response.data
                this.showNewContent = true
                this.isLoading = false
            })
        },
        async updateNewContent() {
            this.newContent.map(e => {
                this.getContentDetails(e.luid)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null
            })
        },
        async getFeaturedAuthorContent() {
            this.isLoading = true

            await axios.get(`${API_ROOT}/tableau/getFeaturedAuthorContent/`).then(response => {
                this.featuredAuthorContent = response.data
                this.showFeaturedAuthorContent = true
                this.isLoading = false
            })
        },
        updateFeaturedAuthorContent() {
            this.featuredAuthorContent.map(e => {
                this.getContentDetails(e[e.type].id)
                // e.type === 'workbook' ? this.getWorkbookPreviewImage(e.luid) : null
            })
        }
    },

})