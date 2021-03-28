function join(){
    var name = document.getElementById("name").value;
    var room = document.getElementById("room").value;
}

var createButton = document.getElementById('create_button');
createButton.onclick = create;

function create() {
    var name = document.getElementById('name').value;
    var room = document.getElementById('room').value;
    window.location.href = "/room/"+room+"?user="+name;
}