// LECTURERS - PRINT INTO html

function lecturerCards() {
  let currentLecturersPage = 1;
  let maxLecturersPage = 2;

  function printLectCards(page) {
    let cards = document.getElementById("cards");
    let lecturers = document.createDocumentFragment();

    cards.innerHTML = "";

    fetch(`/api/lecturers/main/${page}`)
      .then((response) => response.json())
      .then((json) => {
        for (let i = 0; i < json.length; i++) {
          let element = document.createElement("div");
          element.classList.add("card");

          let list = "<ul>";

          for (let j = 0; j < json[i].tags.length; j++) {
            list += `<li>${json[i].tags[j].name}</li>`;
          }
          list += "</ul>";
          element.innerHTML = `<div class="lecturer">
          <img src="${
            json[i].picture_url ? json[i].picture_url : "https://media1.tenor.com/m/QA6mPKs100UAAAAC/caught-in.gif"
          }" alt="LECTURER PROFILE PICTURE" width="80px" height="80px">
          <div class="info">
            <h4>${json[i].title_before + " " + json[i].first_name + " " + json[i].middle_name + " " + json[i].last_name + " " + json[i].title_after}</h4>
            <p>${json[i].claim}</p>
            <div class="info-icons">
              <div class="location">
                <span class="icon">
                  <i class="fa-solid fa-location-dot"></i>
                  ${json[i].location}
                </span>
              </div>
              <div class="price">
                <span class="icon">
                  <i class="fa-solid fa-coins"></i>
                  ${json[i].price_per_hour} Kč / hod.
                </span>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="tags tags-container">
              ${list}
          </div>
          <a href="/lecturer/${json[i].uuid}">
            <div class="visit">
              <span>Více info</span>
              <span class="icon">
                <i class="fa-solid fa-arrow-right"></i>
              </span>
            </div>
          </a>
        </div>`;
          lecturers.appendChild(element);
        }
        cards.appendChild(lecturers);
      });
  }

  function lectCardsPaging(pages) {
    for (let pagescount = 1; pagescount <= pages; pagescount++) {
      const page = document.createElement("a");
      page.addEventListener("click", () => {
        printLectCards(pagescount);
      });
      page.innerText = pagescount;
      pagesElement.append(page);
    }
  }

  function outerNumBtnDisabler() {
    currentLecturersPage == 1 ? (lecturersBTNPrevious.disabled = true) : (lecturersBTNPrevious.disabled = false);

    currentLecturersPage == maxLecturersPage ? (lecturersBTNNext.disabled = true) : (lecturersBTNNext.disabled = false);
  }

  // TAGS - HORIZONTAL SCROLL

  const container = document.getElementsByClassName("tags-container");

  for (let i = 0; i < container.length; i++) {
    container[i].addEventListener("wheel", function (e) {
      container[i].scrollLeft += e.deltaY > 0 ? 100 : -100;
      e.preventDefault();
    });
  }

  const lecturersBTNPrevious = document.getElementById("previous");
  const lecturersBTNNext = document.getElementById("next");
  const pagesElement = document.getElementById("pages");

  lecturersBTNPrevious.addEventListener("click", () => {
    currentLecturersPage--;
    outerNumBtnDisabler();
    printLectCards(currentLecturersPage);
  });

  lecturersBTNNext.addEventListener("click", () => {
    currentLecturersPage++;
    outerNumBtnDisabler();
    printLectCards(currentLecturersPage);
  });

  outerNumBtnDisabler();
  lectCardsPaging(maxLecturersPage);
  printLectCards(currentLecturersPage);
}

lecturerCards();

// PREDELAT PAGES NA ARRAY ABYCH JE MOHL ZVIRAZNIT A PREDELAT NACITANI LEKTORU PROTOZE TO SKACE A JE TO DOCELA SLOW, VYMYSLET NEJAK PRELOAD ABY TO BYLO RYCHLEJSI
