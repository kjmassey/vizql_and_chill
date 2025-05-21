export const tableauUrlRoot = "https://10az.online.tableau.com"
export const tableauApiVersion = "3.25"
export const tableauAuthEndpoint = `${tableauUrlRoot}/api/${tableauApiVersion}/auth/signin`
export const tableauSite = "kgloverdev"
export const patName = "kyle-tc25"
export const patSecret = "MSEfArr3QyGEBdhw5bBuQA==:0hdHsEKQv7DS8VMbgmwEV3YrT5T0CMTB"

export const tableauSignInBody = (patName, patSecret) => {
    return {
        "credentials": {
            "personalAccessTokenName": patName,
            "personalAccessTokenSecret": patSecret,
            "site": {
                "contentUrl": tableauSite
            }
        }
    }
}