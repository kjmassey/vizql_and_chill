export function luidIsInList(luid, list) {
    console.log(luid)
    console.log(list)

    return list.some(e => e.itemLuid === luid)
}