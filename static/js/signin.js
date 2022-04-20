const signinupBtn = document.querySelector('#signin-up-btn');
const signpage=document.querySelector('.signpage')
const signCloseBtn = signpage.querySelectorAll('.close-btn')
const signContainers = document.querySelectorAll('.sign-container')
const signoutBtn=document.querySelector('#signout-btn')
const memberPage=document.querySelector('.nav-link #member-page')
const emailPattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;



//showup sigin or signup
function showUpSignpage(){
    signpage.classList.add('showup');
}
signinupBtn.addEventListener('click',showUpSignpage);

// 離開登入、註冊欄位
function cancelshowUpSignpage(){
    signpage.classList.remove('showup');
}

//變換登入、註冊欄位
function changeSignContainer(){
    signContainers.forEach(container=>{
        container.classList.toggle('show');
    })
}

signContainers.forEach(container => {
    const convertBtn = container.querySelector('.convert-sign');
    convertBtn.addEventListener('click', changeSignContainer);
})


signCloseBtn.forEach(btn => {
    btn.addEventListener('click',cancelshowUpSignpage);
})

signpage.addEventListener('click', e => {
    if( e.composedPath()[0]===signpage){
        cancelshowUpSignpage()
    }
})


// 登入、註冊功能
const signupForm = document.querySelector('#signup');
const signinForm = document.querySelector('#signin');
const userapi = '/api/user';

// 註冊
async function signup(e){
    e.preventDefault();
    if(isValid("signup")){
        let data = {
            name : this.querySelector('input[name="name"]').value,
            email : this.querySelector('input[name="email"]').value,
            password : this.querySelector('input[name="password"]').value 
        }
        await fetch(userapi, {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json'
              }),
            body: JSON.stringify(data)
          
        })
        .then(res => {
            return res.json();
    
        })
     
        .then(result => {
           
            const message = this.querySelector('.message');
            
            if(result.ok){
                message.innerText = '註冊成功';
            }else{
                message.innerText = result.message;
            }
        })

    }


   
}
signupForm.addEventListener('submit', signup)

//登入
async function signin(e){
    e.preventDefault()
    if(isValid("signin")){
        let data ={
            email:this.querySelector('input[name="email"]').value,
            password:this.querySelector('input[name="password"]').value
        }
        await fetch(userapi,{
            method:'PATCH',
            headers: new Headers({
                'Content-Type': 'application/json'
              }),
            body: JSON.stringify(data)
        })
        .then(res=>{return res.json();})
         //如果有成功登入，回到原本頁面並將「註冊｜登入」按鈕改為「登出」按鈕
        .then(result=>{
            if (result.ok){
                cancelshowUpSignpage();
                signinCheck();
                signinupBtn.classList.remove('show');
                signoutBtn.classList.add('show');
                memberPage.classList.add('show');
            
            }
      
            else{ 
                const message = this.querySelector('.message');
                message.innerText = result.message;
            }
          
        })
    }

}
signinForm.addEventListener('submit', signin)




//進入頁面後先檢查使用者有沒有登入
 async function signinCheck(){
    await fetch(userapi,{method:'GET'})
        .then(res => res.json())
        .then(result => {
            if(result.data){
                signinupBtn.classList.remove('show');
                signoutBtn.classList.add('show');
                memberPage.classList.add('show');
               
               
            }else{
                signinupBtn.classList.add('show');
                signoutBtn.classList.remove('show');
                memberPage.classList.remove('show');
                
            }
        })
}
signinCheck()
//登出
function signout(){
    fetch(userapi, {
        method: 'DELETE'
    })
    .then(() => {
        location.reload();

    })
}

signoutBtn.addEventListener('click', signout);


async function bookingsigninCheck(e){
    await fetch(userapi,{method:'GET'})
        .then(res => res.json())
        .then(result => {
            if(result.data){
                location.replace('/booking')
            }else{

                showUpSignpage()
            }
        })
}
const bookingPage= document.querySelector('.nav-link #booking-page')
bookingPage.addEventListener('click',bookingsigninCheck)




const memberapi=`/api/member`


memberPage.addEventListener("click",async(e)=>{
    const response=await fetch(userapi);
    const promise=await response.json();
    const result =await promise;
    if (result.data){
        location.replace('/member')
            
        }else{
            showUpSignpage();
        }
});



// navbar ham icon
const ham = document.querySelector('.ham')
const navLink = document.querySelector('.nav-link')

function toggleNavLink(){
    navLink.classList.toggle('show')
}

ham.addEventListener('click', toggleNavLink)

//註冊or登入前確認每項input是否valid
function isValid(checkStatus) {
    let isValid = true;
    const checkList = document.querySelectorAll(`[input-type=${checkStatus}]`);
    for(const checkItem of checkList) {
        if(checkItem.classList.contains("invalid")) {
            isValid = false;
            continue;
        }
        const input = checkItem.querySelector("input");
        // 驗證欄位
        const checkResult = checkData(input.name, input.value);
        // 顯示驗證訊息
        renderCheck(checkItem, checkResult);
        if(checkResult) {
            isValid = false;
        }
    }
    return isValid;
}

function checkData(inputName, inputValue) {
    switch(inputName) {
        case "name":
            if(!inputValue) {
                return "姓名不可為空白";
            }
            break;
        case "email":
            if(!inputValue) {
                return  "電子信箱不可為空白";
            }
            if (!emailPattern.test(inputValue)) {
                return  "電子信箱格式錯誤";
            }
            break;
        case "password":
            if(!inputValue) {
                return  "密碼不可為空白";
            }
            if(inputValue.length < 3) {
                return "密碼長度需超過3位";
            }
            break;
        default:
            break;
    }
    // 驗證成功
    return false;
}


signpage.addEventListener("focusout", (e) => {
    const target = e.target;
    if(target.nodeName == "INPUT") {
        // 驗證欄位
        const checkResult = checkData(target.name, target.value);
        // 顯示驗證訊息
        renderCheck(target.parentElement, checkResult);
    }
});

function renderCheck(parent, checkResult) {
    const message = parent.querySelector(".user-input-msg > span");
    if(checkResult) {
        // input 加上效果
        parent.classList.add("invalid");
        parent.classList.remove("valid");
        // 訊息 加上效果
        message.textContent = checkResult;
        message.parentElement.classList.add("invalid");
        message.parentElement.classList.remove("valid");
    } else {
        // input 移除效果
        parent.classList.remove("invalid");
        parent.classList.add("valid");
        // 訊息 加上效果
        message.innerText = "驗證成功";
        message.parentElement.classList.remove("invalid");
        message.parentElement.classList.add("valid");
    }
}



