
let imgbox=document.querySelector(".imgBox")
let ol=document.querySelector("#ol")
let profile=document.querySelector('.profile')
let detail=document.querySelector('.detail')
let addressDiv=detail.querySelector('.address');
let transportDiv=detail.querySelector('.transport');
let descriptionDiv=detail.querySelector('.description');
let rightbtn=document.querySelector('#rightbtn')
let leftbtn=document.querySelector('#leftbtn')
let morning = profile.querySelector('input[value="morning"]')
let afternoon = profile.querySelector('input[value="afternoon"]')
const tripDate=document.querySelector('#date')
const dateInputDiv=document.querySelector('.date-input-div')
let priceSpan=document.querySelector('#price')
let id=1;
const attractionId = document.URL.split('/').slice(-1); 
let attractionapi=`/api/attraction/`+attractionId;




async function attractions(){
    if (id==null) {return}

    let result=await fetch(attractionapi,{method:"GET"});
    let data=await result.json();
    //寫入images 和 img_index
    if (data["data"]){
        let pictures=data.data.images
        pictures.forEach(imgurl => {
            const img = document.createElement('img');
            img.src =imgurl;
            img.alt="No picture"
            imgbox.appendChild(img)
        });
        const showimg = imgbox.querySelectorAll('img')
        showimg[0].classList.add('show')
        //製作circle在底部連動顯示的照片
        for (i=0;i<pictures.length;i++){
            let ol_li=document.createElement('li');
            ol.append(ol_li);
            ol_li.id=i+1;
            ol_li.addEventListener('click',function(){
                let index=this.id;
                console.log(index)
                for (let i=0;i<ol.children.length;i++){
                    ol.children[i].className = '';
                    showimg[i].className='';
                }
                this.classList.add('now');
                showimg[index-1].classList.add('show');

            })
        }
        const index=ol.querySelector('li');
        index.classList.add('now');

        const name=profile.querySelector('.name');
        name.innerText=data.data.name;
        const category=profile.querySelector('#category');
        category.innerText=data.data.category;
        const mrt=profile.querySelector('#mrt');
        mrt.innerText=data.data.mrt;
        
        const description=document.createElement('p');
        const address=document.createElement('p');
        const transport=document.createElement('p');
        description.innerText=data.data.description;
        address.innerText=data.data.address;
        transport.innerText=data.data.transport;
        descriptionDiv.appendChild(description);
        addressDiv.appendChild(address);
        transportDiv.appendChild(transport);

        //按右鍵切換
        let circle=0;
        rightbtn.addEventListener('click',function(){
            circle++;
            if(circle==ol.children.length){
                circle=0;
            }
            for(let i =0;i<ol.children.length;i++){
                ol.children[i].className = '';
                showimg[i].className='';
            }
            ol.children[circle].classList.add('now');
            showimg[circle].classList.add('show');
        }
        )
        
        //按左鍵切換
        leftbtn.addEventListener('click',function(){
 
            circle--;
            if(circle<0){
                circle=0;
            }
            for(let i =0;i<ol.children.length;i++){
                ol.children[i].className = '';
                showimg[i].className='';
            }
            ol.children[circle].classList.add('now');
            showimg[circle].classList.add('show');
        }
        )
        
        let autorun= function(){
                timer=setInterval(() => {rightbtn.click();
            
                }, 2500);
            }
           
            imgbox.addEventListener("mouseenter",function(){
                clearInterval(timer);
                
            })
            imgbox.addEventListener("mouseleave",function(){
                autorun();
                
            })
            autorun();
            // 設定預定日期：明日到近三個月
            const today = new Date();
            const tomorrow = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1);
            const afterThreeMonth = new Date(tomorrow.getFullYear(), tomorrow.getMonth() + 3, tomorrow.getDate());
            tripDate.setAttribute("min", formatDate(tomorrow));
            tripDate.setAttribute("max", formatDate(afterThreeMonth));
     
    }

}
//日期物件轉換成 str 20xx-0x-xx 方式
function formatDate(date) {
    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
}

attractions();





// booking-form submit 
const bookingInfo=document.querySelector('.bookingInfo')
const bookingForm = bookingInfo.querySelector('.bookingform')
const bookingDateInput = bookingForm.querySelector('input[name="date"]')


class Price {
    constructor(){
        this._price=0;
    }
    get bookingTime() {
      return this._price;
    }
    //true=2000元(上午)/false=2500(下午)
    set bookingTime(value) {
      if (value) {
        this._price=2000;
      }else if(!value){
        this._price=2500;
    }
      }
      
  };
let bookingimePrice=new Price;
//default(選上午 2000)
bookingimePrice.bookingTime=true;
//監聽選擇上午or下午
morning.addEventListener('click', ()=>{
    bookingimePrice.bookingTime=true;
    priceSpan.innerText = 2000;
})
afternoon.addEventListener('click', ()=>{
    bookingimePrice.bookingTime=false;
    priceSpan.innerText = 2500;
})

//booking按鈕 表單提交
function bookingSubmit(e){
    e.preventDefault();
    const message=document.querySelector('.trip-date-msg')
    // 檢核是否有輸入日期
    if(tripDate.value) {
        dateInputDiv.classList.remove("error");
    } else {
        dateInputDiv.classList.add("error");
        message.classList.add("show");
        message.textContent = "請選擇日期";
        return;
    }
    fetch(userapi)
        .then(res => res.json())    
        .then(result => {
            // 有登入
            
            if(result.data){

                let data = {
                    attractionId : parseInt(attractionId),  
                    date : this.querySelector('input[name="date"]').value,
                    time : this.querySelector('input[name="time"]:checked').value,
                    price : bookingimePrice.bookingTime
                }
                const bookingapi = '/api/booking'
                //將資料傳進後端
                fetch(bookingapi, {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: new Headers({
                        'Content-Type': 'application/json'
                    })
                })
                .then(res => res.json())
                .then(result => {
                    if(result.ok === true){
                        
                        location.replace('/booking')
                    }else{
                        alert(result.message)
                    }
                })
            }else{  // 沒登入
                showUpSignpage()
            }
        })
}

bookingForm.addEventListener('submit', bookingSubmit)



