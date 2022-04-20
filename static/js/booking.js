
// api資料
const bookingapi = '/api/booking'
const bookingBox = document.querySelector('.booking-box')
const title = document.querySelector('.title')
const bookingOrderForm=document.querySelector('.booking-order')
const inputName=bookingOrderForm.querySelector('input[name="name"]')
const inputEmail = bookingOrderForm.querySelector('input[name="email"]')
const orderapi='/api/orders'
const errorMessage = document.querySelector('.error-msg')
const phonePattern=/09[0-9]{8}/
let userid=null


class TotalPrice{
    constructor(){
        this._totalprice=0
    }
    get addPrice(){
        return this._totalprice
    }
    set addPrice(value){
        this._totalprice+=value
    }
}
let totalPrice = new TotalPrice;
async function getUserData(){
    fetch(userapi)
    .then(res => res.json())
    .then(result => {
        if(result.data != null){
            title.innerText = `您好，${result.data.name}，待預定的行程如下：`
            inputName.value = result.data.name
            inputEmail.value = result.data.email
            userid=result.data.id
            
        }else{
            location.replace('/');
        }
    })
}

getUserData()

// 獲取行程資料
async function getBookingData(){
    bookingBox.innerHTML = ''
    await fetch(bookingapi)
    .then(res => res.json())
    .then(result=>(result.data))
    .then(bookings => {
        const trip=[]
      
        if (bookings!==null){
        bookings.forEach(booking => {
     
            let trip_item={
                "attraction":
                    {
                        "id":booking.attraction.attractionId,
                        "name": booking.attraction.name,
                        "address":booking.attraction.address,
                        "image":booking.attraction.image
                    },
                    "date": booking.date,
                    "time":booking.time,
                    }
            trip.push(trip_item)
            
            //行程listform
            const scheduleForm = document.createElement('form')
            scheduleForm.classList.add('scheduleForm')
            //img
            const attractionImg = document.createElement('img')
            attractionImg.src = booking.attraction.image
            //infoBox
            const infoBox = document.createElement('div')
            infoBox.classList.add('info-box')
            //景點名稱         
            const attractionName = document.createElement('h4')
            attractionName.innerText = `台北一日遊：${booking.attraction.name}`
            //deletion icon
            const deleteBtn = document.createElement('Button')
            const deleteicon=document.createElement('img')
            deleteicon.src="/static/icons/icon_delete.png"
            deleteBtn.type = 'submit'
            deleteicon.classList.add('delete-icon')
            deleteBtn.append(deleteicon)
            //booking id (invisible)
            const bookingId=document.createElement('input')
            bookingId.style.display='none'
            bookingId.classList.add('bookingId')
            bookingId.value = booking.bookingId
    
            const dateBox = document.createElement('div')
            const dateLabel = document.createElement('label')
            const dateSpan = document.createElement('span')
            dateLabel.innerText = '日期：'
            dateSpan.innerText = booking.date
            dateBox.append(dateLabel, dateSpan)
    
            const timeBox = document.createElement('div')
            const timeLabel = document.createElement('label')
            const timeSpan = document.createElement('span')
            timeLabel.innerText = '時間：'
            timeSpan.innerText = (booking.time == 'morning')? '早上 9 點到下午 4 點': '下午 2 點到晚上 9 點'
            timeBox.append(timeLabel, timeSpan)
    
            const priceBox = document.createElement('div')
            const priceLabel = document.createElement('label')
            const priceSpan = document.createElement('span')
            priceLabel.innerText = '費用：'
            priceSpan.innerText = booking.price
            priceBox.append(priceLabel, priceSpan)
        
            const addressBox = document.createElement('div')
            const addressLabel = document.createElement('label')
            const addressSpan = document.createElement('span')
            addressLabel.innerText = '地點：'
            addressSpan.innerText = booking.attraction.address
            addressBox.append(addressLabel, addressSpan)
            infoBox.append(attractionName, deleteBtn,bookingId, dateBox, timeBox,priceBox,addressBox)
            scheduleForm.append(attractionImg, infoBox)
            bookingBox.append(scheduleForm)
            totalPrice.addPrice=booking.price
  
        });
        //有booking時的頁面呈現
        isBooking()
        function orderSubmit(e) {
            e.preventDefault();
            // 取得 TapPay Fields 的 status 
            const tappayStatus = TPDirect.card.getTappayFieldsStatus()
             // 確認是否可以 getPrime
             if (tappayStatus.canGetPrime === false) {
                alert('can not get prime')
                return
            }
        
            // Get prime  讓 button click 之後觸發 getPrime 方法
             
            TPDirect.card.getPrime((result) => {
                //status=錯誤代碼，0 為成功
                if (result.status !== 0) {
                    alert('get prime error ' + result.msg)
                    return
                }
                let prime=result.card.prime
               
                // alert('get prime 成功，prime: ' + result.card.prime)
                // send prime to your server, to pay with Pay by Prime API .
                // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api

                let name=this.querySelector('input[name="name"]').value
                let email= this.querySelector('input[name="email"]').value
                let infoContain=document.querySelector('.Info-container')
    
                data={
                    prime: prime,
                    order: {
                        price: totalPrice.addPrice,
                        trip: trip,
                        contact: {
                            name: name,
                            email:email,
                            phone: document.querySelector('input[name="phone"]').value,
                            }
                        }
                    }
                   
                    fetch(orderapi, {
                        method: 'POST',
                        body: JSON.stringify(data),
                        headers: new Headers({
                            'Content-Type': 'application/json'
                        })
                    })
                    .then(res=>res.json())
                    .then(result=>{
                        let resultorderNum;
                        if(result.data != undefined){
                                errorMessage.innerText = result.data.payment.message
                                resultorderNum=result.data.number
                            } else{
                            errorMessage.innerText =  result.message.details
                            resultorderNum=result.message.number                 
                        } 

                    location.replace('/thankyou?number='+resultorderNum)
                    })

                }
                
            )
        
        }
        bookingOrderForm.addEventListener('submit',orderSubmit)

    }else{
        //沒有booking時的頁面呈現
        noBooking()
    }
    
});
}





