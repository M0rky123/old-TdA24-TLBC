const container = document.getElementsByClassName("tags-container");

// create loop thru all html elements in tags-container
for (let i = 0; i < container.length; i++) {
  container[i].addEventListener("wheel", function (e) {
    container[i].scrollLeft += e.deltaY > 0 ? 100 : -100;
    e.preventDefault();
  });
}

