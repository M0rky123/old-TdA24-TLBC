document.addEventListener("DOMContentLoaded", () => {
  let childDivs = document.getElementsByClassName("table-info");
  let maxWidth = Math.max.apply(
    null,
    Array.from(childDivs).map(function (div) {
      return div.clientWidth;
    })
  );

  document.documentElement.style.setProperty("--child-max-width", "0");
  document.documentElement.style.setProperty("--child-max-width", maxWidth + "px");

  // mail wrapping at smaller screen sizes
  const table = document.getElementById("table");
  const mail = document.getElementById("mail");
  const ul = document.querySelectorAll("#mail ul li");

  if (mail > table.clientWidth - 48) {
    mail.style.whiteSpace = "wrap";
    mail.style.width = table.clientWidth - 48;
  } else {
    mail.style.whiteSpace = "normal";
    mail.style.width = "100%";
  }

  window.addEventListener("resize", function () {
    // if mail is bigger than table + 3rem then set white-space to mail to wrap

    if (mail.clientWidth > table.clientWidth - 48) {
      ul.forEach((element) => {
        element.style.whiteSpace = "wrap";
        element.style.width = table.clientWidth - 48;
      });
    } else {
      ul.forEach((element) => {
        element.style.whiteSpace = "nowrap";
        element.style.width = "100%";
      });
    }
  });
});
