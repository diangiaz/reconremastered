      function enableRQty(arg){
        var rtr = document.getElementById("routerBox");
        var rtrQty = document.getElementById("routerQty");

        if (rtr.checked == true){
          rtrQty.disabled = false;
        }
        else{
          rtrQty.disabled = true;
          rtrQty.value = 0;
        }
      }

      function enableSWQty(arg){  
        var sw = document.getElementById("switchBox");
        var swQty = document.getElementById("switchQty");

        if (sw.checked == true){
          swQty.disabled = false;
        }
        else{
          swQty.disabled = true;
          swQty.value = 0;
        }
      }

      function enableSRQty(arg){
        var server = document.getElementById("serverBox");
        var svrQty = document.getElementById("serverQty");

        if (server.checked == true){
          svrQty.disabled = false;
        }
        else{
          svrQty.disabled = true;
          svrQty.value = 0;
        }
      }

      function enableTQty(arg){
        var terminal = document.getElementById("terminalBox");
        var terQty = document.getElementById("terminalQty");
        
        if (terminal.checked == true){
          terQty.disabled = false;
        }
        else{
          terQty.disabled = true;
          terQty.value = 0;
        }
      }