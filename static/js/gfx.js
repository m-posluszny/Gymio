import {playersList} from '/static/js/game.js';
//import {io} from '/static/js/game.js';

const mainCanvas = document.querySelector('#main_canvas');
const canvContext = mainCanvas.getContext('2d');

var x = mainCanvas.width / 2;
var y = mainCanvas.height - 30;

var dx = 2;
var dy = -2;

drawBackground();
// console.log(io);

function drawBall() {
    canvContext.beginPath();
    canvContext.arc(x, y, 10, 0, Math.PI*2);
    canvContext.fillStyle = "#0095DD";
    canvContext.fill();
    canvContext.closePath();
}

function drawPlayers() {
    for (const player of playersList) {
        canvContext.drawImage(player.image, player.x, player.y);
    }
}

function drawBackground() {
    mainCanvas.style.background = "url('https://image.freepik.com/darmowe-zdjecie/phuket-beach-tajlandia_38810-691.jpg')";
    mainCanvas.style.backgroundRepeat = "space";
    mainCanvas.style.backgroundPosition = "center";
    mainCanvas.style.backgroundSize = "contain";
}

function draw() {
    canvContext.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
    drawBall();
    drawPlayers();

    x += dx;
    y += dy;
}
setInterval(draw, 10);