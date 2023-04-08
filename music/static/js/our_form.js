var inputImageButton = document.querySelector("#input-image-button");
var inputImage = document.querySelector('#id_image');

inputImageButton.addEventListener('click', () => {
    inputImage.click();
});

inputImage.addEventListener('change', () => {
    const file = inputImage.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        inputImageButton.innerHTML = `<img src="${event.target.result}" height="300px" width="300px">`;
        inputImageButton.style.padding = '0px'
       
    };
    reader.readAsDataURL(file);
});

document.querySelector('#title-input').addEventListener('input', () => {
    document.querySelector('#id_title').value= document.querySelector('#title-input').value
})