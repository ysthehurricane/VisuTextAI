document.getElementById('image-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const text_prompt = document.getElementById('fn__include_textarea').value;
    const negative_prompt = document.getElementById('fn__exclude_textarea').value;

    const generateButton = e.target.querySelector('button[type="submit"]');
    const loader = document.getElementById('loader');

    // Show loader and disable button
    loader.innerText = "Wait for 2-3 minutes...";
    loader.style.display = 'block';
    generateButton.disabled = true;

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "text_prompt": text_prompt, "negative_prompt": negative_prompt })
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('prompt_title').innerText = data.text_prompt;
            document.getElementById('negative_prompt_title').innerText = "Negative prompt: " + data.negative_prompt;

            const generatedImageContainer = document.getElementById('fn__generation_list');
            generatedImageContainer.innerHTML = ''; // Clear the list before appending new items

            data.image_urls.forEach((url, index) => {
                if (url) {
                    const htmlContent = `
                        <li class="fn__gl_item">
                            <div class="fn__gl__item">
                                <div class="abs_item">
                                    <img src="${url}" alt="Generated Image ${index + 1}" class="fn__svg">
                                    
                                    <div class="all_options">
                                        <div class="fn__icon_options medium_size">
                                            <a href="${url}" class="fn__icon_button" download>
                                                <img src="/static/svg/download.svg" alt="Download Icon" class="fn__svg">
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                    `;

                    generatedImageContainer.insertAdjacentHTML('beforeend', htmlContent);
                } 
            });

            document.getElementById('fn__include_textarea').value = "";
            document.getElementById('fn__exclude_textarea').value = "";
        } else {
            alert('Error generating images. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred. Please try again.');
    } finally {
        // Hide loader and enable button
        loader.style.display = 'none';
        generateButton.disabled = false;
    }
});

