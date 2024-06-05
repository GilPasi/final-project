
const SERVER_IP = '10.200.66.207'

export function getServerIp(){
    return SERVER_IP
}
export function getSmartPhoneFps(){
    // May be replaced in the future if 
    // quering the device is possible
    STANDARD_SMARTPHONE_FPS = 30
    return STANDARD_SMARTPHONE_FPS
}


export function getBaseUrl(){
    // Should be replaced wit the actual domain name eventually
    return `http://${getServerIp()}:8000`
}