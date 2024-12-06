document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".btn-minus").forEach(button => {
        button.addEventListener("click", function () {
            const href = this.getAttribute("data-href");
            if (href) {
                window.location.href = href;
                }
            });
        });
    });
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-plus").forEach(button => {
        button.addEventListener("click", function () {

            const href = this.getAttribute("data-href");
            if (href) {
                window.location.href = href;
                }
            });
        });
    });