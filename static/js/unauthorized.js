champimgs = document.getElementsByClassName("champ_detail");
      for (let i = 0; i < champimgs.length; i++) {
          champimgs[i].addEventListener("click", function() {
              // Ajax 요청을 보냄
              let xhr = new XMLHttpRequest();
              let url = champimgs[i].dataset.champname;
              xhr.open("GET", "/routing/champion/" + url, true);
              console.log('flag1')
              xhr.onreadystatechange = function() {
                  if (xhr.readyState == 4 && xhr.status == 200) {
                      // 서버로부터 받은 응답을 확인하고 팝업 창을 띄움
                      console.log("flag2")
                      let response = JSON.parse(xhr.responseText);
                      alert(response.message);
                  }
              };
              xhr.send();
              xhr.open("GET", "routing/login_page");
              xhr.send();
          })
      }