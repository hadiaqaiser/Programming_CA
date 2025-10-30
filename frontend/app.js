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

