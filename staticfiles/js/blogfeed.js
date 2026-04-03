(function () {
  const row = document.getElementById("categoryRow");
  const left = document.querySelector(".left-nav");
  const right = document.querySelector(".right-nav");
  const scrollAmount = 200;
  left.addEventListener("click", () =>
    row.scrollBy({ left: -scrollAmount, behavior: "smooth" }),
  );
  right.addEventListener("click", () =>
    row.scrollBy({ left: scrollAmount, behavior: "smooth" }),
  );
})();
