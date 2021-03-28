
var socket = io();


function join(){
    var name = document.getElementById("name").textContent;
    var name = document.getElementById("room").textContent;
}

function create() {
    var name = document.getElementById('name').value;
    var room = document.getElementById('room').value;
    socket.on('joined',function(){    window.location.href = "/room/"+room;})
    socket.emit('create_game', {
       
            id: room,
            player_name: name
    });
}