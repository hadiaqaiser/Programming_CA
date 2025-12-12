// Changing API base URL to empty string so frontend calls same host/port (works when Flask serves frontend on EC2)
const API = "";

//shade finder that calls backend /api/shades instead of local mockShades
async function getRecs() {
  const cat = document.getElementById("recCategory").value.trim();
  const fam = document.getElementById("recColor").value.trim();
  const fin = document.getElementById("recFinish").value.trim();

  // build query string same way as ca2
  const params = new URLSearchParams();
  if (cat) params.append("category", cat);
  if (fam) params.append("color_family", fam);
  if (fin) params.append("finish", fin);

  const tbody = document.getElementById("recTableBody");
  tbody.innerHTML = `<tr><td colspan="7">loading shades…</td></tr>`;

  try {
    const res = await fetch(`${API}/api/shades?` + params.toString());
    if (!res.ok) {
      throw new Error("backend problem " + res.status);
    }
    const data = await res.json();

    tbody.innerHTML = "";

    if (!data || data.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td colspan="7">no match found</td>`;
      tbody.appendChild(tr);
      return;
    }

    // using data from backend
    data.forEach(shade => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${shade.product_name}</td>
        <td>${shade.shade_name}</td>
        <td>${shade.shade_code}</td>
        <td>${shade.finish}</td>
        <td>${shade.color_family}</td>
        <td>${shade.msrp}</td>
        <td><button class="btn btn-secondary" onclick="addToWishlistQuick('${shade.shade_name}')">♥</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="7">error talking to backend</td></tr>`;
  }
}

// just empty array now, later i will push wishlist items here
let wishlistData = [];

// keep review rows in a simple array so i can redraw the review table after each api call
let reviewData = [];

// function for dropdown when user change category (foundation/lipstick)
function updateColorOptions() {
  const cat = document.getElementById("recCategory").value;
  const colorSelect = document.getElementById("recColor");

  // clear old options
  colorSelect.innerHTML = "";

  // default first option
  const optBlank = document.createElement("option");
  optBlank.value = "";
  optBlank.textContent = "-- pick color --";
  colorSelect.appendChild(optBlank);

  // if category is foundation → show Light/Medium/Dark
  if (cat === "foundation") {
    ["Light", "Medium", "Dark"].forEach(fam => {
      const o = document.createElement("option");
      o.value = fam;
      o.textContent = fam;
      colorSelect.appendChild(o);
    });

    // else if category is lipstick → show Red/Pink/Brown
  } else if (cat === "lipstick") {
    ["Red", "Pink", "Brown"].forEach(fam => {
      const o = document.createElement("option");
      o.value = fam;
      o.textContent = fam;
      colorSelect.appendChild(o);
    });
  }
}

//CheckAuth using Flask Api
async function checkAuth() {
  const code = document.getElementById("batchInput").value.trim();

  const authArea = document.getElementById("authArea");
  const authError = document.getElementById("authError");
  const statusText = document.getElementById("authStatusText");

  // hide old stuff
  authArea.style.display = "none";
  authError.style.display = "none";

  if (!code) {
    alert("Please enter a batch code");
    return;
  }

  const res = await fetch(`${API}/api/auth/check?batch_code=${encodeURIComponent(code)}`);
  const data = await res.json();

  if (!data.authentic) {
    authError.style.display = "block";
    return;
  }

  // writing all results in table
  const shade = data.shade_info || {};
  const batch = data.batch_info || {};

  statusText.textContent = `Result: ${data.status}`;

  document.getElementById("authProductCell").textContent = data.product_name;
  document.getElementById("authShadeCell").textContent = shade.shade_name;
  document.getElementById("authFinishCell").textContent = shade.finish;
  document.getElementById("authFamilyCell").textContent = shade.color_family;

  document.getElementById("authBatchCell").textContent = batch.batch_code;
  document.getElementById("authMfgCell").textContent = batch.mfg_date;
  document.getElementById("authExpiryCell").textContent = batch.expiry_date;
  document.getElementById("authQualityCell").textContent = batch.status;

  authArea.style.display = "block";
}

// now instead of only updating local array i also send the wishlist item to my flask backend so it is stored in sqlite and will load next time too.
// source: i used MDN fetch POST example with JSON body: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options

async function fakeAddWishlist() {
  const email = document.getElementById("wishEmail").value.trim();
  const shadeId = document.getElementById("wishShadeId").value.trim();
  const note = document.getElementById("wishNote").value.trim();

  if (!email || !shadeId) {
    alert("email and shade needed");
    return;
  }

  try {
    const res = await fetch(`${API}/api/wishlist`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email,
        shade_id: parseInt(shadeId, 10),
        note: note,
      }),
    });

    if (!res.ok) {
      alert("could not save wishlist item (backend error)");
      console.error("wishlist POST failed", res.status);
      return;
    }

    const saved = await res.json();

    // after saving wishlist item in flask api, i reload full list from backend so table always matches sqlite db, not just my local array
    // source: i followed MDN fetch GET example idea and reused my own loadWishlistFromApi() helper → https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

    await loadWishlistFromApi();  // pull fresh wishlist rows from backend

    // clear inputs for nicer UX
    document.getElementById("wishEmail").value = "";
    document.getElementById("wishShadeId").value = "";
    document.getElementById("wishNote").value = "";

    // clear inputs for nicer UX
    document.getElementById("wishEmail").value = "";
    document.getElementById("wishShadeId").value = "";
    document.getElementById("wishNote").value = "";
  } catch (err) {
    console.error("wishlist POST error", err);
    alert("network problem while saving wishlist");
  }
}

