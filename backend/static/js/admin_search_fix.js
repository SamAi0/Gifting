(function() {
    function initSearchFix() {
        var searchbar = document.getElementById("searchbar");
        if (!searchbar) return;

        var searchButton = null;

        // 1. Try to find a primary button containing "search" on the page first
        searchButton = Array.from(document.querySelectorAll("button.btn-primary, button.btn-success, input.btn-primary"))
                            .find(el => {
                                var text = (el.textContent || el.value || "").trim().toLowerCase();
                                return text === "search" || text.includes("search");
                            });

        // 2. If not found, use a robust bubble-up logic, but exclude range filters
        if (!searchButton) {
            var parent = searchbar.parentElement;
            while (parent && !searchButton) {
                searchButton = Array.from(parent.querySelectorAll("button, input[type='button'], input[type='submit']"))
                                    .find(el => {
                                        var text = (el.textContent || el.value || "").trim().toLowerCase();
                                        if (text !== "search" && !text.includes("search")) return false;
                                        
                                        // Ignore buttons that are inside a range filter or other custom filter forms
                                        if (el.closest('.rangefilter') || el.closest('form:not(#changelist-search)')) {
                                            return false;
                                        }
                                        return true;
                                    });
                if (parent.tagName === "BODY" || parent.id === "content") {
                    break;
                }
                parent = parent.parentElement;
            }
        }

        function performSearch() {
            var query = searchbar.value.trim();
            var url = new URL(window.location.href);
            
            if (query) {
                url.searchParams.set("q", query);
            } else {
                url.searchParams.delete("q");
            }
            
            // Reset pagination to first page
            url.searchParams.delete("p");
            
            window.location.href = url.toString();
        }

        if (searchButton) {
            // Change type to 'button' to prevent any broken default form submission
            searchButton.type = "button";
            searchButton.addEventListener("click", function(e) {
                e.preventDefault();
                performSearch();
            });
        }
        
        searchbar.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                e.preventDefault();
                performSearch();
            }
        });
    }

    // Handle potential DOMContentLoaded race condition
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSearchFix);
    } else {
        initSearchFix();
    }
})();
