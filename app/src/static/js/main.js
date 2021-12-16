// start: left sidebar setting

let left_sidebar_toggler_btn = document.querySelector('.left-sidebar-toggler');
let left_sidebar = document.querySelector('.left-sidebar');
let left_sidebar_status = false;

const leftSidebarToggler = () => {
    if(!left_sidebar_status){
        left_sidebar.style.left = '0%';
        left_sidebar_status = true;
        return;
    }
    
    left_sidebar.style.left = '-100%';
    left_sidebar_status = false;

}

left_sidebar_toggler_btn.addEventListener('click', leftSidebarToggler)

document.addEventListener('click', (event) => {
    if (
        event.target != left_sidebar &&
        event.target != left_sidebar_toggler_btn &&
        left_sidebar_status != true
    ){
        left_sidebar.style.left = '-100%';
        left_sidebar_status = false;
    }
})

// end: left sidebar setting
// start: right sidebar setting

let right_sidebar_toggler_btn = document.querySelector('.right-sidebar-toggler');
let right_sidebar = document.querySelector('.right-sidebar');
let right_sidebar_status = false;

const rightSidebarToggler = () => {
    if(!right_sidebar_status){
        right_sidebar.style.right = '0%';
        right_sidebar_status = true;
        return;
    }
    
    right_sidebar.style.right = '-100%';
    right_sidebar_status = false;

}

right_sidebar_toggler_btn.addEventListener('click', rightSidebarToggler)

document.addEventListener('click', (event) => {
    if (
        event.target != right_sidebar &&
        event.target != right_sidebar_toggler_btn &&
        right_sidebar_status != true
    ){
        right_sidebar.style.right = '-100%';
        right_sidebar_status = false;
    }
})

// end: right sidebar setting