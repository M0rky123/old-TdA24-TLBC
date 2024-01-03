document.addEventListener("DOMContentLoaded", function () {
  var childDivs = document.getElementsByClassName("table-info");
  var maxWidth = Math.max.apply(
    null,
    Array.from(childDivs).map(function (div) {
      return div.clientWidth;
    })
  );

  document.documentElement.style.setProperty("--child-max-width", "0");
  document.documentElement.style.setProperty("--child-max-width", maxWidth + "px");
});
