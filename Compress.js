function setup() {
    document.getElementById('buttonid').addEventListener('click', openDialog);
    
    document.getElementById('fileid').addEventListener('change', displayImage);

    document.getElementById('submitid').addEventListener('click', submitForm);
    
}

function openDialog() {
    
    document.getElementById('fileid').click();
    
}

function displayImage() {
    const fileContents = document.getElementById('fileid');
    console.log(fileContents.files[0].arrayBuffer());

    var reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('uploaded_image_id').src = e.target.result;
    }
    reader.readAsDataURL(fileContents.files[0]);
    document.getElementById('uploaded_image_id').alt=fileContents.files[0].name;
    document.getElementById('uploaded_image_id').hidden = false;
}

function submitForm() {
    console.log(document.getElementById('uploaded_image_id').src);
}