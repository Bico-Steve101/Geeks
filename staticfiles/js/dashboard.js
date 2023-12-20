// dashboard.js

document.addEventListener("DOMContentLoaded", async function () {
    // Example 1: Fetch data asynchronously
    try {
        const response = await fetch("/api/data"); // Replace with your API endpoint
        const data = await response.json();
        console.log("Fetched data:", data);
        // Perform actions with the fetched data, e.g., update the UI
    } catch (error) {
        console.error("Error fetching data:", error);
    }
 // Additional feature: Click event listener for cards in Recent Projects and Upcoming Hackathons sections
    const projectCards = document.querySelectorAll('.recent-projects-section .card');
    const hackathonCards = document.querySelectorAll('.upcoming-hackathons-section .card');

    projectCards.forEach(function (card) {
        card.addEventListener('click', function () {
            const projectName = this.querySelector('.card-title').innerText;
            alert(`Clicked on project: ${projectName}`);
        });
    });

    hackathonCards.forEach(function (card) {
        card.addEventListener('click', function () {
            const hackathonName = this.querySelector('.card-title').innerText;
            alert(`Clicked on hackathon: ${hackathonName}`);
        });
    });

    // Additional feature: Simple animation for the graph section
    const graphSection = document.querySelector('.graph-section');

    if (graphSection) {
        graphSection.addEventListener('mouseenter', function () {
            this.style.transform = 'scale(1.05)';
        });

        graphSection.addEventListener('mouseleave', function () {
            this.style.transform = 'scale(1)';
        });
    }
    // Example 2: Update content dynamically
    const dynamicContentElement = document.getElementById("dynamicContent");
    if (dynamicContentElement) {
        dynamicContentElement.innerHTML = "Updated dynamically!";
    }

    // Example 3: Handle user interaction (button click)
    const myButton = document.getElementById("myButton");
    if (myButton) {
        myButton.addEventListener("click", function () {
            alert("Button clicked!");
            // Perform additional actions on button click
        });
    }

    // Example 4: Custom Function with logic
    function myCustomFunction() {
        // Your custom function logic here
        console.log("Custom function executed!");
    }

    // Call your custom functions or examples as needed
    myCustomFunction();

    // Example 5: Function to toggle a class on an element
    function toggleClass(elementId, className) {
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.toggle(className);
        }
    }

    // Example 6: Advanced Animation Function
    function animateElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.transition = "transform 0.5s ease-in-out";
            element.style.transform = "rotate(360deg)";
        }
    }
});