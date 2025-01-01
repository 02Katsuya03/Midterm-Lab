document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".role-button");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            // Remove the 'active' class from all buttons
            buttons.forEach(btn => btn.classList.remove("active"));
            
            // Add the 'active' class to the clicked button
            this.classList.add("active");
        });
    });
});