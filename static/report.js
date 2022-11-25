function again(){
    window.location.href = "goto?place=report";

}
async function submit(){
    var pnum = document.getElementById("phonen").value
    if (confirm("Please confirm the report is correct: ") == true) {
        var res = await fetch("/r", {
            method: "POST",
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({"phone":pnum})
          })
            var resp = await res.json()
            if(res.status == 200){
                
                alert("Report submited, user may be paid now");
                window.location.href = "/?msg=Cheekout+complete";
            }else{
                console.log(resp)
                alert(resp["status"]);
            }

    }
}

function printfile(){
    var pnum = document.getElementById("phonen").value;
    console.log(pnum.toString);
    window.open("/print_report?phone="+pnum.toString());
}