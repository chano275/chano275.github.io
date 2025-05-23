function checkedHandler(checkbox) {
    if(!checkbox.checked) {
      document.getElementById("container").style.paddingTop = "4rem";
    }
    else {
      document.getElementById("container").style.paddingTop = "40rem";
    }
  }