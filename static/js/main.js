const carouselItems = document.querySelectorAll("div#Hottest div.champion");
//console.log(carouselItems[0]);
let i = 1;
setInterval(() => {   //setInterval은 일정 시간 간격을 두고 함수를 실행하는 메서드임.
    // Accessing All the carousel Items
    carouselItems.forEach((item, index) => {
       if(i < carouselItems.length){
        item.style.transition = 1000 + "ms";
        item.style.transform = `translateX(-${i*100}%)` //템플릿 리터럴 : ${} 문법은 문자열 안에서 변수나 표현식을 쉽게 삽입할 수 있게 해줍니다. 
                                                                        //${} 안에 있는 것은 JavaScript 표현식으로 평가되고 그 결과가 문자열에 삽입됩니다.
       }
    })
    
    
    if(i < carouselItems.length){
        i++;
    }
    else{
        i=0;
    }
},2000)
/*-------------------------------------*/
function transformPrev (event) { //어떤 event 실행되었는지, event가 발생한 요소
    const slidePrev = event.target; //해당 event가 발생한 요소
    const slideNext = slidePrev.nextElementSibling;
    const champContainer = slidePrev.parentElement.parentElement.nextElementSibling;
    let activeLi = champContainer.getAttribute('data-position');
    const champList = champContainer.getElementsByClassName('champion');

    if (champContainer.clientWidth < (champList.length * 160) + Number(activeLi)) { //우측에 여전히 챔프원소 있는경우
        activeLi = Number(activeLi) - 160;
        slideNext.style.color = "#2f3859";
        slideNext.classList.add('slide-next-hover');
    }
    champContainer.style.transition = 'transform 1s';
    champContainer.style.transform = 'translateX(' + String(activeLi) + 'px)';
    champContainer.setAttribute('data-position', activeLi);
}

const slidePrevList = document.getElementsByClassName("slide-prev");

for (let i = 0 ; i < slidePrevList.length ;i++) {
    let container = slidePrevList[i].parentElement.parentElement.nextElementSibling;
    let champList = container.getElementsByClassName("champion");
    console.log()
    if (container.clientWidth < (champList.length * 160)) {
        slidePrevList[i].classList.add('slide-prev-hover');
        slidePrevList[i].addEventListener('click', transformPrev);
    } else {
        const arrowBox = slidePrevList[i].parentElement;
        arrowBox.removeChild(slidePrevList[i].nextElementSibling);
        arrowBox.removeChild(slidePrevList[i]);
    }
    
}


/*
document.getElementsByClassName("champion").addEventListener("click", function() {
    // 클릭한 이미지에 대한 데이터
    var data =  
    // 서버로 데이터를 전송하는 AJAX 요청
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/process_image_click", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
});
*/
