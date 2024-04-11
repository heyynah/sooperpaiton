const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const resolvedView = document.getElementById("resolved-img-view");
const cancelButton = document.getElementById("cancel-button");
const submitButton = document.getElementById("submit-button");

inputFile.addEventListener("change", uploadImage);
cancelButton.addEventListener("click", cancelUpload);
submitButton.addEventListener("click", submitImage);

function uploadImage() {
    console.log('Uploading image...');
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
    imageView.style.border = 0;
    console.log('Image uploaded.');
}

function cancelUpload() {
    console.log('Cancelling upload...');
    console.log('imageView:', imageView); // Check if imageView is selecting the correct element
    if (imageView.style.backgroundImage === 'none') {
        alert("There is no uploaded image to cancel.");
    } else {
        imageView.style.backgroundImage = 'none';
        resolvedView.style.backgroundImage = 'none';
        
        // Retrieve the image path from the data attribute
        var imagePath = cancelButton.dataset.imagePath;
        
        // Create and set the image source
        var img = document.createElement('img');
        img.src = imagePath;
        
        // Clear existing content
        imageView.innerHTML = '';
        
        // Append the image and other elements
        imageView.appendChild(img);
        var p = document.createElement('p');
        p.innerHTML = "Drag and drop or click here<br> to upload image";
        imageView.appendChild(p);
        var span = document.createElement('span');
        span.textContent = "Upload any images from desktop";
        imageView.appendChild(span);
        imageView.style.border = "2px dashed #bbb5ff";
        console.log('Upload cancelled.');
    }
}

function submitImage() {
    console.log('Submitting image...');
    if (imageView.style.backgroundImage === 'none') {
        alert("There's no uploaded image to submit.");
    } else {
        const imgData = inputFile.files[0];
        
        const formData = new FormData();
        formData.append('image', imgData);

        const serverUrl = window.location.origin; // Get the server URL

        console.log('Sending image to server...');
        fetch(`${serverUrl}/process_image`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const processedImageUrl = `${serverUrl}/processed_images/${inputFile.files[0].name.replace('.png', '')}_rlt.png`; // Construct URL for processed image
            resolvedView.style.backgroundImage = `url(${processedImageUrl})`;
            resolvedView.style.border = "2px solid #bbb5ff";
            console.log('Image processed and displayed.');
        })
        .catch(error => console.error('Error:', error));
    }
}

dropArea.addEventListener("dragover", function (e) {
    e.preventDefault();
});

dropArea.addEventListener("drop", function (e) {
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    console.log('Image dropped into drop area.');
    uploadImage();
});

window.onload = function () {
    console.log('Window loaded.');
    if (!inputFile.files.length) {
        cancelUpload();
    }
};