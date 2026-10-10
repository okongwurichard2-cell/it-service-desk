document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("helpdeskSidebar");
    const overlay = document.getElementById("helpdeskOverlay");
    const menuToggle = document.getElementById("helpdeskMenuToggle");


    function closeSidebar() {

        if (!sidebar || !overlay || !menuToggle) {
            return;
        }

        sidebar.classList.remove("open");
        overlay.classList.remove("active");
        menuToggle.setAttribute("aria-expanded", "false");
    }


    if (menuToggle && sidebar && overlay) {

        menuToggle.addEventListener("click", function () {

            const isOpen = sidebar.classList.toggle("open");

            overlay.classList.toggle(
                "active",
                isOpen
            );

            menuToggle.setAttribute(
                "aria-expanded",
                String(isOpen)
            );

        });


        overlay.addEventListener(
            "click",
            closeSidebar
        );

    }


    document.querySelectorAll(".helpdesk-message-close").forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const message =
                        button.closest(".helpdesk-message");

                    if (message) {
                        message.remove();
                    }

                }
            );

        }
    );


    document.querySelectorAll(".helpdesk-message").forEach(
        function (message) {

            setTimeout(
                function () {

                    if (message.isConnected) {
                        message.remove();
                    }

                },
                5000
            );

        }
    );

});