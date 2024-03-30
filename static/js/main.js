const carouselItems = document.querySelectorAll("div#top_lane div.champion");
let i = 1;
console.log(carouselItems)
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
