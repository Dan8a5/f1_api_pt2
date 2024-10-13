document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const responseMessage = document.getElementById('responseMessage');
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        const formProps = Object.fromEntries(formData);

        if (!validateForm(formProps)) {
            showResponse('Error: All fields are required.', 'error');
            return;
        }

        try {
            setLoading(true);
            const res = await fetch('http://localhost:8000/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formProps),
            });

            if (res.ok) {
                showResponse('Success: Your message has been sent!', 'success');
                form.reset();
            } else {
                const errorData = await res.json();
                showResponse(`Error: ${errorData.detail || 'There was an issue sending your message.'}`, 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showResponse('Error: Something went wrong!', 'error');
        } finally {
            setLoading(false);
        }
    });

    function validateForm(formProps) {
        return Object.values(formProps).every(value => value.trim() !== '');
    }

    function showResponse(message, type) {
        responseMessage.innerHTML = `<strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> ${message}`;
        responseMessage.className = type;
        responseMessage.style.display = 'block';
    }

    function setLoading(isLoading) {
        submitButton.disabled = isLoading;
        submitButton.textContent = isLoading ? 'Sending...' : 'Send';
    }
});