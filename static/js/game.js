var video = document.querySelector('video');
var canvas_1 = document.getElementById('canvas_1');
var canvas_2 = document.getElementById('canvas_2');

// canvas_1.width = 200;
// canvas_1.height = 200;

// canvas_2.width = 200;
// canvas_2.height = 200;     

var constraints = {
    video: {
        width: { min: 640, ideal: 1920 },
        height: { min: 400, ideal: 1080 },
        aspectRatio: { ideal: 1.7777777778 }
    },
    audio: false
};
var frameWidth;
var frameHeight;


var socket = io();
var url_string =  window.location.href
var url = new URL(url_string);
var username = url.searchParams.get("user");
var room = url_string.split("/")
var room = room[room.length-1].split("?")[0]
console.log(username);
console.log(room);

socket.emit('create_game', {
       
    id: room,
    player_name: username
});

socket.on('joined', mainLoop());

socket.on('camera_b64_resp', get_cam);

socket.on('game_state', on_gamestate);

socket.on('players')

captureCamera(video);


function on_gamestate(data) {
    console.log(data)
    //document.querySelector('#print_result').innerHTML = toString(data);
}

function get_cam(data) {
    fromBase64(data);
    //document.querySelector('#print_result').innerHTML = toString(data);
}

function mainLoop() {    
    // document.querySelector('#print_result').innerHTML = toBase64();
    b64 = toBase64();
    setTimeout(mainLoop, 120);
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
    canvas_1.getContext('2d').drawImage(video, 0, 0);
    return canvas_1.toDataURL();     
}

function fromBase64(data) {
    let image = new Image();
    image.src = data.data.data;
    image.onload = function() {
        canvas_2.getContext('2d').drawImage(image, 0, 0);
    };
}