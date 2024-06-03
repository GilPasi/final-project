
const SERVER_IP = '10.0.0.2'

export function getServerIp(){
    return SERVER_IP
}
export function getSmartPhoneFps(){
    // May be replaced in the future if 
    // quering the device is possible
    STANDARD_SMARTPHONE_FPS = 30
    return 30 
}


export function getBaseUrl(){
    // Should be replaced wit the actual domain name eventually
    return `http://${getServerIp()}:8000`
}