var video = document.querySelector('video');
var canvas = document.getElementById('canvas');     

var constraints = {
    video: true,
    audio: false
};
var socket = io();
socket.on('connect', mainLoop());
socket.on('camera_b64_resp',get_cam)
// var url = "";
// var socket = new WebSocket(url);

captureCamera(video);

function get_cam(data) {    
    console.log("")

}


function mainLoop() {    
    // document.querySelector('#print_result').innerHTML = toBase64();
    b64 = toBase64();
    setTimeout(mainLoop, 60);
    socket.emit('camera_b64', { data: b64 });
}

function captureCamera() {    
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
        video.play();
        
    }).catch((error) => {
        
    });
}

function toBase64() {
    canvas.width = 200;
    canvas.height = 200;
    canvas.getContext('2d').drawImage(video, 0, 0, 200,200);
    return canvas.toDataURL();     
}