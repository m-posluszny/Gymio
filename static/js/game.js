var video = document.querySelector('video');
var canvas_1 = document.getElementById('canvas_1');

var imageWidth = 0;
var imageHeight = 0;

var constraints = {
    video: {
        width: { 
            max: 640, 
            ideal: 320 
        },
        height: { 
            max: 480, 
            ideal: 240 
        },
        resizeMode: "none"
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

socket.on('user_handshake', mainLoop());


socket.on('game_state', on_gamestate);
socket.on('joined',playerJoined)
socket.on('rejected',rejectPlayer)

captureCamera(video);



function get_cam(data) {
    fromBase64(data);
    //document.querySelector('#print_result').innerHTML = toString(data);
}
captureCamera();

class Player {
    constructor(name, x, y, imageBase64) {
        this.x = x;
        this.y = y;
        this.image = new Image();
        this.image.src = imageBase64;
        this.name = name;
    }
}

class Ball {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

export var playersList = {};
export var ball = new Ball(0, 0);


function playerJoined(data) {
    console.log(data)
    console.log("anythin")
    let room = data.room
    let player = room[data.name]
    console.log(room)
    console.log(player)
}

function rejectPlayer(data)
{
    window.location.href = "/"

}

function on_gamestate(data) {
    for (var key in data) {
        if (key != "ball") {
            if (!(key in playersList)) {
                playersList[key] = new Player(data.name, data[key]["position"][0], data[key]["position"][1], data[key]["frame"])
            }
            else {
                playersList[key].image.src = data[key]["frame"];
                playersList[key].x = data[key]["position"][0]
                playersList[key].y = data[key]["position"][1]
            }
        }
    }
    ball.x = data["ball"][0]
    ball.y = data["ball"][1]
    
    // console.log(playersList)
}
mainLoop();
function mainLoop() {    
    // document.querySelector('#print_result').innerHTML = toBase64();
    const b64 = toBase64();
    //convertImgToDataURLviaCanvas()
    socket.emit('camera_b64', { data: b64,room:room,name:username});
    setTimeout(mainLoop, 120);
}

function captureCamera() {    
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
        video.play();
        
        let track = video.srcObject.getTracks()[0];
        if (track.getSettings) {
            imageWidth = track.getSettings().width;
            imageHeight = track.getSettings().height;
            console.log(`${imageWidth}x${imageHeight}`);
        }
    })
    .catch((error) => {
        
    });
}

function toBase64() {
    // var scale = Math.min(canvas_1.width / imageWidth, canvas_1.height / imageHeight);
    // var x = (canvas_1.width / 2) - (imageWidth / 2) * scale;
    // var y = (canvas_1.height / 2) - (imageHeight / 2) * scale;
    // canvas_1.getContext('2d').drawImage(video, x, y, imageWidth * scale, imageHeight * scale);
     canvas_1.getContext('2d').drawImage(video, 0, 0, 320, 240);
    return canvas_1.toDataURL('image/jpeg', 0.6);     
}

// function fromBase64(data) {
//     let image = new Image();
//     image.src = data.data.data;
//     image.onload = function() {
//         canvas_2.getContext('2d').drawImage(image, 0, 0);
//     };
// }