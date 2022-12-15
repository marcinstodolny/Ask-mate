$('#menu-icon').click(() => $('.menu').fadeToggle(800));

if (message) {
    $('.menu').append(`<p style="font-size: 20px">${message}</p>`);
    if (reputation < 100) {
        $('.menu').append(`<img width="100px" height="100px" src="/static/avatar_lvl1.png"><br><br>`);
    } else if (reputation >= 100 && reputation < 500) {
        $('.menu').append(`<img width="100px" height="100px" src="/static/avatar_lvl2.png"><br><br>`);
    } else if (reputation >= 500 && reputation < 1000) {
        $('.menu').append(`<img width="100px" height="100px" src="/static/avatar_lvl3.png"><br><br>`);
    } else if (reputation >= 1000 && reputation < 5000) {
        $('.menu').append(`<img width="100px" height="100px" src="/static/avatar_lvl4.png"><br><br>`);
    } else if (reputation >= 5000) {
        $('.menu').append(`<img width="100px" height="100px" src="/static/avatar_lvl5.png"><br><br>`);
    }
    $('.menu').append(`<button class="menu-btn" onclick="location.href='/user/${user_id}'">User profile</button>`);
    $('.menu').append(`<button class="menu-btn" onclick="location.href='/add_question'">Add new question</button>`);
    $('.menu').append(`<button class="menu-btn" onclick="location.href='/users'">All users</button>`);
    $('.menu').append(`<button class="menu-btn" onclick="location.href='/bonus-questions'">Bonus questions</button>`);
    $('.menu').append(`<button class="menu-btn" onclick="location.href='/logout'">Logout</button>`);
} else {
    $('.menu').append(`<button class="menu-btn" onclick="location.href='/login'">Login</button>`);
    $('.menu').append(`<button class="menu-btn" onclick="location.href='/registration'">Registration</button>`);
}