// when page loads i want to pull existing wishlist rows from flask api n keep them inside my local wishlistData array so table shows real db data.
// Ref: Followed basic fetch GET example from MDN docs: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

async function loadWishlistFromApi() {
  try {
    const res = await fetch(`${API}/api/wishlist`);
    if (!res.ok) {
      console.error("wishlist GET failed", res.status);
      return;
    }

    const data = await res.json();

    // overwrite local array with data from server
    wishlistData = data.map(row => ({
      id: row.id,          // <-- NEW
      email: row.email,
      shadeId: row.shade_id,
      note: row.note || ""
    }));

    renderWishlistTable();
  } catch (err) {
    console.error("wishlist GET error", err);
  }
}

// this loads all reviews for the shade id typed in the box and fills reviewData + table using /api/reviews?shade_id=..
// source: followed MDN fetch GET example again: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

async function loadReviewsForShade() {
  const shadeId = document.getElementById("reviewShadeId").value.trim();

  if (!shadeId) {
    alert("please type shade id first");
    return;
  }

  try {
    const res = await fetch(`${API}/api/reviews?shade_id=${encodeURIComponent(shadeId)}`);
    if (!res.ok) {
      console.error("reviews GET failed", res.status);
      alert("could not load reviews (backend error)");
      return;
    }

    const data = await res.json();

    // overwrite local review array
    reviewData = data.map(r => ({
      email: r.email,
      rating: r.rating,
      comment: r.comment || ""
    }));

    renderReviewTable();
  } catch (err) {
    console.error("reviews GET error", err);
    alert("network problem while loading reviews");
  }
}

function renderWishlistTable() {
  const tbody = document.getElementById("wishTableBody");
  tbody.innerHTML = "";

  if (wishlistData.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="4">wishlist empty</td>`;
    tbody.appendChild(tr);
    return;
  }

  wishlistData.forEach((row, index) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.email}</td>
      <td>${row.shadeId}</td>
      <td>${row.note || ""}</td>
      <td><button class="btn btn-secondary" onclick="deleteWishlistRow(${row.id})">X</button></td>
    `;
    tbody.appendChild(tr);
  });
}

// now delete button asks flask api to remove row from sqlite and then reloads fresh wishlist from server
// source: fetch DELETE pattern from MDN Fetch docs https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options

async function deleteWishlistRow(id) {
  const ok = confirm("Remove this wishlist item?");
  if (!ok) {
    return;
  }

  try {
    const res = await fetch(`${API}/api/wishlist/${id}`, {
      method: "DELETE",
    });

    if (!res.ok) {
      console.error("wishlist DELETE failed", res.status);
      alert("could not delete wishlist item (backend error)");
      return;
    }

    // reload from backend so ui matches database
    await loadWishlistFromApi();
  } catch (err) {
    console.error("wishlist DELETE error", err);
    alert("network problem while deleting wishlist");
  }
}

function addToWishlistQuick(shadeName) {
  alert("saved " + shadeName + " to wishlist (frontend demo)");
}

// sends a new review to flask backend and reloads review table
// source: mdn fetch POST json example
async function submitReview() {
  const shadeId = document.getElementById("reviewShadeId").value.trim();
  const email = document.getElementById("reviewEmail").value.trim();
  const rating = document.getElementById("reviewRating").value;
  const comment = document.getElementById("reviewComment").value.trim();

  if (!shadeId || !email || !rating) {
    alert("please fill shade id, email and rating");
    return;
  }

  try {
    const res = await fetch(`${API}/api/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        shade_id: parseInt(shadeId, 10),
        email: email,
        rating: parseInt(rating, 10),
        comment: comment,
      }),
    });

    if (!res.ok) {
      console.error("review POST failed", res.status);
      alert("could not save review (backend error)");
      return;
    }

    // reload reviews for same shade
    await loadReviewsForShade();

    // clear fields except shade id
    document.getElementById("reviewEmail").value = "";
    document.getElementById("reviewRating").value = "";
    document.getElementById("reviewComment").value = "";
  } catch (err) {
    console.error("review POST error", err);
    alert("network problem while saving review");
  }
}

// renders review table using the reviewData array
// source: basic DOM table update using innerHTML loop
function renderReviewTable() {
  const tbody = document.getElementById("reviewTableBody");
  tbody.innerHTML = "";

  if (reviewData.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="3">no reviews loaded yet</td>`;
    tbody.appendChild(tr);
    return;
  }

  reviewData.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${r.email}</td>
      <td>${r.rating}</td>
      <td>${r.comment}</td>
    `;
    tbody.appendChild(tr);
  });
}

// this makes sure my wishlist data is loaded as soon as html is ready so table is not empty when student opens MedoraCare page.
// source: using DOMContentLoaded from MDN event docs: https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event

window.addEventListener("DOMContentLoaded", loadWishlistFromApi);