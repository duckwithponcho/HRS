(function () {
    // Add an initial history entry
    history.pushState(null, "", location.href);

    // Detect Back or Forward navigation
    window.addEventListener("popstate", function () {
        // Reload the current page
        window.location.reload();
    });
})();

