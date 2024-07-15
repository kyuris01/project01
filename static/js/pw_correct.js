const warning = document.getElementById("warning_box");

fetch('/routing/env', {method:'POST'})
  .then((res)=>{ 
    return res.json();
  })
  .then((data) => {
    apiKey = data.key;
  })
