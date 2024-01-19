// LECTURERS - PRINT INTO html

const maxLecturersPage = Math.ceil(lecturerCount / 6);
const cardCount = 6;
let currentPage = 0;

console.log(filterMinMax, listOfTags, lecturerCount, listOfLocation);

let filterTagsArray = [];
let filterLocationsArray = [];
let filterPricesArray = [];

function filtersCreate() {
  const tags = document.getElementById("filter-tags");
  const location = document.getElementById("filter-location");
  const price = document.getElementById("filter-price");

  for (let i = 0; i < listOfTags.length; i++) {
    let li = document.createElement("li");
    li.setAttribute("data-uuid", listOfTags[i][2]);
    li.innerText = listOfTags[i][1];
    li.addEventListener("click", () => {
      if (!filterTagsArray.includes(li.getAttribute("data-uuid"))) {
        filterTagsArray.push(li.getAttribute("data-uuid"));
        li.classList.add("filter-active");
      } else {
        const index = filterTagsArray.indexOf(li.getAttribute("data-uuid"));
        filterTagsArray.splice(index, 1);
        li.classList.remove("filter-active");
      }
      console.log(filterTagsArray);
    });
    tags.append(li);
  }

  for (let i = 0; i < listOfLocation.length; i++) {
    let li = document.createElement("li");
    li.innerText = listOfLocation[i][0];
    li.addEventListener("click", () => {
      if (!filterLocationsArray.includes(li.innerText)) {
        filterLocationsArray.push(li.innerText);
        li.classList.add("filter-active");
      } else {
        const index = filterLocationsArray.indexOf(li.innerText);
        filterLocationsArray.splice(index, 1);
        li.classList.remove("filter-active");
      }
    });
    location.append(li);
  }

  price.innerText += `${filterMinMax.min} - ${filterMinMax.max}`;
  price.innerHTML += `<li><label for="minValue">Min: </label>
  <input type="number" name="minValue"></li>`;
  price.innerHTML += `<li><label for="maxValue">Max: </label>
  <input type="number" name="maxValue"></li>`;
}

filtersCreate();

function filtersGet(tagsArray, locationsArray, pricesArray) {
  fetch("/api/lecturers/filter", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ location: locationsArray, tags: tagsArray, min_max: pricesArray }),
  })
    .then((response) => response.json())
    .then((json) => {
      for (let i = 0; i < cardCount; i++) {
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
          }  Kč / hod.</span></div></div></div></div><div><div class="tags lect-tags">${list}</div><a class="lect-uuid" href="/lecturer/${
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

document.getElementById("search").addEventListener("click", () => {
  filtersGet(filterTagsArray, filterLocationsArray, filterPricesArray);
});

function createLectCards(page) {
  let cards = document.getElementById("cards");
  let lecturers = document.createDocumentFragment();

  fetch(`/api/lecturers/main/${page}`)
    .then((response) => response.json())
    .then((json) => {
      for (let i = 0; i < cardCount; i++) {
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
          }  Kč / hod.</span></div></div></div></div><div><div class="tags lect-tags">${list}</div><a class="lect-uuid" href="/lecturer/${
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

          location.item(i).innerHTML = `<i class="fa-solid fa-location-dot"></i>${json[i].location}`;

          price.item(i).innerHTML = `<i class="fa-solid fa-coins"></i>${json[i].price_per_hour} Kč / hod.`;

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

const lecturersBTNPrevious = document.getElementById("previous");
const lecturersBTNNext = document.getElementById("next");

function lectCardsPaging() {
  const pages = document.getElementById("pages");
  const maxPageLists = 5;

  for (let i = 1; i <= maxPageLists; i++) {
    const page = document.createElement("button");
    page.setAttribute("class", "page");
    page.addEventListener("click", () => {
      loadLectCards(page.innerText);
      buttonsDisabler();
    });
    page.innerText = i;
    pages.append(page);
  }

  pages.children[0].addEventListener("click", () => {
    dedFromListing(pages.children[0], 0, 2);
  });
  pages.children[1].addEventListener("click", () => {
    dedFromListing(pages.children[1], 1, 1);
  });
  pages.children[2].addEventListener("click", () => {
    activePage(2);
  });
  pages.children[3].addEventListener("click", () => {
    addToListing(pages.children[3], 3, 1);
  });
  pages.children[4].addEventListener("click", () => {
    addToListing(pages.children[4], 4, 2);
  });

  pages.children[0].setAttribute("id", "active-page");
  currentPage = 0;

  function addToListing(btn, nthChild, add) {
    intBtn = parseInt(btn.innerText);
    if (intBtn < maxLecturersPage - 1) {
      pages.childNodes.forEach((e) => {
        e.innerText = parseInt(e.innerText) + add;
      });
      activePage(nthChild - add);
    } else {
      activePage(nthChild);
    }
  }

  function dedFromListing(btn, nthChild, ded) {
    intBtn = parseInt(btn.innerText);
    if (intBtn > 2) {
      pages.childNodes.forEach((e) => {
        e.innerText = parseInt(e.innerText) - ded;
      });
      activePage(nthChild + ded);
    } else {
      activePage(nthChild);
    }
  }

  lecturersBTNPrevious.addEventListener("click", () => {
    let activeTEXT = parseInt(document.getElementById("active-page").innerText);
    if (currentPage < maxLecturersPage - 4 && activeTEXT > 3) {
      console.log(activeTEXT);
      pages.childNodes.forEach((e) => {
        e.innerText = parseInt(e.innerText) - 1;
      });
      currentPage -= 1;
      activePage(currentPage + 1);
      loadLectCards(activeTEXT - 1);
    } else {
      console.log(activeTEXT);
      activePage(currentPage - 1);
      loadLectCards(activeTEXT - 1);
    }
    buttonsDisabler();
  });

  lecturersBTNNext.addEventListener("click", () => {
    let activeTEXT = parseInt(document.getElementById("active-page").innerText);
    if (currentPage > 1 && activeTEXT < maxLecturersPage - 2) {
      console.log(activeTEXT);
      pages.childNodes.forEach((e) => {
        e.innerText = parseInt(e.innerText) + 1;
      });
      currentPage += 1;
      activePage(currentPage - 1);
      loadLectCards(activeTEXT + 1);
    } else {
      console.log(activeTEXT);
      activePage(currentPage + 1);
      loadLectCards(activeTEXT + 1);
    }
    buttonsDisabler();
  });

  function activePage(newPage) {
    currentPage = newPage;
    document.getElementById("active-page").removeAttribute("id");
    document.getElementById("pages").children[currentPage].setAttribute("id", "active-page");
  }
}

console.log(currentPage);

function outerNumBtnDisabler() {
  document.getElementById("active-page").innerText == 1 ? (lecturersBTNPrevious.disabled = true) : (lecturersBTNPrevious.disabled = false);
  document.getElementById("active-page").innerText == maxLecturersPage ? (lecturersBTNNext.disabled = true) : (lecturersBTNNext.disabled = false);
}

function buttonsDisabler() {
  lecturersBTNNext.disabled = true;
  lecturersBTNPrevious.disabled = true;
  setTimeout(() => {
    lecturersBTNNext.disabled = false;
    lecturersBTNPrevious.disabled = false;
    outerNumBtnDisabler();
  }, 200);
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

createLectCards(1);
horizontalScroll(document.getElementsByClassName("tags"));
lectCardsPaging();
outerNumBtnDisabler();
