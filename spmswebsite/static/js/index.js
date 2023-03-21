     const progress = document.querySelector(".progress-done");
     const input = document.querySelector(".input");
     const maxInput = document.querySelector(".maxInput");
     let finalvalue = 0;
     let max = 0;
    
     function changeWidth(){
         progress.style.width = '${(finalvalue / max) * 100}%';
         progress.innerText = '${Math.ceil((finalvalue / max) * 100)}%';
     }
    
     input.addEventListener("keyup", function (){
       finalvalue = parseInt(input.value,10);
       changeWidth();
     });

     maxInput.addEventListener("keyup", function (){
         max = parseInt(maxInput.value,10);
         changeWidth();
     });