
var url_string =  window.location.href
var url = new URL(url_string);

var room = url_string.split("/")
var room = room[room.length-1].split("?")[0]

function join() {
    var name = document.getElementById("name").value;
     window.location.href = "/room/"+room+"?user="+name;
}
