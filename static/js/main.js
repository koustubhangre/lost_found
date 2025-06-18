// main.js

// Example: AJAX submit for the report form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('report-form');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = new FormData(form);
        const resp = await fetch(form.action, {
          method: 'POST',
          body: data,
        });
        if (resp.redirected) {
          window.location.href = resp.url;
        } else {
          const text = await resp.text();
          console.error('Submission failed', text);
          alert('Failed to submit—see console.');
        }
      });
    }
  });
  