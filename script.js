document.getElementById('fileInput').addEventListener('change', function() {
    const fileName = this.files[0].name;
    document.getElementById('fileName').textContent = `Selected file: ${fileName}`;
    document.getElementById('outputbox').style.display = 'none';

    document.getElementById('progressBar').style.width = 0 + '%';
                document.getElementById('progressText').textContent = 0 + '%';
    document.getElementById('languageSelectWrapper').style.display= 'none'
    document.getElementById('unselectButton').style.display = 'inline-block';
    document.getElementById('belowpart').style.display = 'inline-block';
    document.getElementById('belowpart').classList.add('visible');



    
});

document.getElementById('unselectButton').addEventListener('click', function() {
    document.getElementById('fileInput').value = '';
    document.getElementById('fileName').textContent = '';
    this.style.display = 'none';
    document.getElementById('belowpart').style.display = 'none';
    document.getElementById('belowpart').classList.add('hidden');
});

document.getElementById('featureSelect').addEventListener('change', function() {
    const selectedFeature = this.value;
    const languageSelectWrapper = document.getElementById('languageSelectWrapper');
    
    if (selectedFeature === 'transcribe') {
        languageSelectWrapper.style.display = 'block';
    } else {
        languageSelectWrapper.style.display = 'none';
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const feature = document.getElementById('featureSelect').value;
    const language = document.getElementById('languageSelect').value;

    if (file) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://127.0.0.1:5000/api/audioAI', true);
        percentage = 0
        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                percentage = percentComplete
                document.getElementById('progressBar').style.width = percentComplete + '%';
                document.getElementById('progressText').textContent = Math.round(percentComplete) + '%';
                if(Math.round(percentComplete) == 100){
                    document.getElementById('Main').style.display = 'none';
                    document.getElementById('loader').style.display = 'inline';
                    document.getElementById('loader').style.zIndex = 3;
                }
            }
        };
      
        
        
        xhr.onload = function() {

            document.getElementById('belowpart').style.display = 'none';
            document.getElementById('belowpart').classList.add('hidden');
            response_data = JSON.parse(xhr.response)

            if (xhr.status === 200 && response_data.status == 'success') {
                console.log(xhr.response)
                document.getElementById('outputbox').style.display = 'inline';
                document.getElementById('outputbox').innerHTML = '<p>'+ response_data.text +'</p>';
                document.getElementById('uploadForm').reset();
                document.getElementById('loader').style.display = 'none';
                document.getElementById('Main').style.display = 'inline';
                swal.fire('Great',response_data.message,'success')
            } else {
                swal.fire('Opps!',response_data.message,'error')
                document.getElementById('loader').style.display = 'none';
                document.getElementById('uploadForm').reset();
                document.getElementById('outputbox').style.display = 'none';
                document.getElementById('Main').style.display = 'inline';

            }
        };

        const formData = new FormData();
        formData.append('file', file);
        formData.append('feature', feature);
        if (feature === 'transcribe') {
            formData.append('language', language);
        }
        xhr.send(formData);
    } else {
        alert('Please select a file to upload.');
    }
});
