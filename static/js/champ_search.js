let champ_search_input = document.getElementById("champ-search-input");
const champ_search_button = document.getElementById("champ-search-button");
let name_dict;

fetch("/routing/translate", { method: "GET" })
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    name_dict = data;
  });
//console.log(name_dict);

champ_search_button.addEventListener("click", () => {
  if (champ_search_input === "") {
    alert("챔피언의 이름을 적거나 선택하세요!");
  } else {
    const champ_kor_name = champ_search_input.value;
    const champ_eng_name = name_dict[champ_kor_name];
    window.location.href = `http://localhost:5000/routing/champion/${champ_eng_name}`;
  }
});
