export const tableauUrlRoot = "YOUR-TABLEAU-URL-HERE" // e.g. http://10az.online.tableau.com 
export const tableauApiVersion = "3.25"
export const tableauAuthEndpoint = `${tableauUrlRoot}/api/${tableauApiVersion}/auth/signin`
export const tableauSite = "YOUR-SITE-NAME"
export const patName = "YOUR-PAT-NAME"
export const patSecret = "YOUR-PAT-SECRET"

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