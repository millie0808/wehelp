function confirmDelete(){
    if(confirm("確定要刪除這則留言嗎？")){
        return true;
    }
    return false;
}
function checkMessage(){
    let newMessage = document.querySelector('input[name="message"]').value;
    if(newMessage == null || newMessage == ''){
        alert("請輸入留言")
        return false;
    }
    return true;
}
function searchName(){
    let usernameForSearch = document.querySelector('input[name="username"]').value;
    if(usernameForSearch == null || usernameForSearch == ''){
        alert("請輸入要搜尋的帳號");
    }else{
        let endpoint = "http://127.0.0.1:3000/api/member";
        let queryString = "?username="+usernameForSearch;
        fetch(endpoint+queryString,{method:'GET'})
            .then(response => response.json())
            .then(function(result){
                let resultElem = document.querySelector("#searchNameResult");
                if(result.data){
                    resultElem.style.display = "block";
                    resultElem.innerHTML = `${result.data.name} (${usernameForSearch})`;
                }else{
                    resultElem.style.display = "block";
                    resultElem.innerHTML = "無此會員";
                }
            })
    }
}
function changeName(){
    let newName = document.querySelector('input[name="newName"]').value;
    if(newName == null || newName == ""){
        alert("請輸入新名字");
    }
    else{
        let endpoint = "http://127.0.0.1:3000/api/member";
        fetch(endpoint, {
            method: 'PATCH',
            headers: {
                'Content-type': 'application/json',
            },
            body: JSON.stringify({
                "name": newName,
            })
        }).then(function(changeNameResult){
            if(changeNameResult.ok){
                let resultElem = document.querySelector("#changeNameResult");
                resultElem.style.display = "block";
                resultElem.innerHTML = "更新成功";
                // 調整歡迎名字及留言板名字
                let oriNameElem = document.querySelectorAll(".ifChangeNameOri");
                for(let i=0; i<oriNameElem.length; i++){
                    oriNameElem[i].style.display = "none";
                }
                let newNameElem = document.querySelectorAll(".ifChangeNameNew");
                for(let i=0; i<newNameElem.length; i++){
                    newNameElem[i].style.display = "contents";
                    newNameElem[i].innerHTML = newName;
                }
            }
        });
    }
}