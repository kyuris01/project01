//OPEN AI API를 이용해 gpt에게 챔피언 매치팁을 물어보는 기능
const button = document.getElementById("tip-button");
button.addEventListener("click", askTips);

const apiUrl = "https://api.openai.com/v1/chat/completions";
let apiKey;

const text = `리그 오브 레전드에서 "카밀"로 "아트록스"를 상대하는 것은 도전적일 수 있지만, 몇 가지 전략과 팁을 통해 더 나은 결과를 얻을 수 있습니다. 여기 몇 가지 팁을 제공할게요:

게임 초반 (Early Game)
레벨 1 싸움:

아트록스는 레벨 1에서 약한 편이므로, "정확성의 일격 (Q)" 스킬을 이용해 초반 주도권을 가져갈 수 있습니다.
하지만 그의 "지옥사슬 (W)"에 걸리지 않도록 주의하세요. 걸리면 큰 피해를 입을 수 있습니다.
견제와 무빙:

"전술적 휩쓸기 (W)"로 아트록스를 견제하세요. 이 스킬로 아트록스의 체력을 깎아 주도권을 가져갈 수 있습니다.
아트록스의 "어둠의 일격 (Q)" 스킬을 피하기 위해 지속적으로 움직이세요. 특히, 그의 세 번째 Q는 큰 피해를 주므로 피해야 합니다.
게임 중반 (Mid Game)
갱 회피:

카밀은 이동기가 뛰어나므로, 정글러의 갱을 회피할 수 있습니다. 적 정글러의 위치를 항상 인지하고 와드를 설치하여 갱을 방지하세요.
"갈고리 발사 (E)" 스킬을 이용해 갱에서 빠져나갈 수 있습니다.
스킬 콤보:

"정밀한 의도 (Q)" 두 번째 활성화와 "전술적 휩쓸기 (W)"를 활용하여 아트록스를 견제하세요.
"결단의 궁극기 (R)"로 아트록스를 고립시키고 팀원들이 합류할 수 있도록 하세요.
게임 후반 (Late Game)
팀 싸움:
카밀은 팀 싸움에서 적의 주요 딜러를 집중 타겟팅하는 데 능합니다. 아트록스가 아닌 상대방의 주요 딜러를 노려보세요.
아트록스가 무리하지 않도록 주의하고, 그의 스킬들이 빠졌을 때를 노려 공격하세요.
추가 팁
아이템 빌드:

"거대한 히드라"와 같은 체력 회복 아이템을 우선적으로 구입하여 라인 유지력을 높이세요.
"죽음의 무도"와 같은 아이템을 통해 생존력을 높일 수 있습니다.
소환사 주문:

"점멸"과 "순간이동"을 사용하여 맵 전반에서 기동성을 극대화하세요. 때에 따라 "유체화"도 고려해 볼 수 있습니다.
스킬 우선 순위
스킬 업그레이드:
Q 스킬을 우선적으로 강화하여 딜을 극대화하세요.
그 다음으로 E 스킬을 강화하여 이동성과 스턴 효과를 높이세요.
이 팁들을 활용하여 "카밀"로 "아트록스"를 상대할 때 유리한 위치를 선점하고 게임을 유리하게 이끌어 가길 바랍니다. 매 상황에 맞춰 유연하게 플레이하는 것도 중요합니다.`;

fetch("/routing/env", { method: "POST" })
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    apiKey = data.key;
  });

function askTips() {
  const my_champ = document.getElementById("me").innerText;
  const opp_champ = document.getElementById("opp").innerText;
  const line = document.getElementById("line").value;
  const tipbox = document.getElementById("tipbox");
  console.log(my_champ, opp_champ, line);
  const data = {
    model: "gpt-3.5-turbo",
    messages: [
      { role: "system", content: "너는 리그오브레전드에서 챔피언 1대1 매치업에서 나의 챔피언과 상대챔피언의 상성에 따른 플레이 팁을 알려주는 도우미야" },
      { role: "assistant", content: text },
      { role: "user", content: `리그오브레전드 게임에서, ${line} 포지션에서 내가 ${my_champ} 챔피언을 플레이하고 상대방이 ${opp_champ} 일때의 상대하는 팁을 알려줘` },
    ],
  };

  fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("Success:", data.choices[0].message.content);
      tipbox.innerText = data.choices[0].message.content;
    })
    .catch((error) => {
      console.error(error);
    });
}
