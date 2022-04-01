
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

let id=1;
morning.addEventListener('click', ()=>{
    price.innerText = 2000

})
afternoon.addEventListener('click', ()=>{
    price.innerText = 2500
})


const attractionId = document.URL.split('/').slice(-1); 
let apiurl=`/api/attraction/`+attractionId;



async function attractions(){
    if (id==null) {return}

    let result=await fetch(apiurl,{method:"GET"});
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
       
            

    }

}



attractions();
const bookingInfo=document.querySelector('.bookingInfo')
// booking-form submit 
const bookingForm = bookingInfo.querySelector('.bookingform')
const bookingDateInput = bookingForm.querySelector('input[name="date"]')


function bookingSubmit(e){
    e.preventDefault()

    fetch(userapi)
        .then(res => res.json())
        .then(result => {
            // 有登入
            if(result.data){
                let data = {
                    attractionId : parseInt(attractionId),  
                    date : this.querySelector('input[name="date"]').value,
                    time : this.querySelector('input[name="time"]:checked').value,
                    price : parseInt(this.querySelector('#price').innerText)
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
                        const bookingPage = document.querySelector('.nav-link .booking-page')
                        bookingPage.click()
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