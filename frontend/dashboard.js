// ==========================================
// TELCO AI - DASHBOARD JAVASCRIPT
// ==========================================


// ==========================================
// CHECK LOGIN
// ==========================================

const loggedIn = sessionStorage.getItem("loggedIn");

if (loggedIn !== "true") {

    window.location.href = "index.html";

}


// ==========================================
// GET USERNAME
// ==========================================

const username =
    sessionStorage.getItem("username") || "Admin";


// ==========================================
// DISPLAY USERNAME
// ==========================================

const dashboardUsername =
    document.getElementById("dashboardUsername");

const welcomeUsername =
    document.getElementById("welcomeUsername");


if (dashboardUsername) {

    dashboardUsername.textContent = username;

}


if (welcomeUsername) {

    welcomeUsername.textContent = username;

}


// ==========================================
// LOGOUT
// ==========================================

const logoutButton =
    document.getElementById("logoutButton");


if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        async function (event) {

            event.preventDefault();

            try {

                await fetch(
                    "http://127.0.0.1:5000/logout",
                    {
                        method: "POST",
                        credentials: "include"
                    }
                );

            } catch (error) {

                console.log(
                    "Logout request error:",
                    error
                );

            }


            // Clear browser session

            sessionStorage.removeItem(
                "loggedIn"
            );

            sessionStorage.removeItem(
                "username"
            );


            // Go back to login

            window.location.href =
                "index.html";

        }
    );

}


// ==========================================
// CHURN DISTRIBUTION CHART
// ==========================================

const churnCanvas =
    document.getElementById("churnChart");


if (churnCanvas) {

    new Chart(
        churnCanvas,
        {

            type: "doughnut",

            data: {

                labels: [
                    "Retained",
                    "Churned"
                ],

                datasets: [

                    {

                        data: [
                            5174,
                            1869
                        ],

                        borderWidth: 0

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            padding: 20,

                            usePointStyle: true

                        }

                    }

                }

            }

        }
    );

}


// ==========================================
// CONTRACT CHART
// ==========================================

const contractCanvas =
    document.getElementById("contractChart");


if (contractCanvas) {

    new Chart(
        contractCanvas,
        {

            type: "bar",

            data: {

                labels: [
                    "Month-to-month",
                    "One year",
                    "Two year"
                ],

                datasets: [

                    {

                        label: "Customers",

                        data: [
                            3875,
                            1473,
                            1695
                        ],

                        borderWidth: 0

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        }
    );

}


// ==========================================
// INTERNET SERVICE CHART
// ==========================================

const internetCanvas =
    document.getElementById("internetChart");


if (internetCanvas) {

    new Chart(
        internetCanvas,
        {

            type: "pie",

            data: {

                labels: [
                    "DSL",
                    "Fiber optic",
                    "No internet"
                ],

                datasets: [

                    {

                        data: [
                            2421,
                            3096,
                            1526
                        ],

                        borderWidth: 0

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            padding: 15,

                            usePointStyle: true

                        }

                    }

                }

            }

        }
    );

}


// ==========================================
// PAYMENT METHOD CHART
// ==========================================

const paymentCanvas =
    document.getElementById("paymentChart");


if (paymentCanvas) {

    new Chart(
        paymentCanvas,
        {

            type: "bar",

            data: {

                labels: [

                    "Electronic check",

                    "Mailed check",

                    "Bank transfer",

                    "Credit card"

                ],

                datasets: [

                    {

                        label: "Customers",

                        data: [
                            2365,
                            1612,
                            1544,
                            1522
                        ],

                        borderWidth: 0

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        }
    );

}


// ==========================================
// DASHBOARD LOADED
// ==========================================

console.log(
    "Telco AI Dashboard loaded successfully!"
);