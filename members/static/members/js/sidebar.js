/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.querySelector(".main").style.marginLeft = "250px";
  
  // Update the topnav margin AND shrink its width
  let topnav = document.querySelector(".topnav");
  topnav.style.marginLeft = "250px";
  topnav.style.width = "calc(100% - 250px)";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.querySelector(".main").style.marginLeft = "0";
  document.querySelector(".topnav").style.marginLeft = "0"; /* Added this */

  // Reset the topnav margin AND restore its width
  let topnav = document.querySelector(".topnav");
  topnav.style.marginLeft = "0";
  topnav.style.width = "100%";
}   

function menuClicked() {
    const sidenav = document.getElementById("mySidenav");

    if (sidenav.style.width === "250px") {
        closeNav();
    } else {
        openNav();
    }
}
