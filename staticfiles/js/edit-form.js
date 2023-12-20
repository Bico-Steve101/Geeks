const imageUpload = document.getElementById('id_avatar');
const imagePreview = document.getElementById('imagePreview');

imageUpload.addEventListener('change', function() {
  const file = this.files[0];

  if (file) {
    const isValidFileType = ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml'].includes(file.type);

    if (isValidFileType) {
      const reader = new FileReader();

      reader.onload = function(event) {
        imagePreview.src = event.target.result;
        imagePreview.style.display = 'block';
      };

      reader.readAsDataURL(file);
    } else {
      alert('Please select a valid image file (JPEG, PNG, GIF, SVG).');
      this.value = ''; // Clear the input to reset and prevent submission
    }
  }
});
