const API_URL = "http://127.0.0.1:8000";


// REGISTER


const registerForm = document.getElementById("registerForm");


if (registerForm) {

    registerForm.addEventListener("submit", async function(event) {

        event.preventDefault();


        const username =
            document.getElementById("registerUsername").value;

        const email =
            document.getElementById("registerEmail").value;

        const password =
            document.getElementById("registerPassword").value;

        const role =
            document.getElementById("registerRole").value;

        const message =
            document.getElementById("registerMessage");


        const userData = {

            username: username,

            email: email,

            password: password,

            role: role

        };


        try {

            const response = await fetch(
                `${API_URL}/auth/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(userData)
                }
            );


            const data = await response.json();


            if (!response.ok) {

                message.textContent =
                    data.detail || "Registration failed.";

                message.style.color = "red";

                return;
            }


            message.textContent =
                "Account created successfully!";

            message.style.color = "green";


            registerForm.reset();


            setTimeout(() => {

                window.location.href = "index.html";

            }, 1500);


        } catch (error) {

            console.error(error);

            message.textContent =
                "Could not connect to the server.";

            message.style.color = "red";

        }

    });

}



// LOGIN


const loginForm = document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener("submit", async function(event) {

        event.preventDefault();


        const username =
            document.getElementById("loginUsername").value;

        const password =
            document.getElementById("loginPassword").value;

        const role =
            document.getElementById("loginRole").value;

        const message =
            document.getElementById("loginMessage");


        const loginData = {

            username: username,

            password: password,

            role: role

        };


        try {

            const response = await fetch(
                `${API_URL}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(loginData)
                }
            );


            const data = await response.json();


            if (!response.ok) {

                message.textContent =
                    data.detail || "Invalid username or password.";

                message.style.color = "red";

                return;
            }


            message.textContent =
                "Login successful!";

            message.style.color = "green";


            // Save logged-in user
            localStorage.setItem(
                "user",
                JSON.stringify(data)
            );

            window.location.href = "dashboard.html";


            console.log("Logged in:", data);


            setTimeout(() => {

                if (data.role === "Blogger") {

                    alert("Welcome Blogger!");

                } else if (data.role === "Guest") {

                    alert("Welcome Guest!");

                } else if (data.role === "ADMIN") {

                    alert("Welcome Admin!");

                }

            }, 700);


        } catch (error) {

            console.error(error);

            message.textContent =
                "Could not connect to the server.";

            message.style.color = "red";

        }

    });

}

