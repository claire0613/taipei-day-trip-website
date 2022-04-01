const signinupBtn = document.querySelector('#signin-up-btn');
const signpage=document.querySelector('.signpage')
const signCloseBtn = signpage.querySelectorAll('.close-btn')
const signContainers = document.querySelectorAll('.sign-container')
const signoutBtn=document.querySelector('#signout-btn')




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
signupForm.addEventListener('submit', signup)
async function signin(e){
    e.preventDefault()
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
            try{ getBookingData() }catch(e){};
        }
  
        else{ 
            const message = this.querySelector('.message');
            message.innerText = result.message;
        }
      
    })
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
               
               
            }else{
                signinupBtn.classList.add('show');
                signoutBtn.classList.remove('show');
                
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
        signinCheck();

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
