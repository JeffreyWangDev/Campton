async function getlogs(){
    const pss = document.getElementById('pss').value;
    var ress = await fetch("/api/getlog", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify({"password":pss})
      })
    var res =  await ress.json();
    console.log(res["data"])
    if(res["res"] == 0){
        alert(res["data"])
    }else{
        for(var i =0;i<res["data"].length;i++){
            var table = document.getElementById("all"); 
            var row = table.insertRow(-1);
            var id = row.insertCell(0);
            var ip = row.insertCell(1);
            var user = row.insertCell(2);
            var event = row.insertCell(3);
            var time = row.insertCell(4);
            id.innerHTML = res["data"][i][0];
            ip.innerHTML = res["data"][i][2];
            user.innerHTML = res["data"][i][3];
            event.innerHTML = res["data"][i][1];
            time.innerHTML = res["data"][i][4];
        }
    }
}
async function dowloadlogs(){
    const pss = document.getElementById('pss').value;
    var ress = await fetch("/api/getlog", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify({"password":pss})
      })
    var res =  await ress.json();
    console.log(res)
    if(res["res"] == 0){
        alert(res["data"])
    }
}