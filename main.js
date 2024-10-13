// Log a message when the script is loaded
console.log('Script loaded');

// Ensure the DOM content is fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded');
    
    // Get references to the required HTML elements
    const askButton = document.getElementById('askButton'); // Button to trigger API call
    const questionInput = document.getElementById('question'); // Input field where users type their question
    const responseElement = document.getElementById('response'); // Div element to display the API response

    // Check if the necessary elements exist in the DOM
    if (!askButton || !questionInput || !responseElement) {
        console.error('One or more required elements not found');
        return; // Exit if any element is missing to prevent errors
    }

    // Add a click event listener to the "Ask Away" button
    askButton.addEventListener('click', async () => {
        console.log('Ask button clicked');
        
        // Get the user's question from the input field and trim whitespace
        const userQuestion = questionInput.value.trim();
        console.log('User question:', userQuestion);

        // Validate: If the user input is empty, show a message and stop further processing
        if (!userQuestion) {
            responseElement.textContent = 'Please enter a question.'; // Show an error message
            responseElement.style.display = 'block'; // Ensure the response element is visible
            return; // Stop the function if no question is provided
        }

        // Disable the ask button and show a loading state while waiting for the API response
        askButton.disabled = true; // Prevent multiple clicks during the API request
        askButton.classList.add('loading'); // Add a CSS class to indicate loading (change button appearance)
        askButton.textContent = "Loading..."; // Update the button text to show it's processing
        responseElement.style.display = 'none'; // Hide the response area until a new response is ready
        
        try {
            // Construct the API URL using the user's question (encoded to be URL safe)
            const url = `http://localhost:8000/ask/${encodeURIComponent(userQuestion)}`;
            console.log('Sending request to API:', url);
            
            // Send a GET request to the API using the Fetch API
            const response = await fetch(url, {
                method: 'GET', // HTTP method
                headers: {
                    'Content-Type': 'application/json' // Tells the server we're expecting JSON data
                },
                credentials: 'include' // If credentials (like cookies) are needed, include them
            });

            // Log the response status and headers for debugging purposes
            console.log('Response received. Status:', response.status);
            console.log('Response headers:', Object.fromEntries(response.headers.entries()));

            // Check if the API response was successful
            if (!response.ok) {
                // If not successful, log and throw an error with the status and message
                const errorText = await response.text(); // Get the error message from the response
                console.error('Error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            // Parse the JSON response from the API
            const data = await response.json();
            console.log('Full API Response:', data);

            // Display the response in the response element (API response or error message)
            responseElement.textContent = data.response || data.message || 'No response available.';
            responseElement.style.display = 'block'; // Make the response element visible
        } catch (error) {
            // Handle any errors that occurred during the API call
            console.error('Error details:', error); // Log the error for debugging
            responseElement.textContent = `An error occurred: ${error.message}`; // Show an error message to the user
            responseElement.style.display = 'block'; // Make sure the error message is visible
        } finally {
            // Re-enable the ask button and reset the text once the request is complete
            askButton.disabled = false; // Enable the button for future clicks
            askButton.classList.remove('loading'); // Remove the loading CSS class
            askButton.textContent = "Ask Away"; // Reset the button text to its original state
        }
    });
});