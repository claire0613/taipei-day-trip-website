const form = document.querySelector('form')
let content = document.querySelector('.content')
let page=0;
let keyword='';
// let isnextpage=false;
let isfetching=false;

async function loading(){
    isfetching=true;
    
    if (page == null){
        return 
    }
    let apiurl=''
    if (keyword===''){
        apiurl = `/api/attractions?page=${page}`
    }else{
        apiurl = `/api/attractions?page=${page}&keyword=${keyword}`
    }

    let result=await fetch(apiurl,{method:"GET"});
    let data=await result.json();
    let content = document.querySelector('.content')
    if (data["data"]){
        let attractions=data.data
        // let fragment = document.createDocumentFragment();
        
        for (let site of attractions){
            let box = document.createElement('div');
            box.className = 'box'

            let imglink= document.createElement('a')
            imglink.href = `/attraction/${site.id}`
            let img = document.createElement('img');
            img.src = site.images[0]


            let name = document.createElement('a');
            name.href=`/attraction/${site.id}`
            name.className = 'name'
            name.textContent =site.name
            
            let detail=document.createElement('div');
            detail.className = 'detail'
            let mrt=document.createElement('div');
            mrt.textContent =site.mrt
            let category=document.createElement('div');
            category.textContent =site.category

            detail.append(mrt,category)
            imglink.append(img)
            box.append(imglink,name,detail)
            content.appendChild(box)  
        }
        // content.append(fragment)
    }
    page=data["nextPage"]
    isnextpage=false;
    if(content.innerHTML === ''){
        const nodata = document.createElement('h3')   
        nodata.innerText = `無「${keyword}」的景點`
        nodata.style.color = '#666666'
        content.append(nodata)
        
    }
    isfetching=false;
  
    }
 

 function keywordSearch(event){
    event.preventDefault();
    // isnextpage=true;
    let text=document.querySelector('input').value;
    keyword = text;
    page = 0;
    content.textContent = ''
    loading()
    // isnextpage=false;

}



const options = {
    rootMargin: "0px 0px 200px 0px",
    threshold: 0
  }
let callback = ([entry]) => {
        if (entry.isIntersecting) {
            if(!isfetching){
                // setTimeout(loading,1000);
                loading();
            }

  
        }
          
    
      
    
  }


// 設定觀察對象：告訴 observer 要觀察哪個目標元素
const footer = document.querySelector('footer')

// 製作鈴鐺：建立一個 intersection observer，帶入相關設定資訊
let observer = new IntersectionObserver(callback, options)
// // 設定觀察// 觀察目標元素
observer.observe(footer)
form.addEventListener('submit',keywordSearch)













// 滾動時觸發renderNextPage 



// window.addEventListener("DOMContentLoaded", function() {
//     // 選定頁面中帶有 lazy class 名稱的那張圖片
//     let lazyImage = document.querySelector("img.lazy")
    
//     const lazyLoad = function() {
//       // 確認圖片是否進到可視範圍
//       if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0)) {
//         // 確認有才加載圖片
//         lazyImage.src = lazyImage.dataset.src
//         lazyImage.srcset = lazyImage.dataset.srcset
//         lazyImage.classList.remove("lazy")
//         // 完成後就註銷掉 scroll 事件監聽
//         document.removeEventListener("scroll", lazyLoad)
//       }
//     }
  
//     // 註冊 scroll 事件監聽器，使用者滑動頁面觸發 lazyLoad 
//     window.addEventListener('scroll', nextPage);
//   })