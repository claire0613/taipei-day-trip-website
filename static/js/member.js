

const orderList=document.querySelector('.order-list')
const userCaptial=document.querySelector('.user-captial')
const userNameAuto=document.querySelector('.username-auto')
const userEmail=document.querySelector('#email')
const userNameSave=document.querySelector('.username-save')
const userNameEdit=document.querySelector('.username-edit')
const userNameEditIcon=document.querySelector('#username-edit-icon')
const userNameSaveIcon=document.querySelector('#username-save-icon')
const modifiedMsg=document.querySelector('.modified-msg')
const pwdSave=document.querySelector('.pwd-save')
const pwdEdit=document.querySelector('.pwd-edit')
const pwdEditIcon=document.querySelector('#pwd-edit-icon')
const pwdSaveIcon=document.querySelector('#pwd-save-icon')
const memberRightBtn=document.querySelector('#rightbtn')
const memberleftBtn=document.querySelector('#leftbtn')
const memberpageError=document.querySelector('.error-msg')


async function getMemberInfo(){
    const response=await fetch(userapi);
    const promise=await response.json();
    const result =await promise;
    if (result.data){
        userCaptial.innerHTML=result.data.name[0]
        userNameAuto.innerHTML=result.data.name
        userEmail.innerHTML=result.data.email
    }else{
        location.replace('/');
    }
}
let page=0;
let oredernextPage=null;
async function getMemberoder(){
    if (page == null){
        return 
    }
    const orderHisapi = `/api/orders?page=${page}`

    const response= await fetch(orderHisapi)
    const promise=await response.json();
    const result =await promise;
    const ordersLink=await result.data;
    const orderLinkDiv=document.querySelector('.order-link');
    orderLinkDiv.innerHTML="";
    oredernextPage=await result.nextPage;

    
    if (ordersLink!==undefined){
        ordersLink.forEach(order => {
            const orderlink = document.createElement('a');
            orderlink.href = `/thankyou?number=${order['ordernum']}`;
            const ordernumDiv=document.createElement('div');
            ordernumDiv.innerHTML=order['ordernum'];
            ordernumDiv.classList.add('ordernumber');
            const tripDiv=document.createElement('div');
            tripDiv.classList.add('trip-list');
            order['trip'].forEach(attraction=>{
                const tripDetail=document.createElement('div');
                tripDetail.classList.add('trip-list-detail');
                const attrName=document.createElement('div');
                attrName.innerHTML=attraction['attractionName'];
                attrName.classList.add('attr-name');
                const dateDiv=document.createElement('div');
                dateDiv.innerHTML=attraction['date'];
                dateDiv.classList.add('date');
                const priceDiv=document.createElement('div');
                priceDiv.innerHTML=attraction['price'];
                priceDiv.classList.add('price');
                tripDetail.append(attrName,dateDiv,priceDiv);
                tripDiv.append(tripDetail);
            })
            const totalPriceDiv=document.createElement('div');
            totalPriceDiv.innerHTML=order['totalPrice'];
            totalPriceDiv.classList.add('totalprice');
            const orderStatus=document.createElement('div');
            orderStatus.innerHTML=(order['status']==0)?'已付款':'未付款';
            orderStatus.classList.add('status');
            orderlink.append(ordernumDiv,tripDiv,totalPriceDiv,orderStatus);
            orderLinkDiv.append(orderlink);

            memberpageError.innerHTML='';
        });

        }else{
            memberpageError.innerHTML='未曾有訂單';

        }


    }

    memberRightBtn.addEventListener('click',()=>{
        if (oredernextPage !==null){
            page+=1
            getMemberoder();
        }
        
    })
    memberleftBtn.addEventListener('click',()=>{
        if (oredernextPage !==1){
            page-=1
            getMemberoder();
        }
        
    })

userNameEditIcon.addEventListener("click",()=>{
    userNameSave.classList.add('hide');
    userNameEdit.classList.remove('hide');
   

})
userNameSaveIcon.addEventListener('click',async(e)=>{
    const newName=document.querySelector('#newName').value.trim()
    const data={
        "newName":newName,
        "pwd":null
    }
    const option={
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json'
          }),
        body: JSON.stringify(data)
    }
    const response= await fetch('/api/member',option);
    const promise=await response.json();
    const result=await promise;
    if (result.ok){
        modifiedMsg.innerHTML="更新成功"
        userNameSave.classList.remove('hide');
        userNameEdit.classList.add('hide');
        userNameAuto.innerHTML=newName;
        setTimeout(()=>{modifiedMsg.innerHTML='';},2000)

    }else{
        modifiedMsg.innerHTML="更新失敗"
    }
})

pwdEditIcon.addEventListener("click",()=>{
    pwdSave.classList.add('hide');
    pwdEdit.classList.remove('hide');
   

})
pwdSaveIcon.addEventListener('click',async(e)=>{
    const newPwd=document.querySelector('#newPwd').value.trim()
    const data={
        "newName":null,
        "pwd":newPwd
    }
    const option={
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json'
          }),
        body: JSON.stringify(data)
    }
    const response= await fetch('/api/member',option);
    const promise=await response.json();
    const result=await promise;
    if (result.ok){
        modifiedMsg.innerHTML="更新成功"
        pwdSave.classList.remove('hide');
        pwdEdit.classList.add('hide');
        setTimeout(()=>{modifiedMsg.innerHTML='';},2000)

    }else{
        modifiedMsg.innerHTML="更新失敗"
    }
})






getMemberInfo()
getMemberoder()