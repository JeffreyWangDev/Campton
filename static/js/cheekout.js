
async function additem(){
    const itemnum = document.getElementById('item_number').value;
    var ress = await fetch("/api/getitem?itemnum="+itemnum);
    var res =  await ress.json();
    console.log(res)
    if(res["res"]==1){
        var tf = true;
        if(res["data"][0][7].toString()==0){ 
            
        
        var rowl = document.getElementById("all").rows.length;
        for(let i =0;i<rowl;i++){
            var j = document.getElementById("all").rows[i].cells[0].innerHTML;
            //console.log(j);
            ///console.log(res["data"][0][3]);
            console.log(document.getElementById("all").rows[i].cells[2].innerHTML)
            price = price+parseInt(document.getElementById("all").rows[i].cells[2].innerHTML);
            if(j.toString() == res["data"][0][3].toString()){
                console.log(j);
                console.log(res["data"][0][3]);
                tf=false;
            } 
        console.log(tf)
        }
        if(tf){
            var table = document.getElementById("all"); 
            var row = table.insertRow(-1);
            var no = row.insertCell(0);
            var name = row.insertCell(1);
            var price = row.insertCell(2);
            no.innerHTML = res["data"][0][3];
            name.innerHTML = res["data"][0][5];
            price.innerHTML = res["data"][0][4];
            document.getElementById('item_number').value="";
            var price = 0;
            var rowl = document.getElementById("all").rows.length;
            for(let i =1;i<rowl;i++){
                var j = document.getElementById("all").rows[i].cells[2].innerHTML;
                //console.log(j);
                ///console.log(res["data"][0][3]);
                console.log(j)
                price = price+parseInt(j);
                if(j.toString() == res["data"][0][3].toString()){
                    console.log(j);
                    console.log(res["data"][0][3]);
                    tf=false;
                }
            }
            document.getElementById('numitem').value=rowl-1;
            document.getElementById('total').value=price;
        }else{
            alert("Error: Item already added!");
        }
    }else{
        alert("Error: Item already sold!");
    }
    }else{
        console.log("error!!!!")
        alert(res["data"])
    }
}


async function submit(){
    var all = {} 
    var rowl = document.getElementById("all").rows.length;
    for(let i =1;i<rowl;i++){
        var j = document.getElementById("all").rows[i].cells[0].innerHTML;
        all[i]=j;
    }
    if(!all[1]){
        
        alert("Please add items before submiting")
    }else{
        if (confirm("Please confirm the checkout is with the correct item id's and that the user has paid: ") == true) {
            var res = await fetch("/api/postitems", {
                method: "POST",
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify(all)
              })
                var resp = await res.json()
                if(res.status == 200){
                    window.location.href = "/?msg=Checkout+complete";
                }else{
                    console.log(resp)
                    alert(resp["status"])
                }
   
        }
    }

    
}
