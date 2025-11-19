const API = "http://127.0.0.1:5001";
// start small data, just lipstick shades for test
const mockShades = [
  {product_name:"Medora Lipstick", shade_name:"Cherry", shade_code:"21", finish:"Matte", color_family:"Red", msrp:450},
  {product_name:"Medora Lipstick", shade_name:"Rose", shade_code:"22", finish:"Glowy", color_family:"Pink", msrp:450},
  {product_name:"Medora Lipstick", shade_name:"Rust", shade_code:"23", finish:"Matte", color_family:"Brown", msrp:450},
];

// addin foundation product too, so i can test category later
mockShades.push(
  {product_name:"Medora Foundation", shade_name:"Ivory", shade_code:"11", finish:"Matte", color_family:"Light", msrp:1200},
  {product_name:"Medora Foundation", shade_name:"Honey", shade_code:"14", finish:"Glowy", color_family:"Medium", msrp:1200},
  {product_name:"Medora Foundation", shade_name:"Cocoa", shade_code:"16", finish:"Glowy", color_family:"Dark", msrp:1200}
);

// just empty array now, later i will push wishlist items here
let wishlistData = [];


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
    ["Red","Pink","Brown"].forEach(fam => {
      const o = document.createElement("option");
      o.value = fam;
      o.textContent = fam;
      colorSelect.appendChild(o);
    });
  }
}

//add shade finder filter and table render js. working nice now
//write this function with my own logic but used gpt for filter syntax idea
function getRecs() {
  const cat = document.getElementById("recCategory").value.trim();
  const fam = document.getElementById("recColor").value.trim();
  const fin = document.getElementById("recFinish").value.trim();

  //filter check was confusing me so i used gpt for this
  const result = mockShades.filter(s => {
    const matchCat = !cat || s.product_name.toLowerCase().includes(cat);
    const matchFam = !fam || s.color_family === fam;
    const matchFin = !fin || s.finish === fin;
    return matchCat && matchFam && matchFin;
  });

  const tbody = document.getElementById("recTableBody");
  tbody.innerHTML = "";

  if (result.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="7">no match found</td>`;
    tbody.appendChild(tr);
    return;
  }

  result.forEach(shade => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${shade.product_name}</td>
      <td>${shade.shade_name}</td>
      <td>${shade.shade_code}</td>
      <td>${shade.finish}</td>
      <td>${shade.color_family}</td>
      <td>${shade.msrp}</td>
      <td><button onclick="addToWishlistQuick('${shade.shade_name}')">♥</button></td>
    `;
    tbody.appendChild(tr);
  });
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

//wishlist added using local array, can add and delete items now
function fakeAddWishlist(){
  const email = document.getElementById("wishEmail").value.trim();
  const shadeId = document.getElementById("wishShadeId").value.trim();
  const note = document.getElementById("wishNote").value.trim();

  if(!email || !shadeId){
    alert("email and shade needed");
    return;
  }

  wishlistData.push({ email, shadeId, note });
  renderWishlistTable();
}

function renderWishlistTable(){
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
      <td><button onclick="deleteWishlistRow(${index})">X</button></td>
    `;
    tbody.appendChild(tr);
  });
}

function deleteWishlistRow(i){
  wishlistData.splice(i,1);
  renderWishlistTable();
}

function addToWishlistQuick(shadeName){
  alert("saved " + shadeName + " to wishlist (frontend demo)");}
