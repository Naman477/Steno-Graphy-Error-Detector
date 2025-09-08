document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('accuracyForm');
    const errorMessageDiv = document.getElementById('errorMessage');
    const resultsDiv = document.getElementById('results');
    const sourceTotalCharsSpan = document.getElementById('sourceTotalChars');
    const errorsFoundSpan = document.getElementById('errorsFound');
    const accuracySpan = document.getElementById('accuracy');
    const differencesList = document.getElementById('differencesList');
    const highlightedSourceDiv = document.getElementById('highlightedSource');
    const highlightedTargetDiv = document.getElementById('highlightedTarget');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        errorMessageDiv.style.display = 'none';
        resultsDiv.style.display = 'none';

        const formData = new FormData(form);

        try {
            const response = await fetch('/api/v1/accuracy', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const report = await response.json();

            sourceTotalCharsSpan.textContent = report.sourceTotalChars;
            errorsFoundSpan.textContent = report.errorsFound;
            accuracySpan.textContent = report.accuracy;

            differencesList.innerHTML = ''; // Clear previous differences
            if (report.differences && report.differences.length > 0) {
                report.differences.forEach(diff => {
                    const li = document.createElement('li');
                    li.textContent = diff;
                    differencesList.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = 'No significant differences found.';
                differencesList.appendChild(li);
            }

            highlightedSourceDiv.innerHTML = report.highlightedSourceHtml;
            highlightedTargetDiv.innerHTML = report.highlightedTargetHtml;

            resultsDiv.style.display = 'block';

        } catch (error) {
            console.error('Error:', error);
            errorMessageDiv.querySelector('p').textContent = `Error: ${error.message || 'An unexpected error occurred.'}`;
            errorMessageDiv.style.display = 'block';
        }
    });
});