function save_timezone() {
    let data = new FormData();
    data.append("time_zone", Intl.DateTimeFormat().resolvedOptions().timeZone);
    xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://127.0.0.1:5000/save_timezone");
    xhttp.send(data);
}