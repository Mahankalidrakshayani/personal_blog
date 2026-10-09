/**
 * Main JavaScript for My Personal Blog Website
 * Handles interactivity: alerts auto-dismiss, file upload preview,
 * reading progress bar, share buttons, and dynamic counters.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // 2. Image preview for file inputs (Post form & Profile Avatar)
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"], input[name="featured_image"], input[name="avatar"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const previewContainer = document.getElementById(input.name + '-preview') || document.getElementById('image-preview');
            if (previewContainer) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    previewContainer.innerHTML = `<img src="${event.target.result}" alt="Preview" class="img-fluid rounded" style="max-height: 260px; width: 100%; object-fit: cover;">`;
                    previewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // 3. Reading progress bar on blog detail page
    const readingBar = document.getElementById('reading-progress');
    const article = document.querySelector('.post-article-content');
    if (readingBar && article) {
        window.addEventListener('scroll', () => {
            const articleRect = article.getBoundingClientRect();
            const articleTop = articleRect.top + window.scrollY;
            const articleHeight = article.offsetHeight;
            const windowHeight = window.innerHeight;
            const scrollTop = window.scrollY;

            if (scrollTop >= articleTop) {
                const progress = Math.min(
                    100,
                    Math.max(0, ((scrollTop - articleTop) / (articleHeight - windowHeight + 200)) * 100)
                );
                readingBar.style.width = `${progress}%`;
            } else {
                readingBar.style.width = '0%';
            }
        });
    }

    // 4. Copy share link to clipboard
    const copyLinkBtn = document.getElementById('copy-share-link');
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', (e) => {
            e.preventDefault();
            navigator.clipboard.writeText(window.location.href).then(() => {
                const originalHtml = copyLinkBtn.innerHTML;
                copyLinkBtn.innerHTML = '<i class="bi bi-check2"></i> Copied!';
                copyLinkBtn.classList.add('btn-success');
                setTimeout(() => {
                    copyLinkBtn.innerHTML = originalHtml;
                    copyLinkBtn.classList.remove('btn-success');
                }, 2500);
            }).catch(err => {
                console.error('Failed to copy link', err);
            });
        });
    }

    // 5. Comment character counter
    const commentInput = document.querySelector('textarea[name="content"]');
    const charCounter = document.getElementById('comment-char-counter');
    if (commentInput && charCounter) {
        const updateCounter = () => {
            const remaining = 1000 - commentInput.value.length;
            charCounter.textContent = `${commentInput.value.length}/1000 characters`;
        };
        commentInput.addEventListener('input', updateCounter);
        updateCounter();
    }
});
