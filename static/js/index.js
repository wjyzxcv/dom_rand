event_expan = ["9", "10", "13", "15", "16"];

function reset_ex(onload = true) {
  if (onload) {
    document.getElementById("inputs").reset();
  }
  for (let opt of document.getElementById("expan")) {
    opt.disabled = false;
  }
  document.getElementById("sel_expan").style.display = "none";
  document.getElementById("lab_card_expan").innerHTML = "No. of Expansions";
}

function load_fun(expan_list) {
  expan_sel = document.getElementById("expan");
  for (let i = 0; i < expan_list.length; i++) {
    new_opt = document.createElement("option");
    new_opt.value = i.toString();
    new_opt.innerHTML = expan_list[i];
    expan_sel.appendChild(new_opt);
  }
  expan_sel.selectedIndex = 0;
  reset_ex();
}

function mode_sel() {
  reset_ex(false);
  mode = document.getElementById("mode").value;
  switch (mode) {
    case "a":
      document.getElementById("lab_card_expan").innerHTML = "No. of Expansions";
      break;
    case "b":
      document.getElementById("sel_expan").style.display = "";
      document.getElementById("lab_card_expan").innerHTML = "No. of Cards";
      break;
    case "c":
      for (let opt of document.getElementById("expan")) {
        if (!event_expan.includes(opt.value.toString())) {
          opt.disabled = true;
        }
      }
      expan_sel.selectedIndex = parseInt(event_expan[0]);
      document.getElementById("sel_expan").style.display = "";
      document.getElementById("lab_card_expan").innerHTML = "No. of Cards";
      break;
    case "d":
    case "e":
    case "f":
    case "g":
      document.getElementById("lab_card_expan").innerHTML = "No. of Cards";
      break;
    case "h":
      document.getElementById("lab_card_expan").innerHTML = "No. of Cards";
      break;
  }
}
