import {playersList, ball} from '/static/js/game.js';
//import {io} from '/static/js/game.js';

const mainCanvas = document.querySelector('#main_canvas');
const canvContext = mainCanvas.getContext('2d');

drawBackground();
// console.log(io);

function drawBall() {
    canvContext.beginPath();
    canvContext.arc(ball.x, ball.y, 20, 0, Math.PI*2);
    canvContext.fillStyle = "#0095DD";
    canvContext.fill();
    canvContext.closePath();
}

function drawPlayers() {
    for (var key in playersList) {
        let player = playersList[key]
        canvContext.drawImage(player.image, player.x, player.y);
    }
}

function drawBackground() {
    mainCanvas.style.background = "url('https://image.freepik.com/darmowe-zdjecie/phuket-beach-tajlandia_38810-691.jpg')";
    mainCanvas.style.backgroundRepeat = "space";
    mainCanvas.style.backgroundPosition = "center";
    mainCanvas.style.backgroundSize = "cover";
    mainCanvas.style.width = 1200;
}

function draw() {
    canvContext.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
    drawBall();
    drawPlayers();
}
setInterval(draw, 60);