// сворачивает дублирующие окна в фильтре фильмов
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


// звёзды рейтинга
const stars = document.querySelectorAll('.icon-label');

stars.forEach(star => {
    star.addEventListener('click', () => {
        stars.forEach(s => s.classList.remove('selected'));
        star.classList.add('selected');
    });
});


// добавить рейтинг
const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        // .then(response => alert("Рейтинг установлен"))
        // .catch(error => alert("Ошибка"))
});
  