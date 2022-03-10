const searchForm = document.querySelector('.desktop form')
const content = document.querySelector('.content')
const footer = document.querySelector('footer')
let page=0;
let keyword='';
let loaingStatus=false;



async function loading(){
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
    if (data["data"]){
        let attractions=data.data
        let fragment = document.createDocumentFragment();
    }


   
    
}





// window.addEventListener('scroll', debounce(renderNextPage))