// 刪除行程
function deleteBooking(e){
    e.preventDefault();
    const bookingId = this.querySelector('input.bookingId')
    id=bookingId.value
    fetch(bookingapi, {
        method: 'DELETE',
        body: JSON.stringify({"bookingId": id }),
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .then(result => {        
        getBookingData()
       
    })
}


// 沒有任何行程時不顯示表單
function noBooking(){
    const noBooking = document.createElement('div')
    noBooking.innerText = '目前沒有任何待預定的行程'
    noBooking.classList.add('notice')
    bookingOrderForm.classList.remove('show')
    bookingBox.append(noBooking)
  
}
function isBooking(){
    //顯示下方資訊表單
    bookingOrderForm.classList.add('show')
    //總價格
    const showtotalPrice=document.querySelector('.total-price')
    showtotalPrice.innerHTML=totalPrice.addPrice
    //reconfirm all booking form
    const scheduleForms = document.querySelectorAll('form.scheduleForm')
    scheduleForms.forEach(form => {
        form.addEventListener('submit', deleteBooking)
    })
    
}

getBookingData();

// const scheduleForm = document.createElement('form.scheduleForm')
// $(document).on('submit',scheduleForm,deleteBooking);
// scheduleForm.addEventListener('submit', deleteBooking)


// TapPay付款相關函式
// 設置好等等 GetPrime 所需要的金鑰
TPDirect.setupSDK(124040, 'app_u0KOcvz4md0vhyEfU4nojM7K9wiIy1jEC2GYreFXVMwlJzF3kEfRV4hHSMcU', 'sandbox')

// 把 TapPay 內建輸入卡號的表單給植入到 div 中
// Display ccv field
TPDirect.card.setup({
    fields: {
        number: {
            element: '#card-number',
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            element: '#card-expiration-date',
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'CVV'
        }
    },
    styles: {
        // Style all elements
        'input': {
            'color': '#666666'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        }
    }
})

const orderBtn = document.querySelector('#order-btn')
const tappayErrorMsg=document.querySelector('.tappay-error')
//得知目前卡片資訊的輸入狀態
TPDirect.card.onUpdate(function(update) {
    if (update.canGetPrime) {
        tappayErrorMsg.innerHTML=""
       
        orderBtn.removeAttribute('disabled')
    } else {
        orderBtn.setAttribute('disabled', true)
    }
    // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
    if (update.cardType === 'visa') {
        // Handle card type visa.
    }

  })


// orderBtn.addEventListener('submit',orderSubmit)
// $(document).on('submit',orderBtn,orderSubmit);


