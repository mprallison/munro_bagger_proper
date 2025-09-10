const container = document.getElementById('buttons-container');

// Convert object to array of {label, link}
const usersArray = Object.entries(user_links).map(([label, link]) => ({ label, link }));

// Store checkbox states
const checkedUsers = {};

export function addUserButtons(filter = "") {

    
  container.innerHTML = "";

  usersArray
    .filter(item => item.label.toLowerCase().includes(filter.toLowerCase()))
    .forEach(item => {
      // Table row
      const tr = document.createElement('tr');
      tr.style.display = "flex"; // Use flex for scrollable tbody
      tr.style.alignItems = "center";
      tr.style.marginBottom = "5px";

      // Checkbox cell
      const tdCheckbox = document.createElement('td');
      tdCheckbox.style.width = "30px";
      const checkbox = document.createElement('input');
      checkbox.type = "checkbox";
      checkbox.value = item.label;
      checkbox.checked = !!checkedUsers[item.label];
      checkbox.onclick = (e) => {
        e.stopPropagation();
        checkedUsers[item.label] = checkbox.checked;
      };
      tdCheckbox.appendChild(checkbox);

      // Button cell
      const tdButton = document.createElement('td');
      tdButton.style.flexGrow = "1";
      const btn = document.createElement('button');
      btn.style.display = "flex";
      btn.style.alignItems = "center";
      btn.style.gap = "10px";
      btn.style.width = "190px";
      btn.style.height = "30px";
      btn.style.border = "1px solid black";
      btn.style.backgroundColor = "#e0f0ff";
      btn.style.cursor = "pointer";

      // Image
      const img = document.createElement('img');
      img.src = user_imgs[item.label]
      //img.src = `/static/images/${item.label}.png`;
      img.alt = item.label;
      img.style.width = "24px";
      img.style.height = "24px";

      // Text
      const labelText = document.createTextNode(item.label);

      btn.appendChild(img);
      btn.appendChild(labelText);

      btn.onclick = () => window.location.href = item.link;

      tdButton.appendChild(btn);

      tr.appendChild(tdCheckbox);
      tr.appendChild(tdButton);

      container.appendChild(tr);
    });
}

//window.addUserButtons = addUserButtons;