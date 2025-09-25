document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('accuracyForm');
    const errorMessageDiv = document.getElementById('errorMessage');
    const errorMessageText = document.getElementById('errorMessageText');
    const closeErrorBtn = document.getElementById('closeError');
    const resultsDiv = document.getElementById('results');
    const progressIndicator = document.getElementById('progressIndicator');
    const progressBar = document.querySelector('.progress-fill');
    const newComparisonBtn = document.getElementById('newComparison');
    const exportResultsBtn = document.getElementById('exportResults');
    const fullscreenButtons = document.querySelectorAll('.toggle-fullscreen');

    // Close error message
    if (closeErrorBtn) {
        closeErrorBtn.addEventListener('click', () => {
            errorMessageDiv.style.display = 'none';
        });
    }

    // New comparison
    if (newComparisonBtn) {
        newComparisonBtn.addEventListener('click', () => {
            resultsDiv.style.display = 'none';
            form.reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Export results
    if (exportResultsBtn) {
        exportResultsBtn.addEventListener('click', () => {
            alert('Export functionality would be implemented here. In a real application, this would generate a PDF or CSV report.');
        });
    }

    // Fullscreen toggle
    fullscreenButtons.forEach(button => {
        button.addEventListener('click', () => {
            const target = button.getAttribute('data-target');
            const content = target === 'source' ? 
                document.getElementById('highlightedSource') : 
                document.getElementById('highlightedTarget');
            
            if (!document.fullscreenElement) {
                if (content.requestFullscreen) {
                    content.requestFullscreen();
                } else if (content.webkitRequestFullscreen) {
                    content.webkitRequestFullscreen();
                } else if (content.msRequestFullscreen) {
                    content.msRequestFullscreen();
                }
                button.innerHTML = '<i class="fas fa-compress"></i>';
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
                button.innerHTML = '<i class="fas fa-expand"></i>';
            }
        });
    });

    // Form submission
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Form submitted');

            // Hide previous results and errors
            errorMessageDiv.style.display = 'none';
            resultsDiv.style.display = 'none';

            // Show progress indicator
            progressIndicator.style.display = 'block';
            progressBar.style.width = '30%';

            // Simulate progress
            const progressInterval = setInterval(() => {
                const currentWidth = parseInt(progressBar.style.width);
                if (currentWidth < 90) {
                    progressBar.style.width = (currentWidth + 10) + '%';
                }
            }, 300);

            const formData = new FormData(form);

            try {
                progressBar.style.width = '90%';
                
                const response = await fetch('/api/v1/accuracy', {
                    method: 'POST',
                    body: formData
                });

                clearInterval(progressInterval);
                progressBar.style.width = '100%';

                if (!response.ok) {
                    const errorText = await response.text();
                    if (response.status === 401) {
                        throw new Error('Authentication required. Please log in first.');
                    }
                    throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
                }

                const report = await response.json();
                console.log('Report received:', report);

                // Update summary stats
                document.getElementById('accuracy').textContent = report.accuracy ?? '0%';
                document.getElementById('errorsFound').textContent = report.errorsFound ?? '0';
                document.getElementById('sourceTotalWords').textContent = report.sourceTotalWords ?? '0';
                document.getElementById('targetTotalWords').textContent = report.targetTotalWords ?? '0';

                // Update detail stats
                document.getElementById('sourceTotalChars').textContent = report.sourceTotalChars ?? '0';
                document.getElementById('targetTotalChars').textContent = report.targetTotalChars ?? '0';
                document.getElementById('sourceWhitespaceCount').textContent = report.sourceWhitespaceCount ?? '0';
                document.getElementById('targetWhitespaceCount').textContent = report.targetWhitespaceCount ?? '0';

                // Update document content
                const highlightedSourceDiv = document.getElementById('highlightedSource');
                const highlightedTargetDiv = document.getElementById('highlightedTarget');
                
                highlightedSourceDiv.innerHTML = report.highlightedSourceHtml && report.highlightedSourceHtml.trim() !== ''
                    ? report.highlightedSourceHtml
                    : '<em>No source content available.</em>';
                highlightedTargetDiv.innerHTML = report.highlightedTargetHtml && report.highlightedTargetHtml.trim() !== ''
                    ? report.highlightedTargetHtml
                    : '<em>No target content available.</em>';

                // Update categorized errors
                const categorizedErrorsList = document.getElementById('categorizedErrorsList');
                categorizedErrorsList.innerHTML = ''; // Clear previous errors
                
                if (report.categorizedErrors && report.categorizedErrors.length > 0) {
                    // Create error distribution data for chart
                    const errorTypes = {};
                    report.categorizedErrors.forEach(error => {
                        errorTypes[error.errorType] = (errorTypes[error.errorType] || 0) + 1;
                    });

                    // Create chart
                    createErrorChart(errorTypes);

                    // Display errors
                    report.categorizedErrors.forEach(error => {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'error-item';
                        
                        let iconClass = 'fa-exclamation-circle';
                        let errorColor = '#dc2626';
                        
                        if (error.errorType === 'Whitespace Error') {
                            iconClass = 'fa-text-width';
                            errorColor = '#f59e0b';
                        } else if (error.errorType === 'Punctuation Error') {
                            iconClass = 'fa-pen';
                            errorColor = '#8b5cf6';
                        } else if (error.errorType === 'Missing Text') {
                            iconClass = 'fa-minus-circle';
                            errorColor = '#ef4444';
                        } else if (error.errorType === 'Extra Text') {
                            iconClass = 'fa-plus-circle';
                            errorColor = '#3b82f6';
                        }
                        
                        errorDiv.innerHTML = `
                            <h4 style="color: ${errorColor};">
                                <i class="fas ${iconClass}"></i> 
                                Error #${error.errorNumber}: ${error.errorType}
                            </h4>
                            <div class="error-details">
                                <p><strong>Source:</strong> ${error.inSource}</p>
                                <p><strong>Target:</strong> ${error.inTarget}</p>
                            </div>
                        `;
                        categorizedErrorsList.appendChild(errorDiv);
                    });
                    
                    document.getElementById('categorizedErrors').style.display = 'block';
                } else {
                    document.getElementById('categorizedErrors').style.display = 'none';
                }

                // Hide progress and show results
                setTimeout(() => {
                    progressIndicator.style.display = 'none';
                    resultsDiv.style.display = 'block';
                    
                    // Scroll to results
                    resultsDiv.scrollIntoView({ behavior: 'smooth' });
                }, 500);

            } catch (error) {
                console.error('Error:', error);
                clearInterval(progressInterval);
                progressIndicator.style.display = 'none';
                
                errorMessageText.textContent = `Error: ${error.message || 'An unexpected error occurred.'}`;
                errorMessageDiv.style.display = 'block';
            }
        });
    }

    // Create error distribution chart
    function createErrorChart(errorTypes) {
        const ctx = document.getElementById('errorChart');
        if (!ctx) return;

        // Destroy existing chart if it exists and is a Chart instance
        if (window.errorChart && typeof window.errorChart.destroy === 'function') {
            window.errorChart.destroy();
        }

        // Prepare data
        const labels = Object.keys(errorTypes);
        const data = Object.values(errorTypes);
        
        // Color palette for different error types
        const backgroundColors = [
            '#ef4444', // red for Missing Text
            '#3b82f6', // blue for Extra Text
            '#f59e0b', // amber for Whitespace Error
            '#8b5cf6', // violet for Punctuation Error
            '#10b981', // green
            '#f97316', // orange
            '#ec4899'  // pink
        ];

        // Create chart
        window.errorChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
});