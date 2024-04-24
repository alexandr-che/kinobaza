document.addEventListener('DOMContentLoaded', function() {
    var collapseElements = document.querySelectorAll('.collapse');
    collapseElements.forEach(function(collapse) {
        collapse.addEventListener('show.bs.collapse', function() {
            collapseElements.forEach(function(otherCollapse) {
                if (otherCollapse !== collapse && otherCollapse.classList.contains('show')) {
                    otherCollapse.classList.remove('show');
                }
            });
        });
    });
});