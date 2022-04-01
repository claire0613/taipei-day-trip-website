
// api資料
const bookingapi = '/api/booking'
const bookingBox = document.querySelector('.booking-box')
const title = document.querySelector('.title')
const bookingOrderForm=document.querySelector('.booking-order')
const inputName=bookingOrderForm.querySelector('input[name="name"]')
const inputEmail = bookingOrderForm.querySelector('input[name="email"]')


let userid



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

const errorMessage = document.querySelector('.error-message')
let totalPrice = 0
const prime=document.querySelector('.total-price')

// 獲取行程資料
async function getBookingData(){
    bookingBox.innerHTML = ''
    totalPrice = 0
    await fetch(bookingapi)
    .then(res => res.json())
    .then(result=>result.data)
    .then(booking => {
        if (booking){
            //行程listform
        const scheduleForm = document.createElement('form')
        scheduleForm.classList.add('scheduleForm')
        //img
        const attractionImg = document.createElement('img')
        attractionImg.src = booking.attraction.image
        //infoBox
        const infoBox = document.createElement('div')
        infoBox.classList.add('info-box')

        const attractionName = document.createElement('h4')
        attractionName.innerText = `台北一日遊：${booking.attraction.name}`

        const deleteBtn = document.createElement('Button')
        const deleteicon=document.createElement('img')
        deleteicon.src="/static/icons/icon_delete.png"
        deleteBtn.type = 'submit'
        deleteicon.classList.add('delete-icon')
        deleteBtn.append(deleteicon)
        const bookingId=document.createElement('input')
        bookingId.style.display='none'
        bookingId.classList.add('bookingId')
        bookingId.value = booking.id

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
        const bookingid=document.createElement('div')
        infoBox.append(attractionName, deleteBtn,bookingId, dateBox, timeBox,priceBox,addressBox)
        scheduleForm.append(attractionImg, infoBox)
        bookingBox.append(scheduleForm)
        prime.innerHTML=booking.price
        bookingOrderForm.classList.add('show')

        }  
        
        if(bookingBox.innerText === ''){
            noBooking()
        }
  
    
});
}

// 刪除行程
function deleteBooking(e){
    e.preventDefault();
    const bookingId = this.querySelector('input.bookingId')
    id=bookingId.value
    console.log(id)
    fetch(bookingapi, {
        method: 'DELETE',
        body: JSON.stringify({"userid": id }),
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .then(result => {  
        bookingOrderForm.classList.remove('show')      
        getBookingData()
       
    })
}


// 沒有任何行程時不顯示表單
function noBooking(){
    const noBooking = document.createElement('h4')
    noBooking.innerText = '目前沒有任何待預定的行程'
    noBooking.classList.add('error-message')
    bookingOrderForm.classList.remove('show')
    bookingBox.append(noBooking)
}

getBookingData()
const scheduleForm = document.createElement('form.scheduleForm')
$(document).on('submit',scheduleForm,deleteBooking);
// scheduleForm.addEventListener('submit', deleteBooking)

