let current_location_pathname = location.pathname;

/////Making the selected navbar item bolder
//Getting my current locaton URL
let menu_item = document.querySelectorAll('.navigationbar_1item a');
let menu_length = menu_item.length;
let e = 0;
for (let i = 1; i < menu_length; i++){
  if (menu_item[i].pathname + "/" === current_location_pathname){
    e=i; 
  }
};
menu_item[e].className = "active";

/////Display the search table once the search button is clicked
let serstat=document.getElementById("search_status").textContent;
if (serstat == "not found") {
  let disp_mess_err = document.getElementById("no_book_found");
  disp_mess_err.style.display = "block";
  document.getElementById("empty_bs_table").style.display="none";
}else if (serstat == "found") {
  document.getElementById("book_search_table").style.display="block";
  document.getElementById("empty_bs_table").style.display="none";
  // disp_res_tab.style.border = "none";
};

/////Creating a button that takes the user  to the top of the page 
//Select the button
mybutton = document.getElementById("top_page");
// When the user scrolls down 500px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
function movetotop_Function() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
} 