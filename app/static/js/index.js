// LECTURERS - PRINT INTO html

let currentLecturersPage = 1;
let maxLecturersPage = 2;

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

console.log("cau");

// PREDELAT PAGES NA ARRAY ABYCH JE MOHL ZVIRAZNIT A PREDELAT NACITANI LEKTORU PROTOZE TO SKACE A JE TO DOCELA SLOW, VYMYSLET NEJAK PRELOAD ABY TO BYLO RYCHLEJSI
