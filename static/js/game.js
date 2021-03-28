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
socket.on('camera_b64_resp', updateGame)
socket.on('joined',playerJoined)

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

export var playersList = [];



function playerJoined(data) {
    console.log(data)
    console.log("anythin")
    let room = data.room
    let player = room[data.name]
    playersList.push(new Player(data.name,player.position[0],player.position[0], ""))
}


function on_gamestate(data) {
    //console.log(data)
    //document.querySelector('#print_result').innerHTML = toString(data);
}

function on_gamestate(data) {
    if (playersList != undefined) {
        for (let step = 0; step < length(playersList); step++) {
                let name =  playersList[step].name
                playersList[step].image.src = data.data.data;
                playersList[step].x = data[name].pos[0]
                playersList[step].y = data[name].pos[1]
            }
        }
}
mainLoop();
function mainLoop() {    
    // document.querySelector('#print_result').innerHTML = toBase64();
    const b64 = toBase64();
    //convertImgToDataURLviaCanvas()
    socket.emit('camera_b64', { data: b64,room:room });
    setTimeout(mainLoop, 60);
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
    //var scale = Math.min(canvas_1.width / imageWidth, canvas_1.height / imageHeight);
    //var x = (canvas_1.width / 2) - (imageWidth / 2) * scale;
    //var y = (canvas_1.height / 2) - (imageHeight / 2) * scale;
    //canvas_1.getContext('2d').drawImage(video, x, y, imageWidth * scale, imageHeight * scale);
    canvas_1.getContext('2d').drawImage(video, 0, 0, 256, 256);
    return canvas_1.toDataURL('image/jpeg', 0.1);     
}

// function fromBase64(data) {
//     let image = new Image();
//     image.src = data.data.data;
//     image.onload = function() {
//         canvas_2.getContext('2d').drawImage(image, 0, 0);
//     };
// }