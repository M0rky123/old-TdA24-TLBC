// LECTURERS - PRINT INTO html

let currentLecturersPage = 1;
const maxLecturersPage = Math.ceil(lecturerCount / 6);
const cardCount = 6;

function createLectCards(page) {
  buttonsDisabler();
  let cards = document.getElementById("cards");
  let lecturers = document.createDocumentFragment();

  fetch(`/api/lecturers/main/${page}`)
    .then((response) => response.json())
    .then((json) => {
      for (let i = 0; i < json.length; i++) {
        let element = document.createElement("div");
        element.classList.add("card");

        try {
          let list = "<ul>";

          for (let j = 0; j < json[i].tags.length; j++) {
            list += `<li><button>${json[i].tags[j].name}</button></li>`;
          }
          list += "</ul>";

          element.innerHTML = `<div class="lecturer"><img class="lect-img" src="${
            json[i].picture_url ? json[i].picture_url : "https://media1.tenor.com/m/QA6mPKs100UAAAAC/caught-in.gif"
          }" alt="LECTURER PROFILE PICTURE" width="80px" height="80px"><div class="info"><div><h4 class="lect-fname">${
            json[i].title_before + " " + json[i].first_name + " " + json[i].middle_name + " " + json[i].last_name + " " + json[i].title_after
          }</h4><p class="lect-claim">${
            json[i].claim
          }</p></div><div class="info-icons"><div class="location"><span class="icon lect-location"><i class="fa-solid fa-location-dot"></i>${
            json[i].location
          }</span></div><div class="price"><span class="icon lect-price"><i class="fa-solid fa-coins"></i>${
            json[i].price_per_hour
          } Kč / hod.</span></div></div></div></div><div><div class="tags lect-tags">${list}</div><a class="lect-uuid" href="/lecturer/${
            json[i].uuid
          }"><div class="visit"><span>Více info</span><span class="icon"><i class="fa-solid fa-arrow-right"></i></span></div></a></div>`;
        } catch (error) {
          element.classList.value = "blank-card";
        }
        lecturers.appendChild(element);
      }
      cards.innerHTML = "";
      cards.appendChild(lecturers);
    });
}

function loadLectCards(page) {
  let cards = document.getElementById("cards");
  buttonsDisabler();

  fetch(`/api/lecturers/main/${page}`)
    .then((response) => response.json())
    .then((json) => {
      const card = document.getElementById("cards").children;
      const img = cards.getElementsByClassName("lect-img");
      const fname = cards.getElementsByClassName("lect-fname");
      const claim = cards.getElementsByClassName("lect-claim");
      const location = cards.getElementsByClassName("lect-location");
      const price = cards.getElementsByClassName("lect-price");
      const tags = cards.getElementsByClassName("lect-tags");
      const uuid = cards.getElementsByClassName("lect-uuid");

      for (let i = 0; i < cardCount; i++) {
        card.item(i).classList.remove("blank-card");
        card.item(i).style.background = "var(--col-light)";
        try {
          img.item(i).setAttribute("src", json[i].picture_url ? json[i].picture_url : "https://media1.tenor.com/m/QA6mPKs100UAAAAC/caught-in.gif");

          fname.item(i).textContent =
            json[i].title_before + " " + json[i].first_name + " " + json[i].middle_name + " " + json[i].last_name + " " + json[i].title_after;

          claim.item(i).textContent = json[i].claim;

          location.item(i).innerHTML = "";
          location.item(i).append(json[i].location);

          price.item(i).innerHTML = "";
          price.item(i).append(json[i].price_per_hour);

          let list = "<ul>";
          for (let j = 0; j < json[i].tags.length; j++) {
            list += `<li><button>${json[i].tags[j].name}</button></li>`;
          }
          list += "</ul>";

          tags.item(i).innerHTML = list;

          uuid.item(i).setAttribute("href", `/lecturer/${json[i].uuid}`);
        } catch (error) {
          card.item(i).classList.add("blank-card");
          card.item(i).style.background = "none";
        }
      }
    });
}

function lectCardsPaging(pages) {
  const container = document.getElementById("pages");

  for (let pagescount = 1; pagescount <= pages; pagescount++) {
    const page = document.createElement("button");
    page.setAttribute("class", "page");
    page.addEventListener("click", () => {
      loadLectCards(pagescount);
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
  loadLectCards(currentLecturersPage);
  buttonsDisabler();
});

lecturersBTNNext.addEventListener("click", () => {
  activePage(currentLecturersPage, currentLecturersPage + 1);
  currentLecturersPage++;
  loadLectCards(currentLecturersPage);
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

createLectCards(1);
horizontalScroll(document.getElementsByClassName("tags"));
outerNumBtnDisabler();
lectCardsPaging(maxLecturersPage);
