// LECTURERS - PRINT INTO html

let currentLecturersPage = 1;
let maxLecturersPage = Math.ceil(lecturerCount / 6);

function printLectCards(page) {
  let cards = document.getElementById("cards");
  let lecturers = document.createDocumentFragment();

  cards.innerHTML = "";

  fetch(`/api/lecturers/main/${page}`)
    .then((response) => response.json())
    .then((json) => {
      for (let i = 0; i < 6; i++) {
        let element = document.createElement("div");
        element.classList.add("card");

        try {
          let list = "<ul>";

          for (let j = 0; j < json[i].tags.length; j++) {
            list += `<li>${json[i].tags[j].name}</li>`;
          }
          list += "</ul>";

          element.innerHTML = `<div class="lecturer"><img src="${
            json[i].picture_url ? json[i].picture_url : "https://media1.tenor.com/m/QA6mPKs100UAAAAC/caught-in.gif"
          }" alt="LECTURER PROFILE PICTURE" width="80px" height="80px"><div class="info"><h4>${
            json[i].title_before + " " + json[i].first_name + " " + json[i].middle_name + " " + json[i].last_name + " " + json[i].title_after
          }</h4><p>${json[i].claim}</p><div class="info-icons"><div class="location"><span class="icon"><i class="fa-solid fa-location-dot"></i>${
            json[i].location
          }</span></div><div class="price"><span class="icon"><i class="fa-solid fa-coins"></i>${
            json[i].price_per_hour
          } Kč / hod.</span></div></div></div></div><div><div class="tags tags-container">${list}</div><a href="/lecturer/${
            json[i].uuid
          }"><div class="visit"><span>Více info</span><span class="icon"><i class="fa-solid fa-arrow-right"></i></span></div></a></div>`;
        } catch (error) {
          element.classList.value = "blank-card";
        }
        lecturers.appendChild(element);
      }
      cards.appendChild(lecturers);
    });
}

function lectCardsPaging(pages) {
  const container = document.getElementById("pages");

  for (let pagescount = 1; pagescount <= pages; pagescount++) {
    const page = document.createElement("a");
    page.setAttribute("href", "#cards");
    page.addEventListener("click", () => {
      printLectCards(pagescount);
      activePage(currentLecturersPage, pagescount);
      currentLecturersPage = pagescount;
      outerNumBtnDisabler();
    });
    page.innerText = pagescount;
    pagesElement.append(page);
  }

  container.children[0].setAttribute("id", "active-page");
}

function activePage(oldPage, newPage) {
  const container = document.getElementById("pages");
  container.children[oldPage - 1].removeAttribute("id");
  container.children[newPage - 1].setAttribute("id", "active-page");
}

function outerNumBtnDisabler() {
  currentLecturersPage == 1 ? (lecturersBTNPrevious.disabled = true) : (lecturersBTNPrevious.disabled = false);

  currentLecturersPage == maxLecturersPage ? (lecturersBTNNext.disabled = true) : (lecturersBTNNext.disabled = false);
}

// TAGS - HORIZONTAL SCROLL

// write me a function to horizontal scroll
function horizontalScroll(container) {
  for (let i = 0; i < container.length; i++) {
    container[i].addEventListener("wheel", function (e) {
      container[i].scrollLeft += e.deltaY > 0 ? 100 : -100;
      e.preventDefault();
    });
  }
}

const lecturersBTNPrevious = document.getElementById("previous");
const lecturersBTNNext = document.getElementById("next");
const pagesElement = document.getElementById("pages");

lecturersBTNPrevious.addEventListener("click", () => {
  activePage(currentLecturersPage, currentLecturersPage - 1);
  currentLecturersPage--;
  printLectCards(currentLecturersPage);
  buttonsDisabler();
});

lecturersBTNNext.addEventListener("click", () => {
  activePage(currentLecturersPage, currentLecturersPage + 1);
  currentLecturersPage++;
  printLectCards(currentLecturersPage);
  buttonsDisabler();
});

function buttonsDisabler() {
  lecturersBTNNext.disabled = true;
  lecturersBTNPrevious.disabled = true;
  setTimeout(() => {
    lecturersBTNNext.disabled = false;
    lecturersBTNPrevious.disabled = false;
    outerNumBtnDisabler();
  }, 200);
}

horizontalScroll(document.getElementsByClassName("tags-container"));
outerNumBtnDisabler();
lectCardsPaging(maxLecturersPage);
printLectCards(currentLecturersPage);
