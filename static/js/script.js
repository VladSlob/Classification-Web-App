function handleShowImagePreview() {
    const imageInput = document.getElementById("imageInput");
    const imagePreview = document.getElementsByClassName("image-preview")[0];
    const labelText = document.getElementsByClassName("image-loading-label_text")[0];

    function previewImage(event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                imagePreview.src = e.target.result;

                labelText.classList.add("hidden");

                imagePreview.classList.remove("hidden");
            };

            reader.readAsDataURL(file);
        }
    }

    imageInput.addEventListener("change", previewImage);

    function cleanup() {
        imageInput.removeEventListener("change", previewImage);
    }

    window.addEventListener("beforeunload", cleanup);
}

document.addEventListener("DOMContentLoaded", handleShowImagePreview);
