
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

//     var loader_script = '<div id="pre-loader">' +
//     '<div class="spinner-border text-primary" role="status">' +
//     '<span class="sr-only">Loading...</span>' +
//     '</div>' +
//     '</div>';
// window.start_loader = function() {
//     if ($('body>#pre-loader').length <= 0) {
//         $('body').append(loader_script)
//     }
// }
// window.end_loader = function() {
//     var loader = $('body>#pre-loader')
//     if (loader.length > 0) {
//         loader.remove()
//     }
// }
    