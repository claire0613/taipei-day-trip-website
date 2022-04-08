const ordernumId=document.URL.split('=').slice(-1)
let orderNumDiv=document.querySelector('.orderNum')
let orderName=document.querySelector('.ordername')
let paystatus=document.querySelector('.status')
let totalPriceDiv=document.querySelector('.totalPrice')
let orderinfoContain=document.querySelector('.orderinfo-container')
let orderStatus=document.querySelector('.orderstatus')
let thankapi=`api/order/${ordernumId}`

async function get_order(){
    let request=await fetch(thankapi)
    let res=await request.json()
    if (res){
        orderNumDiv.innerText=res.data.number;
        orderName.innerText=res.data.contact.name;
        totalPriceDiv.innerText=res.data.totalPrice;
        paystatus.innerText=res.data.status;
        if (res.data.status==0){
            orderStatus.innerText='行程預定成功'
        }else{
            orderStatus.innerText='行程預定失敗'
            orderStatus.style.color='red'
        }


    }
}
async function getUserData(){
    fetch(userapi)
    .then(res => res.json())
    .then(result => {
        if(result.data != null){
            get_order()
            
        }else{
            orderinfoContain.innerHTML=''
            location.replace('/');
        }
    })
}
getUserData()
