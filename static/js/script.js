document.addEventListener('DOMContentLoaded', function() {

const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const fileNames = document.getElementById('fileNames');
const runQc = document.getElementById('run-qc');
const runAuthor = document.getElementById('run-author');
const emptyFiles = document.getElementById('empty-file');
const url = 'http://127.0.0.1:5000';

var files = '';
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('highlight');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('highlight');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('highlight');
    const files = e.dataTransfer.files;
    handleFiles(files);
});

fileInput.addEventListener('change', () => {
    files = fileInput.files;
    handleFiles(files);
});
uploadBtn.addEventListener('click',()=>{
    fileInput.click();
})
emptyFiles.addEventListener('click',()=>{
    files='';
    fileNames.innerHTML = "";
    console.log(files.length)
})


runQc.addEventListener('click',async ()=>{
    const formData = new FormData();
    console.log('files are',files)
    formData.append('file', files[0]);
    fetch(`${url}/runQcScript`, {
        method: 'POST',
        body: formData
    }).then(response=> response.json())
    .then(data=>{
        console.log(data)
        // var data = JSON.stringify(data, null, 2);    
        document.getElementById('qc-comments').value = data.qcComments.replace(/\\n/g, '\n');
        document.getElementById('qc-comments').style.height = "300px";
        document.getElementById('sponsors').value = data.sponsorInfo.replace(/\\n/g, '\n');
        document.getElementById('sponsors').style.height = "300px";
    })    
});

runAuthor.addEventListener('click',async ()=>{
    const formData = new FormData();
    console.log('files are',files)
    formData.append('file', files[0]);
    if(files.length<1){
        alert('please add a file');
        return;
    }
    fetch(`${url}/runAuthor`, {
        method: 'POST',
        body: formData
    }).then(response => response.blob()) // Convert the response to a Blob
    .then(blob => {
        // Create a link element
        var link = document.createElement('a');
        // Set the href attribute to a URL created from the Blob
        link.href = URL.createObjectURL(blob);
        // Set the download attribute with the desired file name
        link.download = 'final.xlsx';
        // Append the link to the document body
        document.body.appendChild(link);
        // Trigger a click event on the link to initiate the download
        link.click();
        // Remove the link from the document
        document.body.removeChild(link);
    }).catch(error => console.error('Error:', error));
});
    

function handleFiles(files) {
    if (files.length>1){
        alert("Please upload 1 file at a time")
    }
    if (files.length > 0) {
        const file = files[0];
        fileNames.innerHTML = "";
        fileNames.appendChild(document.createElement("li").appendChild(document.createTextNode(`File Name:- ${file.name}`)));
        console.log(files);
    }
}

}); 