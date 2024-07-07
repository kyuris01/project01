const button = document.getElementById("tip_button");
button.addEventListener("click", askTips);

const apiUrl = 'https://api.openai.com/v1/chat/completions';
let apiKey;

fetch('/routing/env', {method:'POST'})
  .then((res)=>{ 
    return res.json();
  })
  .then((data) => {
    apiKey = data.key;
  })


function askTips() {
    const my_champ = document.getElementById('me').value;
    const opp_champ = document.getElementById('opp').value;
    const line = document.getElementById('line').value;
    const tipbox = document.getElementById('tipbox');
    const data = {
        model : "gpt-3.5-turbo",
        messages : [
            {role: "system", content: "너는 리그오브레전드에서 챔피언 1대1 매치업에서 나의 챔피언과 상대챔피언의 상성에 따른 플레이 팁을 알려주는 도우미야"},
            {role: "user", content: `리그오브레전드 게임에서, ${line} 포지션에서 내가 ${my_champ} 챔피언을 플레이하고 상대방이 ${opp_champ} 일때의 상대하는 팁을 알려줘`}
        ]
    }
    
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
          },
          body: JSON.stringify(data)
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log('Success:', data.choices[0].message.content);
        tipbox.innerText = data.choices[0].message.content;
    })
}