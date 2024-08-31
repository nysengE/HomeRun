const views = document.querySelectorAll('.view');

views.forEach((view) => {
    view.addEventListener('click', () => {

        const clubno = view.querySelector('.clubno').value;

        window.location.href='/club/view/'+clubno;


    });
})
