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
function transformNext(event) {
    const slideNext = event.target;
    const slidePrev = slideNext.previousElementSibling;
    const champContainer = slideNext.parentElement.parentElement.nextElementSibling;
    let activeLi = champContainer.getAttribute('data-position');
    const champList = champContainer.getElementsByClassName('champion');
    //data-position이 0이하이면 오른쪽버튼 활성화
    if (Number(activeLi) < 0) {
        activeLi = Number(activeLi) + 160;

        slidePrev.style.color = "#000000";
        slidePrev.classList.add('slide-prev-hover');
        slidePrev.addEventListener('click', transformPrev);

        if (Number(activeLi) === 0) {
            slideNext.style.color = "#808080";
            slideNext.classList.remove('slide-next-hover');
            slideNext.removeEventListener('click', transformNext);
        }
    }
    champContainer.style.transition = 'transform 1s';
    champContainer.style.transform = 'translateX(' + String(activeLi) + 'px)';
    champContainer.setAttribute('data-position', activeLi);
}



function transformPrev (event) { //어떤 event 실행되었는지, event가 발생한 요소
    const slidePrev = event.target; //해당 event가 발생한 요소
    const slideNext = slidePrev.nextElementSibling;
    const champContainer = slidePrev.parentElement.parentElement.nextElementSibling;
    let activeLi = champContainer.getAttribute('data-position');
    const champList = champContainer.getElementsByClassName('champion');

    if (champContainer.clientWidth < (champList.length * 160) + Number(activeLi)) { //우측에 여전히 챔프원소 있는경우
        activeLi = Number(activeLi) - 160;
        

        if (champContainer.clientWidth > (champList.length * 160) + Number(activeLi)) { // 위에서 이동을 시키고나서, 우측에 넘치지 않는 경우
            slidePrev.style.color = "#808080";
            slidePrev.classList.remove('slide-prev-hover');
            slidePrev.removeEventListener('click', transformPrev);
            
        }
        slideNext.style.color = "#000000";
        slideNext.classList.add('slide-next-hover');
        slideNext.addEventListener('click', transformNext);
    }
    champContainer.style.transition = 'transform 1s';
    champContainer.style.transform = 'translateX(' + String(activeLi) + 'px)';
    champContainer.setAttribute('data-position', activeLi);
}

const slidePrevList = document.getElementsByClassName("slide-prev");

for (let i = 0 ; i < slidePrevList.length ;i++) {
    let container = slidePrevList[i].parentElement.parentElement.nextElementSibling;
    let champList = container.getElementsByClassName("champion");
    
    if (container.clientWidth < (champList.length * 160)) {
        slidePrevList[i].classList.add('slide-prev-hover');
        slidePrevList[i].addEventListener('click', transformPrev); //처음에는 왼쪽에 붙어있으므로 왼쪽으로 이동하는것만 활성화
    } else {
        // const arrowBox = slidePrevList[i].parentElement;
        // arrowBox.removeChild(slidePrevList[i].nextElementSibling);
        // arrowBox.removeChild(slidePrevList[i]);
    }
    
}